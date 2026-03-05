# Building a Conversational Agent with Google ADK

Google ADK (Agent Development Kit) is not as straightforward as calling `agent.ask("hello")`. It has a specific architecture that took some trial and error to understand. This post documents how it works and the patterns we settled on for Medixio.

## The Architecture

Three components work together:

- **`LlmAgent`** — defines the agent's identity: model, name, and instruction prompt. It's pure configuration with no state.
- **`Runner`** — orchestrates execution. It receives messages, finds the right session, calls the agent, and streams events back.
- **`SessionService`** — stores conversation history. The Runner reads and writes sessions through it.

You never call the agent directly. The flow is always: **you → Runner → SessionService → LlmAgent → events back to you**.

## Lifecycle

The key insight is that these components have different lifetimes:

| Component | Lifetime | Why |
|---|---|---|
| `LlmAgent` | App (singleton) | Stateless configuration |
| `Runner` | App (singleton) | Stateless orchestrator |
| `SessionService` | App (singleton) | Manages the session store |
| `Session` | Per user | Holds conversation history |

Create `LlmAgent`, `Runner`, and `SessionService` once when your app starts. Sessions are created per user on first interaction and reused across messages.

## Setting Up the Runner

```python
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()

runner = Runner(
    agent=LlmAgent(
        model="gemini-2.0-flash-lite",
        name="my_agent",
        instruction="You are a helpful assistant.",
    ),
    app_name="my_app",
    session_service=session_service,
)
```

The `agent` parameter must be a `BaseAgent` instance — not a string name.

## Sending a Message

The Runner's `run_async` returns an async generator of `Event` objects. Most events are intermediate steps (tool calls, internal reasoning). You only care about the final one:

```python
from google.genai import types

message = types.Content(
    role="user",
    parts=[types.Part(text="Hello")]  # text= is required, not positional
)

async for event in runner.run_async(
    user_id="user_123",
    session_id="user_123",
    new_message=message,
):
    if event.is_final_response() and event.content and event.content.parts:
        response = event.content.parts[0].text or ""
```

`event.content.parts` can be `None` even when `event.content` is not, so both checks are needed. `parts[0].text` is `Optional[str]`, so the `or ""` handles the linter and edge cases.

## Session Management

### `auto_create_session`

The Runner has an `auto_create_session=False` default. Without it, calling `run_async` with an unknown `session_id` raises `SessionNotFoundError`. You can enable it:

```python
Runner(..., auto_create_session=True)
```

But this creates sessions without any initial state. If you need to seed user data into the session on creation, manage sessions yourself:

```python
async def get_or_create_session(self, user):
    session = await self.session_service.get_session(
        app_name="my_app",
        user_id=str(user.id),
        session_id=str(user.id),
    )
    if not session:
        session = await self.session_service.create_session(
            app_name="my_app",
            user_id=str(user.id),
            session_id=str(user.id),
            state={"first_name": user.first_name, "last_name": user.last_name},
        )
    return session  # don't forget to return it
```

Always return the session — forgetting `return session` is a silent bug that causes `SessionNotFoundError` later.

### Session Timeout

For a conversational bot, it makes sense to reset context after a period of inactivity. Use `session.last_update_time` (a Unix timestamp the ADK maintains automatically):

```python
async def clear_if_idle(self, user, session):
    if (time.time() - session.last_update_time) > SESSION_TIMEOUT:
        await session_service.delete_session(
            app_name="my_app",
            user_id=str(user.id),
            session_id=str(user.id),
        )
        # next call to get_or_create_session will create a fresh one
```

### Session Storage Options

ADK ships with four session service implementations:

| Service | Backend | Use case |
|---|---|---|
| `InMemorySessionService` | RAM | Development only, lost on restart |
| `SqliteSessionService` | SQLite | Simple single-server deployments |
| `DatabaseSessionService` | SQLAlchemy (Postgres, MySQL) | Production multi-instance |
| `VertexAiSessionService` | Google Cloud | Managed cloud deployments |

For most bots, `InMemorySessionService` is fine if the conversation context isn't business-critical. The actual domain data (appointments, users) should live in your own database regardless.

## Injecting User Context into the Prompt

ADK automatically replaces `{variable_name}` placeholders in string instructions with values from the session state before sending to the LLM.

```python
AGENT_IDENTITY = """
You are a helpful assistant.
You are talking with {first_name?} {last_name?}.
"""
```

The `?` suffix makes the variable optional — if the key is missing from the state, it substitutes an empty string instead of raising a `KeyError`. Without `?`, a missing key throws an error.

The state must be flat. Nested dicts like `{user.name}` do not work — only `artifact.filename` has special dot-notation handling. Keep your state keys as flat identifiers:

```python
state={"first_name": "Jose", "last_name": "Garcia"}
```

**Important:** this automatic injection only works when `instruction` is a plain string. If you pass a callable as `instruction`, ADK skips the injection and expects you to handle it manually.

## Wrapping Everything in a Clean Interface

Rather than scattering Runner and session logic across the codebase, encapsulate it all in a single class:

```python
class Agent:
    def __init__(self):
        self.__session_service = InMemorySessionService()
        self.__runner = Runner(
            agent=LlmAgent(model=..., name=..., instruction=...),
            app_name="my_app",
            session_service=self.__session_service,
        )

    async def ask(self, user: User, question: str) -> str:
        await self.__clear_session_if_idle(user)
        message = types.Content(role="user", parts=[types.Part(text=question)])
        async for event in self.__runner.run_async(
            user_id=str(user.id),
            session_id=str(user.id),
            new_message=message,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                return event.content.parts[0].text or ""
        return ""
```

Callers only need to call `agent.ask(user, text)`. All the ADK plumbing stays hidden.

## Common Pitfalls

**`is_idle_session` must be awaited.** If it's an `async` method and you forget `await`, the coroutine object is always truthy — your sessions will always be deleted immediately after creation.

**`get_session` returns `None`, not an exception.** `SessionNotFoundError` comes from the Runner, not the session service. If you see it, a session wasn't created before `run_async` was called.

**`types.Part(text=question)`, not `types.Part(question)`.** The `text` argument is keyword-only — passing it positionally silently creates an empty part.

**Variable names in state must match the prompt.** `{user_name?}` in the prompt won't resolve if the state has `first_name`. The key in `state={}` must exactly match the placeholder in the instruction.
