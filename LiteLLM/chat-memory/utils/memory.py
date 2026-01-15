import os
from typing import List, Tuple

from litellm import completion

from .session import SessionState, Message

# How many recent turns to keep verbatim (user+assistant pairs)
RECENT_TURNS_TO_KEEP = int(os.getenv("RECENT_TURNS_TO_KEEP", "8"))

# When messages get "too big", we summarize older ones.
# (Token counting varies by model/provider; use a simple char threshold.)
SUMMARIZE_CHAR_THRESHOLD = int(os.getenv("SUMMARIZE_CHAR_THRESHOLD", "8000"))

# Model for summarization
MODEL_SUMMARY = os.getenv("SUMMARY_MODEL", "gemini/gemini-2.5-flash")

# Base system prompt
SYSTEM_BASE = os.getenv(
    "SYSTEM_PROMPT",
    "You are a helpful assistant. Be concise but accurate."
)


# Memory management
def build_messages_for_model(state: SessionState, system_base: str = SYSTEM_BASE) -> List[Message]:
    """
    Construct prompt with:
      system = base system prompt + optional summary memory
      then recent conversation messages (trimmed)
    """
    sys = system_base
    if state.summary.strip():
        # 如果有摘要 (Summary)，將其附加到 System Prompt 中
        # 這樣模型就能「記得」之前的對話重點，即使原本的訊息已經被移除了
        sys += "\n\n# Conversation Memory (summary)\n" + state.summary.strip()

    msgs: List[Message] = [{"role": "system", "content": sys}]
    msgs.extend(state.messages)
    return msgs


def estimate_size_chars(messages: List[Message]) -> int:
    return sum(len(m.get("content", "")) for m in messages)


def keep_recent_turns(messages: List[Message], turns_to_keep: int = RECENT_TURNS_TO_KEEP) -> Tuple[List[Message], List[Message]]:
    """
    Keep last N turns (user+assistant pairs) from the end.
    Return (older, recent)
    """
    if turns_to_keep <= 0:
        return (messages, [])

    # 我們將 "一輪 (turn)" 定義為一組 (User + Assistant) 的對話。
    # 所以如果要保留 N 輪，大概就是保留最後 2*N 則訊息。
    keep_n = turns_to_keep * 2
    if len(messages) <= keep_n:
        # 如果訊息總數還沒超過要保留的數量，就不需要切割
        return ([], messages)

    # older: 比較舊的訊息，這些會被拿去壓縮成摘要
    older = messages[:-keep_n]
    # recent: 最近的訊息，這些會原封不動地保留在對話紀錄中，保持對話流暢度
    recent = messages[-keep_n:]
    return (older, recent)


def summarize_older_messages(
    state: SessionState,
    turns_to_keep: int = RECENT_TURNS_TO_KEEP,
    model_summary: str = MODEL_SUMMARY
) -> None:
    """
    Summarize older messages into state.summary,
    keeping only recent turns verbatim.
    """
    # 1. 將訊息切分為「舊訊息 (older)」與「近期訊息 (recent)」
    # 我們只對「舊訊息」進行摘要壓縮
    older, recent = keep_recent_turns(state.messages, turns_to_keep)
    if not older:
        return

    # 2. 準備摘要用的 Prompt
    # 我們告訴模型：請把「現有的摘要」加上「這些舊訊息」，合併成一個「新的摘要」。
    existing = state.summary.strip()
    # 將舊訊息格式化為文字字串
    older_text = "\n".join([f'{m["role"]}: {m["content"]}' for m in older])

    prompt = [
        {
            "role": "system",
            "content": (
                "You are a memory summarizer for a chat assistant.\n"
                "Goal: write a compact, factual summary of the conversation so far.\n"
                "Rules:\n"
                "- Keep stable user preferences, constraints, decisions, definitions.\n"
                "- Keep important context needed to continue the chat.\n"
                "- Remove chit-chat and redundant phrasing.\n"
                "- Use bullet points. Keep it short.\n"
                "- Do NOT invent facts.\n"
            ),
        },
        {
            "role": "user",
            "content": (
                f"Existing summary (may be empty):\n{existing if existing else '(empty)'}\n\n"
                f"Older conversation messages to compress:\n{older_text}\n\n"
                "Return the updated summary only."
            ),
        },
    ]

    response = completion(
        model=model_summary,
        messages=prompt,
        temperature=0.2,
    )
    new_summary = response.choices[0].message.content.strip()

    state.summary = new_summary
    state.messages = recent


def maybe_summarize(
    state: SessionState,
    system_base: str = SYSTEM_BASE,
    summarize_char_threshold: int = SUMMARIZE_CHAR_THRESHOLD,
) -> None:
    """
    Trigger summarization based on size heuristic.
    """
    # 為了判斷是否需要摘要，我們先估算一下目前所有內容 (System Prompt + 摘要 + 對話歷史) 的總長度
    msgs_for_size = [{"role": "system", "content": system_base + "\n" + state.summary}] + state.messages

    # 如果總字數超過設定的閾值 (預設 8000 字元)，就觸發摘要機制
    if estimate_size_chars(msgs_for_size) >= summarize_char_threshold:
        summarize_older_messages(state)
