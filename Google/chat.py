from dotenv import load_dotenv
from gemini_agent import GeminiAgent


if __name__ == "__main__":
    # 載入 .env 內容到環境變數，並強制更新
    if not load_dotenv(override=True):
        print("警告：.env 檔案不存在或解析失敗，請確認它位於專案根目錄。")

    gemini_agent = GeminiAgent()
    input_text = "你好，簡介一下你自己"
    response = gemini_agent.process(input_text)
    print("問題: ", input_text)
    print("回答: ", response)
