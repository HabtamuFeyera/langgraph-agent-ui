from dataclasses import dataclass
from tools import StockPriceTool
from langgraph.graph.state import CompiledStateGraph

from agents.financial_agent.financial_agent import financial_agent
from agents.bg_task_agent.bg_task_agent import bg_task_agent
from agents.chatbot import chatbot
from agents.research_assistant import research_assistant
from agents.travel_agent import travel_agent  # Import the travel agent
from schema import AgentInfo

DEFAULT_AGENT = "research-assistant"

@dataclass
class Agent:
    description: str
    graph: CompiledStateGraph


agents: dict[str, Agent] = {
    "chatbot": Agent(description="A simple chatbot.", graph=chatbot),
    "research-assistant": Agent(
        description="A research assistant with web search and calculator.", graph=research_assistant
    ),
    "bg-task-agent": Agent(description="A background task agent.", graph=bg_task_agent),
    "financial-agent": Agent(
        description="A financial agent for stock prices, currency conversion, and more.",
        graph=financial_agent,
    ),
    "travel-agent": Agent(  # Add the travel agent
        description="An AI Travel Agent for destination recommendations, weather updates, and travel planning.",
        graph=travel_agent,
    ),
}


def get_agent(agent_id: str) -> CompiledStateGraph:
    return agents[agent_id].graph


def get_all_agent_info() -> list[AgentInfo]:
    return [
        AgentInfo(key=agent_id, description=agent.description) for agent_id, agent in agents.items()
    ]
