import warnings

from litellm import completion


warnings.filterwarnings(
    "ignore",
    message=r"^Pydantic serializer warnings:.*",
    category=UserWarning,
    module=r"pydantic\.main",
)


if __name__ == "__main__":
    # 設定環境變數後，呼叫任意支援的模型

    # 1. 非串流回應
    response = completion(
        model="gemini/gemini-2.5-flash",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Explain LiteLLM in one sentence"}
        ],
    )
    print(response.choices[0].message["content"])

    # 2. 串流回應
    # for chunk in completion(
    #     model="gemini/gemini-2.5-flash",
    #     messages=[{"role": "user", "content": "Summarize LiteLLM briefly"}],
    #     stream=True,
    # ):
    #     delta = chunk["choices"][0]["delta"]
    #     if "content" in delta:
    #         print(delta["content"], end="")
