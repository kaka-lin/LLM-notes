"""
ChatGPT-style summary memory + session chat for LiteLLM

Usage:
  export GEMINI_API_KEY="..."  # or GOOGLE_API_KEY depending on your setup
  python3 chat_session.py

Commands:
  /new                    create a new session and switch to it
  /switch <session_id>    switch to an existing session
  /sessions               list sessions
  /clear                  clear current session (messages + summary)
  /exit                   exit
"""

import os
import warnings

from litellm import completion

from utils.session import (
    SessionState,
    load_session,
    save_session,
    new_session,
    list_sessions,
)
from utils.memory import (
    build_messages_for_model,
    maybe_summarize,
)

warnings.filterwarnings(
    "ignore",
    message=r"^Pydantic serializer warnings:.*",
    category=UserWarning,
    module=r"pydantic\.main",
)

# Configuration
# 可以透過環境變數設定使用的模型，預設使用 gemini-2.5-flash
MODEL_CHAT = os.getenv("CHAT_MODEL", "gemini/gemini-2.5-flash")


def chat_once(state: SessionState, user_text: str, model: str = MODEL_CHAT) -> str:
    """
    Executes a single chat turn:
    records user input, checks if memory compression is needed, calls the API, and saves the result.
    """
    # 1. Add user input to memory
    state.messages.append({"role": "user", "content": user_text})

    # 2. Check if memory is too long, and summarize if needed
    maybe_summarize(state)

    # 3. Build prompt for the model (including System Prompt + summary + recent conversation)
    msgs = build_messages_for_model(state)

    # 4. Call LiteLLM for chat
    response = completion(
        model=model,
        messages=msgs,
        temperature=0.4,
    )
    assistant_text = response.choices[0].message.content

    # 5. Add AI response to memory and save current session state to file
    state.messages.append({"role": "assistant", "content": assistant_text})
    save_session(state)
    return assistant_text


def main(model: str = MODEL_CHAT) -> None:
    # Load last session if exists, else create new
    # On startup: try to load the last session, or create a new one if none exists
    sessions = list_sessions()
    state = load_session(sessions[-1]) if sessions else None
    if state is None:
        state = new_session()
        save_session(state)

    print(f"== LiteLLM Chat (model={model}) ==")
    print(f"Session: {state.session_id}")
    print("Type /sessions, /new, /switch <id>, /clear, /exit\n")

    while True:
        try:
            # User input
            user_prompt = input("你說： ")
        except (EOFError, KeyboardInterrupt):
            print("\n聊天結束啦，下次再聊喔！👋")
            break

        if not user_prompt:
            continue

        # Commands
        if user_prompt == "/exit":
            print("\n.聊天結束啦，下次再聊喔！👋")
            break

        if user_prompt == "/sessions":
            sids = list_sessions()
            if not sids:
                print("(no sessions)")
            else:
                print("Sessions:")
                for sid in sids:
                    mark = " *" if sid == state.session_id else ""
                    print(f"  - {sid}{mark}")
            continue

        if user_prompt == "/new":
            state = new_session()
            save_session(state)
            print(f"Switched to new session: {state.session_id}")
            continue

        if user_prompt.startswith("/switch "):
            sid = user_prompt.split(" ", 1)[1].strip()
            loaded = load_session(sid)
            if loaded is None:
                print(f"Session not found: {sid}")
            else:
                state = loaded
                print(f"Switched to session: {state.session_id}")
            continue

        if user_prompt == "/clear":
            state.summary = ""
            state.messages = []
            save_session(state)
            print("Cleared current session memory.")
            continue

        # Normal chat
        ans = chat_once(state, user_prompt, model=model)
        print(f"🤖 助理說： {ans}\n")


if __name__ == "__main__":
    main(MODEL_CHAT)
