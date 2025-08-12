# TensorRT-LLM 安裝與設定

> [!NOTE]
> TensorRT-LLM 是一個開源函式庫，用於在 NVIDIA GPU 上加速和優化大型語言模型（LLM）的推理性能。

## 安裝方式

您可以選擇透過 Pip (Linux) 或 Docker 來安裝 TensorRT-LLM。

### 1. 使用 Pip (Linux)

> [!IMPORTANT]
> 需要 Python 3.10 或更高版本。

在透過 `pip` 安裝之前，必須先完成以下前置作業：

1. **安裝 CUDA Toolkit**:
    請參考 [CUDA Installation Guide for Linux](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html) 進行安裝，並確保 `CUDA_HOME` 環境變數已正確設定。

2. **安裝 Open MPI**:
    ```bash
    sudo apt-get -y install libopenmpi-dev
    ```

3. **安裝 PyTorch (NVIDIA Blackwell GPUs & SBSA 平台可選)**:
    若您使用 NVIDIA Blackwell 系列 GPU 或 SBSA 平台，需要安裝特定的 PyTorch 版本。
    ```bash
    pip3 install torch==2.7.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
    ```

完成上述步驟後，即可安裝 TensorRT-LLM：

```bash
# 安裝 TensorRT-LLM
pip3 install --upgrade pip setuptools && pip3 install tensorrt_llm
```

### 2. 使用 Docker (推薦)

建議使用官方提供的 Docker 容器來快速設定環境，這是最簡單且最不容易出錯的方式。

```bash
# 從 NVIDIA NGC 拉取 TensorRT-LLM 開發容器
docker run --ipc host --gpus all -it nvcr.io/nvidia/tensorrt-llm/release
```

## 使用範例

### 1. Run Offline inference with LLM API

這個範例展示如何在 Python 中直接使用 TensorRT-LLM 進行推理。

```python
from tensorrt_llm import LLM, SamplingParams


def main():

    # Model could accept HF model name, a path to local HF model,
    # or TensorRT Model Optimizer's quantized checkpoints like nvidia/Llama-3.1-8B-Instruct-FP8 on HF.
    llm = LLM(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

    # Sample prompts.
    prompts = [
        "Hello, my name is",
        "The capital of France is",
        "The future of AI is",
    ]

    # Create a sampling params.
    sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

    for output in llm.generate(prompts, sampling_params):
        print(
            f"Prompt: {output.prompt!r}, Generated text: {output.outputs[0].text!r}"
        )

    # Got output like
    # Prompt: 'Hello, my name is', Generated text: '\n\nJane Smith. I am a student pursuing my degree in Computer Science at [university]. I enjoy learning new things, especially technology and programming'
    # Prompt: 'The president of the United States is', Generated text: 'likely to nominate a new Supreme Court justice to fill the seat vacated by the death of Antonin Scalia. The Senate should vote to confirm the'
    # Prompt: 'The capital of France is', Generated text: 'Paris.'
    # Prompt: 'The future of AI is', Generated text: 'an exciting time for us. We are constantly researching, developing, and improving our platform to create the most advanced and efficient model available. We are'


if __name__ == '__main__':
    main()
```

### 2. Deploy online serving with `trtllm-serve`

`trtllm-serve` 是一個基於 FastAPI 的高效能服務，讓您可以將 TensorRT-LLM 編譯後的模型部署為一個符合 OpenAI API 標準的線上服務。

> [!TIP]
> `trtllm-serve` 提供了豐富的設定選項，例如 `--host`、`--port` 等，您可以透過 `trtllm-serve --help` 來查看所有可用的參數。

#### 步驟 1: 編譯模型 (手動)

雖然 `trtllm-serve` 的即時編譯功能非常方便，但在某些情況下，您可能需要手動使用 `trtllm build` 指令來獲得更多控制權，例如：

- **精確控制量化**: 套用 INT8 或 INT4 量化以追求極致效能。
- **調整引擎參數**: 設定最大批次大小 (`--max_batch_size`)、最大輸入/輸出長度等。
- **離線環境部署**: 在沒有網路連線的環境中部署模型。

