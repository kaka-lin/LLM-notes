import openai


def handle_non_streaming_response(response) -> str:
    """處理非串流回應，回傳完整文字內容"""
    # dict (OpenAI-like)
    if isinstance(response, dict):
        return response["choices"][0]["message"]["content"]
    # pydantic object
    return response.choices[0].message.content


def handle_streaming_response(response) -> str:
    """處理串流回應，逐步輸出並回傳完整文字內容"""
    full_response = ""
    finish_reason = None

    try:
        for chunk in response:
            if chunk.choices and len(chunk.choices) > 0:
                choice = chunk.choices[0]
                delta = choice.delta
                content = getattr(delta, 'content', None)
                if content:
                    full_response += content
                if choice.finish_reason:
                    finish_reason = choice.finish_reason
    except Exception as e:
        print(f"\n[Error handling streaming response]: {e}")
        raise

    if not full_response and finish_reason is None:
        print("\n[Warning] Streaming response resulted in empty content with no finish reason")
        raise openai.APIError("Empty streaming response received without proper completion")
    elif not full_response and finish_reason:
        print(f"\n[Debug] Streaming response resulted in empty content but completed with finish_reason: {finish_reason}")
        raise openai.APIError(f"Streaming response completed with finish_reason '{finish_reason}' but no content received")

    return full_response, finish_reason


async def handle_streaming_response_async(response) -> str:
    """處理串流回應，逐步輸出並回傳完整文字內容"""
    full_response = ""
    finish_reason = None

    try:
        async for chunk in response:
            if chunk.choices and len(chunk.choices) > 0:
                choice = chunk.choices[0]
                delta = choice.delta
                content = getattr(delta, 'content', None)
                if content:
                    full_response += content
                if choice.finish_reason:
                    finish_reason = choice.finish_reason
    except Exception as e:
        print(f"\n[Error handling streaming response]: {e}")
        raise

    if not full_response and finish_reason is None:
        print("\n[Warning] Streaming response resulted in empty content with no finish reason")
        raise openai.APIError("Empty streaming response received without proper completion")
    elif not full_response and finish_reason:
        print(f"\n[Debug] Streaming response resulted in empty content but completed with finish_reason: {finish_reason}")
        raise openai.APIError(f"Streaming response completed with finish_reason '{finish_reason}' but no content received")

    return full_response, finish_reason

