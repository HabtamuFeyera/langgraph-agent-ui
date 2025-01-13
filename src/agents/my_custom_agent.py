from datetime import datetime
from typing import Literal

from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.runnables import RunnableConfig, RunnableLambda, RunnableSerializable
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.managed import RemainingSteps
from langgraph.prebuilt import ToolNode

from agents.tools import calculator
from core import get_model, settings


class MyCustomAgentState(MessagesState, total=False):
    """Custom agent's state."""
    remaining_steps: RemainingSteps


# Define tools for the agent
web_search = DuckDuckGoSearchResults(name="WebSearch")
tools = [web_search, calculator]

# Custom instruction for the agent
current_date = datetime.now().strftime("%B %d, %Y")
instructions = f"""
    You are a helpful assistant with advanced capabilities for searching the web, performing calculations,
    and analyzing user queries. You also have a unique ability to handle additional tools designed for custom tasks.
    Today's date is {current_date}.

    Guidelines:
    - Provide concise and clear responses.
    - Use the calculator tool for math questions and the web search tool for research tasks.
    - Respond in markdown format when appropriate for better readability.
    """


def wrap_model(model: BaseChatModel) -> RunnableSerializable[MyCustomAgentState, AIMessage]:
    model = model.bind_tools(tools)
    preprocessor = RunnableLambda(
        lambda state: [SystemMessage(content=instructions)] + state["messages"],
        name="StateModifier",
    )
    return preprocessor | model


async def acall_model(state: MyCustomAgentState, config: RunnableConfig) -> MyCustomAgentState:
    m = get_model(config["configurable"].get("model", settings.DEFAULT_MODEL))
    model_runnable = wrap_model(m)
    response = await model_runnable.ainvoke(state, config)

    # Handle response or add additional processing if necessary
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


# Define the graph
my_custom_agent = StateGraph(MyCustomAgentState)
my_custom_agent.add_node("model", acall_model)
my_custom_agent.add_node("tools", ToolNode(tools))
my_custom_agent.set_entry_point("model")

# Always END after processing tools
my_custom_agent.add_edge("tools", END)

# After "model", if there are tool calls, run "tools". Otherwise END.
def pending_tool_calls(state: MyCustomAgentState) -> Literal["tools", "done"]:
    last_message = state["messages"][-1]
    if not isinstance(last_message, AIMessage):
        raise TypeError(f"Expected AIMessage, got {type(last_message)}")
    if last_message.tool_calls:
        return "tools"
    return "done"


my_custom_agent.add_conditional_edges("model", pending_tool_calls, {"tools": "tools", "done": END})

# Compile the graph with a memory saver for checkpointing
my_custom_agent = my_custom_agent.compile(checkpointer=MemorySaver())
