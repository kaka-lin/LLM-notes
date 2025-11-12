# vLLM

vLLM 是一個由 UC Berkeley 開發的開源函式庫，專為提升大型語言模型（LLM）的吞吐量與推理性能而設計。它透過 `PagedAttention` 等創新技術，顯著提高了 LLM 服務的吞吐量（Throughput）。特別適合在服務端部署 GPT、LLaMA、Mistral 等模型時使用。

## 核心功能

- **PagedAttention**:
  - vLLM 的核心創新是 `PagedAttention` 技術，讓注意力機制像作業系統的虛擬記憶體分頁一樣管理 GPU 記憶體。
  - 能夠高效管理 `Key-Value Cache`，避免記憶體碎片化，並支援同時處理大量請求。
- **高吞吐量推理**:
  - 相比 HuggingFace Transformers，vLLM 的吞吐量提升 2-4 倍。
  - 可以支援 數千個並發請求，特別適合 ChatGPT 類似的多使用者場景。
- **連續批次處理 (Continuous Batching)**:
  - 自動將多個請求動態組合成一個批次進行推理，優化 GPU 利用率。
- **模型支援**: 支援 Llama、Mixtral、GPT-2、Mistral 等多種主流模型。
- **易於使用**: 提供與 OpenAI 相容的 API 伺服器，方便開發者快速整合與部署。如:
  - /v1/completions
  - /v1/chat/completions。
- **分散式推理**: 支援 `Tensor Parallelism，`可將單一模型分散到多個 GPU 上運行。

## 快速使用

### 1. 安裝

您可以透過 `pip` 快速安裝 vLLM。

```bash
pip install vllm
```

### 2. 啟動 API 伺服器

安裝完成後，您可以使用一行指令啟動與 OpenAI 相容的 API 伺服器。

```bash
python -m vllm.entrypoints.openai.api_server \
    --model openai/gpt-oss-20b
```

or

```bash
vllm serve openai/gpt-oss-20b
```

### 3. 發送請求

服務啟動後，您可以使用 `cURL` 或 Python 的 `openai` 函式庫來發送請求。

1. **使用 cURL**

    ```bash
    curl http://localhost:8000/v1/chat/completions \
        -H "Content-Type: application/json" \
        -d '{
            "model": "openai/gpt-oss-20b",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "你好，簡介一下你自己"}
            ],
            "max_tokens": 1024,
            "temperature": 0
        }'
    ```

    You should expect the following response:

    ```bash
    {
    "id": "chatcmpl-9fe1f37594a34139b588697716c29778",
    "object": "chat.completion",
    "created": 1756202889,
    "model": "openai/gpt-oss-20b",
    "choices": [
        {
        "index": 0,
        "message": {
            "role": "assistant",
            "content": "你好！我是 ChatGPT，一個由 OpenAI 訓練的大型語言模型。我的主要功能是理解並生成自然語言，能夠協助你完成各種文字相關的任務，例如：\n\n- 回答問題、提供資訊\n- 撰寫、修改或校對文章、報告、信件\n- 進行翻譯、語言學習輔導\n- 創作故事、詩歌、對話腳本\n- 幫助編程、解釋程式碼\n- 提供學習、研究、工作上的建議\n\n我能使用多種語言（包括中文、英文、日文、法文等），並且能根據你的需求調整語氣、風格或深度。雖然我盡力提供準確且有用的資訊，但我並非專業人士，對於醫療、法律、財務等專業領域的建議，還是建議你諮詢相關專家。\n\n如果你有任何問題或需要協助，隨時告訴我！",
            "refusal": null,
            "annotations": null,
            "audio": null,
            "function_call": null,
            "tool_calls": [],
            "reasoning_content": "The user says in Chinese: \"你好，簡介一下你自己\" meaning \"Hello, introduce yourself briefly.\" So we need to respond in Chinese, presumably. The assistant is ChatGPT. We should give a brief introduction: name, capabilities, etc. Should be friendly."
        },
    ...
    }
    ```

2. **使用 Python OpenAI 函式庫**

    ```python
    import openai

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

    print(response.choices[0].message.content)
    ```

    You should expect the following response:

    ```bash
    你好！我是 ChatGPT，一個由 OpenAI 訓練的大型語言模型。我的主要功能是理解並生成自然語言，能夠協助你完成各種文字相關的任務，例如：

    - 回答問題、提供資訊
    - 撰寫、修改或校對文章、報告、信件
    - 進行翻譯、語言學習輔導
    - 創作故事、詩歌、對話腳本
    - 幫助編程、解釋程式碼
    - 提供學習、研究、工作上的建議

    我能使用多種語言（包括中文、英文、日文、法文等），並且能根據你的需求調整語氣、風格或深度。雖然我盡力提供準確且有用的資訊，但我並非專業人士，對於醫療、法律、財務等專業領域的建議，還是建議你諮詢相關專家。

    如果你有任何問題或需要協助，隨時告訴我！
    ```

### 4. 更多模型範例

如果您想了解如何使用 vLLM 運行其他特定模型（例如：DeepSeek, Gemma），請參考 [`Recipes/`](./Recipes/) 資料夾中對應的社群貢獻指南。
