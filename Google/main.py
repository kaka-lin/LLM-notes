import asyncio
from dotenv import load_dotenv

from gemini_agent import GeminiAgent


async def main():
    # 載入 .env 內容到環境變數，並強制更新
    if not load_dotenv(override=True):
        print("警告：.env 檔案不存在或解析失敗，請確認它位於專案根目錄。")

    gemini_agent = GeminiAgent()

    # 用法 1: 非同步對話
    input_text = "你好，簡介一下你自己"
    response = gemini_agent.process(
        input_text, mode="chat", is_live=False, response_format="text"
    )
    print("問題: ", input_text)
    print("回答: ", response)

    # 用法 2: live 對話
    input_text = "Hello? Gemini are you there?"
    await gemini_agent.process(
        input_text, mode="chat", is_live=True, response_format="text"
    )

    # 用法 3: live 對話，回傳音檔
    input_text = "Hello? Gemini are you there?"
    await gemini_agent.process(
        input_text, mode="chat", is_live=True, response_format="audio"
    )

    # 用法 4: live 語音轉文字
    result_text = await gemini_agent.process(
        "test.mp3", mode="asr", is_live=True, response_format="text"
    )
    print("ASR 結果: ", result_text)

if __name__ == "__main__":
    asyncio.run(main())
