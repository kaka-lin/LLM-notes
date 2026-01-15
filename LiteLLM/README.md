# LiteLLM

**LiteLLM** 是一個 **開源 Python 庫與代理（Gateway/Proxy）**，旨在讓開發者用 *統一的介面* 連接並呼叫來自不同 AI 供應商的語言模型（LLM），例如 OpenAI、Anthropic、Google、Azure、HuggingFace 等。

## 核心理念

- **統一 API 接口**：使用類似 OpenAI API 的格式與函式，例如 `completion`、`responses` 或 `embeddings`，即可呼叫不同供應商的模型，而不需逐一學習每個 API 的細節。

- **多模型接入**：支援 `100+` 種大型語言模型，包括雲端與本地模型，讓應用切換模型變得非常輕鬆。

- **簡化整合流程**：自動管理 API Key、錯誤處理、重試/回退邏輯 (fallbacks)、支出追蹤 (spend tracking)、速率限制 (rate limiting)、快取 (caching) 等。

    > 當主要模型不可用時，可自動轉到備援模型，提高系統可靠性。

## 與 LangChain / Ollamv, vLLM 等框架的分工

| 元件 | 定位 | 解決什麼問題 |
|---|---|---|
| LiteLLM | LLM Gateway / SDK | 多模型統一呼叫、routing、fallback、cost / quota |
| LangChain | 應用框架 | RAG、Agent、多步驟流程 |
| Ollama | Local LLM Runtime | 本地快速跑模型、PoC |
| vLLM | Inference Engine | 高吞吐、高併發 GPU 推理 |

### LiteLLM vs LangChain

| 面向 | LiteLLM | LangChain |
|---|---|---|
| 抽象層級 | 低（API / Gateway） | 高（Workflow / App） |
| 管模型切換 | ✅ | ❌ |
| 管成本 / quota | ✅ | ❌ |
| RAG / Agent | ❌ | ✅ |

### 層級關係

```text
[ Client / LangChain / Langflow ]
                ↓
             LiteLLM
   (routing / fallback / cost)
                ↓
        ┌───────────────┐
        │               │
     Ollama           vLLM
 (dev / local)   (prod / high QPS)
```

- LiteLLM **不跑模型**
- Ollama / vLLM **只負責跑模型**

## 範例

```bash
python chat.py
```
