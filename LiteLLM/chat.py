import warnings

from litellm import completion

from response_handlers import handle_non_streaming_response, handle_streaming_response

warnings.filterwarnings(
    "ignore",
    message=r"^Pydantic serializer warnings:.*",
    category=UserWarning,
    module=r"pydantic\.main",
)


def chat_once(stream: bool = False):
    response = completion(
        model="gemini/gemini-2.5-flash",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Explain LiteLLM in one sentence"}
        ],
        stream=stream,
    )

    if not stream and (response is None or len(response["choices"]) == 0):
        raise Exception("API Error: No choices in response")

    if stream:
        content, finish_reason = handle_streaming_response(response)
    else:
        content = handle_non_streaming_response(response)

    print(content)


def main():
    print("=== 非串流回應 ===")
    chat_once(stream=False)

    print("\n=== 串流回應 ===")
    chat_once(stream=True)


if __name__ == "__main__":
    main()
