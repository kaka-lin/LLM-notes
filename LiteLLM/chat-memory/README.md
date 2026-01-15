# LiteLLM Chat Memory

這是一個基於 [LiteLLM](https://github.com/BerriAI/litellm) 構建的 CLI 聊天應用程式，具備 **長短期記憶管理 (Long-term Memory)** 功能。

當對話長度超過設定閾值時，系統會自動將舊的對話內容進行摘要壓縮，並儲存到 System Prompt 中，讓 AI 能夠在不超過 Token 限制的情況下「記得」之前的對話重點。

## 🚀 特色功能

*   **自動摘要記憶**：使用滾動式摘要機制 (Rolling Summary)，保留對話關鍵資訊。
*   **多重對話 Session**：可以建立、切換、列出多個獨立的對話 Session。
*   **持久化儲存**：對話紀錄與摘要會以 JSON 格式儲存在本地端，重啟後可繼續對話。
*   **模型彈性**：支援 LiteLLM 支援的所有模型 (Gemini, GPT-4, Claude 等)。

## 📦 安裝需求

確保您已安裝 Python 3.9+。

1.  安裝相依套件：

    ```bash
    pip install litellm
    ```

## ⚙️ 設定環境變數

在執行之前，您需要設定 API Key 以及相關參數。

### 必要設定

根據您使用的模型設定對應的 API Key。範例使用 Google Gemini：

```bash
export GEMINI_API_KEY="your_api_key_here"
```

*(如果您使用 OpenAI，則設定 `OPENAI_API_KEY`，依此類推)*

### 進階設定 (可選)

您可以透過以下環境變數自定義行為：

| 變數名稱 | 預設值 | 說明 |
| :--- | :--- | :--- |
| `CHAT_MODEL` | `gemini/gemini-2.5-flash` | 對話使用的主要模型 |
| `SUMMARY_MODEL` | 同 `CHAT_MODEL` | 用於執行摘要任務的模型 |
| `CHAT_DATA_DIR` | `./.chat_sessions` | 對話紀錄儲存的資料夾路徑 |
| `RECENT_TURNS_TO_KEEP` | `8` | 保留完整對話的輪數 (一輪 = User + AI) |
| `SUMMARIZE_CHAR_THRESHOLD` | `8000` | 觸發摘要壓縮的字元數閾值 |
| `SYSTEM_PROMPT` | "You are a helpful..." | 系統提示詞 (System Prompt) |

## ▶️ 如何使用

1.  **啟動程式**：

    ```bash
    python chat_memory.py
    ```

    *啟動時會自動載入最後一次的 Session，若無則建立新的。*

2.  **聊天介面指令**：

    *   `/new`: 建立一個全新的對話 Session。
    *   `/sessions`: 列出所有已存檔的 Session ID。
    *   `/switch <session_id>`: 切換到指定的 Session。
    *   `/clear`: 清空當前 Session 的所有記憶與對話。
    *   `/exit`: 結束程式。


## 🧠 記憶運作原理

1.  **短期記憶**：系統會保留最近 `RECENT_TURNS_TO_KEEP` 輪的完整對話。
2.  **長期記憶**：當總訊息長度超過 `SUMMARIZE_CHAR_THRESHOLD` 時，系統會啟動「摘要代理」。
3.  **摘要合併**：舊的完整對話會被壓縮成條列式的摘要，並與現有的摘要合併。
4.  **注入 Context**：新的摘要會被插入到 System Prompt 中，作為 AI 的背景知識。
