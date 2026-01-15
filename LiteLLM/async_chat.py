import asyncio
import warnings

import openai
from litellm import acompletion
from litellm.llms.custom_httpx.async_client_cleanup import close_litellm_async_clients

from response_handlers import handle_non_streaming_response, handle_streaming_response_async

warnings.filterwarnings(
    "ignore",
    message=r"^Pydantic serializer warnings:.*",
    category=UserWarning,
    module=r"pydantic\.main",
)

async def async_chat_once(stream: bool = False):
    response = await acompletion(
        model="gemini/gemini-2.5-flash",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Explain LiteLLM in one sentence"}
        ],
        temperature=0.2,
        stream=stream,
    )

    if not stream and (response is None or len(response["choices"]) == 0):
        raise Exception("API Error: No choices in response")

    if stream:
        content, finish_reason = await handle_streaming_response_async(response)
    else:
        content = handle_non_streaming_response(response)

    print(content)


async def main():
    try:
        print("=== 非串流回應 ===")
        await async_chat_once(stream=False)

        print("\n=== 串流回應 ===")
        await async_chat_once(stream=True)
    finally:
        # ✅ 在 event loop 關閉前，手動把 LiteLLM 內部 async clients 關掉
        await close_litellm_async_clients()


if __name__ == "__main__":
    asyncio.run(main())
