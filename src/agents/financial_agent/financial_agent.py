from datetime import datetime
from typing import Literal

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.runnables import RunnableConfig, RunnableLambda, RunnableSerializable
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.managed import RemainingSteps

from agents.llama_guard import LlamaGuard, LlamaGuardOutput, SafetyAssessment
from core import get_model, settings

import yfinance as yf

class AgentState(MessagesState, total=False):
    safety: LlamaGuardOutput
    remaining_steps: RemainingSteps


current_date = datetime.now().strftime("%B %d, %Y")
instructions = f"""
    You are a financial assistant capable of providing financial data and advice.
    You can retrieve stock prices, exchange rates, and perform basic financial calculations.
    Today's date is {current_date}.

    NOTE: THE USER CAN'T SEE THE TOOL RESPONSE.

    A few things to remember:
    - Always verify your data using reliable financial sources.
    - If citing specific stock prices or exchange rates, include markdown-formatted links to any citations.
    - Avoid providing financial advice unless explicitly requested and frame responses cautiously.
"""


def wrap_model(model: BaseChatModel) -> RunnableSerializable[AgentState, AIMessage]:
    preprocessor = RunnableLambda(
        lambda state: [SystemMessage(content=instructions)] + state["messages"],
        name="StateModifier",
    )
    return preprocessor | model


def format_safety_message(safety: LlamaGuardOutput) -> AIMessage:
    content = (
        f"This conversation was flagged for unsafe content: {', '.join(safety.unsafe_categories)}"
    )
    return AIMessage(content=content)


async def acall_model(state: AgentState, config: RunnableConfig) -> AgentState:
    m = get_model(config["configurable"].get("model", settings.DEFAULT_MODEL))
    model_runnable = wrap_model(m)
    response = await model_runnable.ainvoke(state, config)

    # LlamaGuard for content safety
    llama_guard = LlamaGuard()
    safety_output = await llama_guard.ainvoke("Agent", state["messages"] + [response])
    if safety_output.safety_assessment == SafetyAssessment.UNSAFE:
        return {"messages": [format_safety_message(safety_output)], "safety": safety_output}

    if state["remaining_steps"] < 2 and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="Sorry, need more steps to process this request.",
                )
            ]
        }
    return {"messages": [response]}


async def get_stock_price(query: str) -> str:
    try:
        stock_symbol = query.split("stock price of")[-1].strip()
        ticker = yf.Ticker(stock_symbol)
        price = ticker.info["regularMarketPrice"]
        return f"The current stock price of {stock_symbol} is ${price:.2f}."
    except Exception as e:
        return f"Unable to retrieve stock price. Error: {str(e)}"


async def financial_tool(state: AgentState, config: RunnableConfig) -> AgentState:
    last_message = state["messages"][-1].content.lower()
    if "stock price" in last_message:
        response_content = await get_stock_price(last_message)
        return {"messages": [AIMessage(content=response_content)]}
    return {"messages": [AIMessage(content="Financial query not recognized.")]}


async def llama_guard_input(state: AgentState, config: RunnableConfig) -> AgentState:
    llama_guard = LlamaGuard()
    safety_output = await llama_guard.ainvoke("User", state["messages"])
    return {"safety": safety_output}


async def block_unsafe_content(state: AgentState, config: RunnableConfig) -> AgentState:
    safety: LlamaGuardOutput = state["safety"]
    return {"messages": [format_safety_message(safety)]}


# Define the graph
agent = StateGraph(AgentState)
agent.add_node("model", acall_model)
agent.add_node("financial_tool", financial_tool)
agent.add_node("guard_input", llama_guard_input)
agent.add_node("block_unsafe_content", block_unsafe_content)
agent.set_entry_point("guard_input")


# Check for unsafe input and block further processing if found
def check_safety(state: AgentState) -> Literal["unsafe", "safe"]:
    safety: LlamaGuardOutput = state["safety"]
    match safety.safety_assessment:
        case SafetyAssessment.UNSAFE:
            return "unsafe"
        case _:
            return "safe"


agent.add_conditional_edges(
    "guard_input", check_safety, {"unsafe": "block_unsafe_content", "safe": "financial_tool"}
)

# Always END after blocking unsafe content
agent.add_edge("block_unsafe_content", END)

# After "financial_tool", END.
agent.add_edge("financial_tool", END)

financial_agent = agent.compile(checkpointer=MemorySaver())