**基本用法**

```bash
# 將 TinyLlama 模型編譯成 FP16 格式的 TensorRT 引擎
# --output 指定編譯後引擎的儲存目錄
trtllm build --model_name "TinyLlama/TinyLlama-1.1B-Chat-v1.0" \
             --output ./tinyllama_engine \
             --dtype float16
```

**進階用法：INT8 量化**

```bash
# 使用 INT8-SmoothQuant 量化
trtllm build --model_name "TinyLlama/TinyLlama-1.1B-Chat-v1.0" \
             --output ./tinyllama_engine_int8 \
             --quant_mode int8_sq
```

> [!NOTE]
> `trtllm build` 指令會從 Hugging Face Hub 下載模型並進行編譯。編譯過程可能需要一些時間，具體取決於模型大小和您的硬體規格。手動編譯產生的引擎目錄可以被 `trtllm-serve --model <engine_dir>` 指令重複使用。

#### 步驟 2: 啟動服務

模型編譯完成後，您可以使用 `trtllm-serve` 指令來啟動 API 伺服器。

**方法一：使用已編譯的引擎**

如果已手動執行 `trtllm build`，可以將產生的引擎目錄路徑傳遞給 `trtllm-serve`：
```bash
# 將預先編譯好的引擎目錄傳遞給 trtllm-serve
trtllm-serve --model ./tinyllama_engine
```

**方法二：使用 Hugging Face 模型與即時編譯 (推薦)**

是的，`trtllm-serve` 支援**即時編譯 (Just-In-Time, JIT)**。您可以直接將 Hugging Face 的模型名稱作為參數傳遞給它。伺服器在首次啟動時會自動在背景執行下載、轉換和編譯，然後將產生的 TensorRT 引擎快取起來供後續使用。

這種方式極大地簡化了部署流程。

```bash
# 直接傳遞模型名稱，觸發即時編譯
trtllm-serve "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# 或是改變 host 跟 port
trtllm-serve "TinyLlama/TinyLlama-1.1B-Chat-v1.0" --host 0.0.0.0 --port 8000
```

<details>
<summary>點此展開/折疊即時編譯的日誌範例</summary>

```log
# 首次執行時，伺服器會依序進行三個步驟：下載、載入、編譯
Loading Model: [1/3]    Downloading HF model
...
Downloaded model to /root/.cache/huggingface/hub/models--TinyLlama--TinyLlama-1.1B-Chat-v1.0/snapshots/...
Time: 319.334s

Loading Model: [2/3]    Loading HF model to memory
[08/12/2025-07:26:13] [TRT-LLM] [I] Specified dtype 'auto'; inferred dtype 'bfloat16'.
...
Time: 0.559s

Loading Model: [3/3]    Building TRT-LLM engine
[08/12/2025-07:26:13] [TRT-LLM] [I] Set paged_kv_cache to True.
...
[08/12/2025-07:27:49] [TRT-LLM] [I] Timing cache serialized to model.cache
Time: 98.972s

Loading model done.
Total latency: 418.866s
```
</details>

此指令會在本地的 `http://localhost:8000` 啟動一個 API 服務。

#### 步驟 3: 發送請求

服務啟動後，您可以透過以下兩種主要方式與模型互動。

1. **方法一：使用 cURL (命令列)**

    `cURL` 是在終端機中測試 API 最直接的方式。

    > [!NOTE]
    > `trtllm-serve` 支援 `/v1/chat/completions` 端點，建議優先使用。

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

2. **方法二：使用 Python OpenAI 函式庫**

    > [!IMPORTANT]
    > 此時他就是 local 端的 OpenAI。

   1. **安裝函式庫**:
       ```bash
       pip install openai
       ```

   2. **Python 程式**:
        ```python
        import openai

        # 建立一個客戶端，指向本地運行的 trtllm-serve
        client = openai.OpenAI(
            base_url="http://localhost:8000/v1",
            api_key="unused"  # 本地服務不需要 API 金鑰
        )

        # 使用 chat.completions.create 方法發送請求
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
        ```
