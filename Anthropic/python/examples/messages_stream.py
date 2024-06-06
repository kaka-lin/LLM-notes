import os

import anthropic
import base64
import httpx


if __name__ == "__main__":
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(
        # 預設為 os.environ.get("ANTHROPIC_API_KEY")
        api_key=api_key
    )

    # Message
    with client.messages.stream(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello, Claude"}],
        model="claude-3-opus-20240229",
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
