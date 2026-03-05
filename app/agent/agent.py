import time
from typing import TypedDict

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.genai import types

from app.agent.prompts import AGENT_IDENTITY
from app.modules.users.domain import UserMessenger


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


class Agent:
    def __init__(self):
        self.__session_service = InMemorySessionService()
        self.agent = LlmAgent(
            model=agent_config.get("model"),
            name=agent_config.get("name"),
            instruction=agent_config.get("instruction"),
        )
        self.__runner = Runner(
            agent=self.agent,
            session_service=self.__session_service,
            app_name=agent_config.get("name"),
        )

    async def __get_session(self, user: UserMessenger) -> Session | None:
        session = await self.__session_service.get_session(
            app_name=agent_config.get("name"),
            session_id=str(user.messenger_id),
            user_id=str(user.messenger_id),
        )
        if not session:
            session = await self.__session_service.create_session(
                app_name=agent_config.get("name"),
                session_id=str(user.messenger_id),
                user_id=str(user.messenger_id),
                state={"first_name": user.first_name, "last_name": user.last_name},
            )
        return session

    async def __is_idle_session(self, session: Session) -> bool:
        now = time.time()
        return (now - session.last_update_time) > agent_config.get("session_timeout")

    async def __clear_session_if_idle(self, user: UserMessenger):
        session = await self.__get_session(user)
        if session and await self.__is_idle_session(session):
            await self.__runner.session_service.delete_session(
                app_name=agent_config.get("name"),
                session_id=str(user.messenger_id),
                user_id=str(user.messenger_id),
            )

    async def ask(self, user: UserMessenger, question: str) -> str:
        await self.__clear_session_if_idle(user)
        message = types.Content(role="user", parts=[types.Part(text=question)])
        async for event in self.__runner.run_async(
            user_id=str(user.messenger_id),
            session_id=str(user.messenger_id),
            new_message=message,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                return event.content.parts[0].text or ""
        return ""
