# TensorRT-LLM

> [!NOTE]
> TensorRT-LLM 是一個開源函式庫，用於在 NVIDIA GPU 上加速和優化大型語言模型（LLM）的推理性能。

## 核心功能

- **高效能推理**: 透過 Kernel Fusion、INT4/INT8 量化等技術，實現極致的推理速度。
- **模型支援**: 支援 Llama、GPT-J、Falcon、MPT 等多種主流模型。
- **易於使用**: 提供簡潔的 Python API，方便開發者整合與部署。
- **彈性擴展**: 支援多 GPU 與多節點推理，滿足大規模部署需求。

## 安裝

詳細的安裝與設定指南，請參考：

- **[安裝與設定指南 (Installation Guide)](./installation.md)**

## 快速開始

### 1. 使用 Docker 啟動服務

建議使用官方提供的 Docker 容器來快速設定環境。

```bash
# 從 NVIDIA NGC 拉取 TensorRT-LLM 開發容器
docker run --ipc host --gpus all -it nvcr.io/nvidia/tensorrt-llm/release
```

容器啟動後，您可以直接在容器內使用 `trtllm-serve` 指令來部署模型。

```bash
# 直接傳遞模型名稱，觸發即時編譯並啟動服務
trtllm-serve "TinyLlama/TinyLlama-1.1B-Chat-v1.0" --host 0.0.0.0 --port 8000
```

### 2. 發送請求

服務啟動後，您可以使用 `cURL` 或 Python 的 `openai` 函式庫來發送請求。

1. **使用 cURL**

    ```bash
    curl -X POST http://localhost:8000/v1/chat/completions \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d '{
                "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "你好，簡介一下你自己"}
                ],
                "max_tokens": 100,
                "temperature": 0
            }'
    ```

2. 使用 Python OpenAI 函式庫

    ```bash
    python3
    ```
