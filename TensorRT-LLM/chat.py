import openai


if __name__ == "__main__":
    client = openai.OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="unused"  # 本地服務不需要 API 金鑰
    )

    response = client.chat.completions.create(
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "你好，簡介一下你自己"}
        ],
        max_tokens=100,
        temperature=0
    )

    # 印出模型的回應
    print(response.choices[0].message.content)
