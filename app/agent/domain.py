from typing import TypedDict

from app.agent.prompts import AGENT_IDENTITY


class AgentConfig(TypedDict):
    name: str
    model: str
    instruction: str
    session_timeout: int


agent_config: AgentConfig = {
    "name": "medixio",
    "model": "gemini-3.1-flash-lite-preview",
    "instruction": AGENT_IDENTITY,
    "session_timeout": 30 * 60,
}
