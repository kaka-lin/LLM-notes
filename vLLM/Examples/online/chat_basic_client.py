from openai import OpenAI


def main():
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="unused",  # 本地服務不需要 API 金鑰
    )

    response = client.chat.completions.create(
        model="google/gemma-3-4b-it",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "簡單介紹一下 vLLM 是什麼，以及它適合做什麼？"},
        ],
        max_tokens=100,
        temperature=0.3,
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
