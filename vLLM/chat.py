import openai


if __name__ == "__main__":
    # 修改 base_url 指向本地運行的 vLLM 伺服器
    client = openai.OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="vllm"  # 本地服務不需要 API 金鑰
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "你好，簡介一下你自己"}
        ],
        max_tokens=1024,
        temperature=0
    )

    # 印出模型的回應
    print(response.choices[0].message.content)
