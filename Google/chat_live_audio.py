import asyncio
from dotenv import load_dotenv

from gemini_agent import GeminiAgent


async def main():
    # 載入 .env 內容到環境變數，並強制更新
    if not load_dotenv(override=True):
        print("警告：.env 檔案不存在或解析失敗，請確認它位於專案根目錄。")

    input_text = "Hello? Gemini are you there?"
    gemini_agent = GeminiAgent(is_live=True)
    await gemini_agent.process(input_text, response_format="audio")


if __name__ == "__main__":
    asyncio.run(main())
