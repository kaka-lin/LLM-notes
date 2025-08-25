# 在 Triton 中部署 Hugging Face Llava1.5-7b 模型

使用 Triton Inference Server 結合 TensorRT‑LLM backend，將 Hugging Face 上的 Llava1.5‑7B 模型部署為高效能推論服務

> Llava (Large Language and Vision Assistant) 是一個大型多模態模型 (LMM)，它將視覺編碼器與大型語言模型 (LLM) 結合，實現了基於視覺和語言輸入的通用對話能力。

## Step 1: 下載模型權重

我們需要從 Hugging Face Hub 下載 Llava 1.5-7b 的模型權重。

```bash
git lfs install
git clone https://huggingface.co/llava-hf/llava-1.5-7b-hf
```

## Step 2: 下載官方 `tutorials` repository

這份官方 `tutorials` repository 包含了許多模型的範例設定檔與腳本，其中也包含了我們這次要部署的 Llava 1.5 模型的 Triton Model Repository 模板。後續步驟會使用到這裡面的設定檔。

```bash
git clone https://github.com/triton-inference-server/tutorials.git --branch r25.07
```

## Step 3: 準備 TensorRT-LLM Backend

> [!IMPORTANT]這邊使用版本：25.07
>
> `tensorrtllm_backend` 每一個版本都不一樣需要注意，例如:
> - 25.05: 包含 *all_models*/, *scripts*/ and *tools*/
> - 25.07: 上面已經從 repo 移除，並且都包含在 Docker 中
>
> 所以在後面步驟時需要注意使用的版本來運行相關程式。

```bash
git clone https://github.com/triton-inference-server/tensorrtllm_backend.git --branch r25.07
cd tensorrtllm_backend
apt-get update && apt-get install git-lfs -y --no-install-recommends
git lfs install
git submodule update --init --recursive
```

## Step 4: 啟動 Triton 容器

以 Docker 啟動 Triton Inference Server（包含 TRT‑LLM backend），並掛載必要路徑：

```bash
docker run --rm -it \
  --gpus all \
  --net host --ipc=host \
  --shm-size=2g --ulimit memlock=-1 --ulimit stack=67108864 \
  -e PMIX_MCA_gds=hash \
  -v /path/to/tensorrtllm_backend:/tensorrtllm_backend \
  -v /path/to/Llava-1.5-7b-hf:/llava-1.5-7b-hf \
  -v /path/to/engines:/engines \
  -v /path/to/tutorials:/tutorials \
  nvcr.io/nvidia/tritonserver:25.07-trtllm-python-py3
```

參數說明：

- `-e PMIX_MCA_gds=hash`: 這項參數是為了解決容器內 OpenMPI 的權限與行程間通訊 (IPC) 問題。當遇到 `MPI_Init_thread` 相關錯誤時，設定此環境變數會讓 OpenMPI 的 PMIx 元件改用檔案式的雜湊儲存來取代共享記憶體 (GDS)，從而避開 `/dev/shm` 的權限問題。
- **在容器內以 root 執行 `mpirun`**: 如果您需要在容器內以 `root` 使用者身份執行 `mpirun`（例如，在某些腳本中），Open MPI 預設是不允許的。您需要明確地加上 `--allow-run-as-root` 參數，或是設定環境變數 `OMPI_ALLOW_RUN_AS_ROOT=1` 和 `OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1` 來啟用此權限。


## Step 5: 建立 TensorRT-LLM 引擎

Llava1.5 模型需建立兩種引擎：

- 視覺編碼引擎（visual）
- 語言模型引擎（LLM）

> [!NOTE]
> 建立建立語言模型引擎跟視覺編碼引擎時會重覆覆蓋 `config.json`
> 所以下面我們分成 `llm/` 跟 `vision/` folder

### Step 5.1: 設定環境變數

首先，設定必要的環境變數，方便後續指令使用。

```bash
# 環境變數
HF_LLAVA_MODEL=/llava-1.5-7b-hf
UNIFIED_CKPT_PATH=/tmp/ckpt/llava/7b/
ENGINE_DIR=/engines/llava1.5
LLM_ENGINE_DIR=$ENGINE_DIR/llm
VISION_ENGINE_DIR=$ENGINE_DIR/vision
CONVERT_CHKPT_SCRIPT=/tensorrtllm_backend/tensorrt_llm/examples/models/core/llama/convert_checkpoint.py
```

### Step 5.2: 轉換 HF 權重為 TRT-LLM checkpoint

執行 `convert_checkpoint.py` 腳本，將 Hugging Face 模型權重轉換為 TensorRT-LLM 格式的 checkpoint。

```bash
python3 ${CONVERT_CHKPT_SCRIPT} \
  --model_dir ${HF_LLAVA_MODEL} \
  --output_dir ${UNIFIED_CKPT_PATH} \
  --dtype float16
```

### Step 5.3: 建立語言模型引擎 (TensorRT LLM engine)

使用 `trtllm-build` 指令，基於轉換後的 checkpoint 建立語言模型引擎。

```bash
trtllm-build \
  --checkpoint_dir ${UNIFIED_CKPT_PATH} \
  --output_dir ${LLM_ENGINE_DIR} \
  --gemm_plugin float16 \
  --use_fused_mlp=enable  \
  --max_batch_size 1 \
  --max_input_len 2048 \
  --max_seq_len 2560 \
  --max_multimodal_len 576
```

參數說明：
- `--gemm_plugin float16`: 使用 float16 精度的 GEMM (矩陣乘法) 插件以提升效能。
- `--use_fused_mlp=enable`: 啟用 Fused MLP (多層感知器) 優化，可以減少 GPU kernel 的啟動次數，提升效率。
- `--max_batch_size`: 最大批次大小。
- `--max_input_len`: 輸入序列的最大長度。
- `--max_seq_len`: 整個序列的最大長度。輸入: 2048 + 輸出: 512。
- `--max_multimodal_len`: 多模態輸入（例如圖片特徵）的最大長度。1 (max_batch_size) * 576 (num_multimodal_features) for LLaVA。

### Step 5.4: 建立視覺編碼引擎 (TensorRT visual encoder engine)

執行 `build_multimodal_engine.py` 腳本，建立視覺編碼器引擎。

```bash
python3 /tensorrtllm_backend/tensorrt_llm/examples/models/core/multimodal/build_multimodal_engine.py \
  --model_path ${HF_LLAVA_MODEL} \
  --model_type llava \
  --output_dir ${VISION_ENGINE_DIR}
```

## Step 6: 使用位於相同 llama 範例資料夾中的 run.py 來檢查測試模型的輸出

```bash
python3 /tensorrtllm_backend/tensorrt_llm/examples/models/core/multimodal/run.py \
    --max_new_tokens 30 \
    --hf_model_dir ${HF_LLAVA_MODEL} \
    --engine_dir ${ENGINE_DIR} \
    --image_path=https://storage.googleapis.com/sfr-vision-language-research/LAVIS/assets/merlion.png \
    --input_text "\n Which city is this?" \
    --batch_size=1 # for LLaVA
```

You should expect the following response:

```bash
[TensorRT-LLM] TensorRT-LLM version: 0.20.0
...
[08/25/2025-08:53:26] [TRT-LLM] [I] ---------------------------------------------------------
[08/25/2025-08:53:26] [TRT-LLM] [I]
[Q] ['\n Which city is this?']
[08/25/2025-08:53:26] [TRT-LLM] [I]
[A]: ['This is the city of Singapore.']
[08/25/2025-08:53:26] [TRT-LLM] [I] Generated 7 tokens
[08/25/2025-08:53:26] [TRT-LLM] [I] ---------------------------------------------------------
```

## Step 7: 設定 Triton Model Repository

`Triton Model Repository` 是一個特定結構的資料夾，`Triton Inference Server` 會從中讀取模型並提供服務。每個模型都有自己的子資料夾，裡面包含設定檔 (`config.pbtxt`) 和模型權重。

在這個步驟中，我們使用 `tensorrtllm_backend` 提供的 `fill_template.py` 腳本，來自動填寫 `config.pbtxt` 的模板。這個模板則來自於我們在 Step 2 從 NVIDIA Triton 官方下載的 `tutorials` 範例庫。

```bash
FILL_TEMPLATE_SCRIPT=/tensorrtllm_backend/tools/fill_template.py
python3 ${FILL_TEMPLATE_SCRIPT} \
  -i /tutorials/Popular_Models_Guide/Llava1.5/model_repository/tensorrt_llm/config.pbtxt \
  engine_dir:${ENGINE_DIR}
```

> [!NOTE]
> **關於 Ensemble 模型**
>
> `ensemble` 是 Triton 的一種進階功能，它允許將多個模型串聯成一個 pipeline。對於 Llava 這種多模態模型，理論上也可以使用 ensemble 來實現：
> 1.  **預處理模型 (Preprocessing)**：接收圖片和文字，將它們轉換為特徵向量。
> 2.  **視覺編碼模型 (Vision Encoder)**：處理圖片特徵。
> 3.  **語言模型 (LLM)**：結合文字與圖片特徵，生成最終結果。
>
> 不過，在這個範例中已經將這個複雜的流程整合在單一模型中處理，因此我們不需要手動設定 ensemble。我們只需要準備好 `tensorrt_llm` 格式的模型，Triton 就會自動處理前處理與模型的呼叫。

## Step 8: 啟動 Triton 伺服器

準備好模型儲存庫後，我們就可以啟動 Triton 推理伺服器了。

### Step 8.1: 設定環境變數，並啟動 Triton 伺服器

首先，設定必要的環境變數，並執行官方提供的啟動腳本。

```bash
# 設定環境變數
# TRT_ENGINE_LOCATION 指的是「視覺編碼器（vision）那顆 TensorRT 引擎」的檔案路徑
export TRT_ENGINE_LOCATION="/engines/llava1.5/vision/model.engine"
export HF_LOCATION="/llava-1.5-7b-hf"

# 執行啟動腳本
# --world_size=1: 指定使用單一 GPU
# --model_repo: 指定 Triton Model Repository 的路徑
python3 /app/scripts/launch_triton_server.py \
  --world_size=1 \
  --model_repo=/tutorials/Popular_Models_Guide/Llava1.5/model_repository
```

執行此命令後，伺服器很可能會因為版本不同缺少參數而啟動失敗。請觀察終端機的錯誤訊息，並參考下面的步驟來逐一修復設定檔。

### Step 8.2: 修改 `config.pbtxt` 以符合新版後端要求

接下來的幾個子步驟，都是為了解決啟動失敗的問題。您需要手動編輯位於 `/tutorials/Popular_Models_Guide/Llava1.5/model_repository/` 中的 `tensorrt_llm/config.pbtxt` 及 `llava-1.5/config.txt` 的檔案，在 `parameters` 區塊中加入對應的設定。

#### 8.2.1: 新增 `tokenizer_dir`

- **問題**: TensorRT-LLM 後端需要明確知道 Tokenizer 的路徑才能將模型輸出的 ID 轉換回文字 (detokenize)，但教學範本的設定檔中缺少此項。
- **解決方案**: 在 `tensorrt_llm/config.pbtxt` 中加入 `tokenizer_dir` 參數，並將其指向 Hugging Face 模型的目錄。

    ```pbtxt
    parameters: {
      key: "tokenizer_dir"
        value: {
          string_value: "/llava-1.5-7b-hf"
        }
    }
    ```

#### 8.2.2: 新增 `xgrammar` 相關參數

- **問題**: 25.05 版之後的 TensorRT-LLM 後端導入了 `XGrammar` 功能（用於限制生成文法），即使不使用，引擎在初始化時也會檢查相關參數，缺少就會報錯。
- **解決方案**: 在 `tensorrt_llm/config.pbtxt` 中補上這兩個參數，並給予空字串值來表示關閉此功能。

    ```pbtxt
    parameters: {
      key: "xgrammar_tokenizer_info_path"
        value: {
          string_value: ""
        }
    }
    parameters: {
      key: "xgrammar_tokenizer_merge_path"
        value: {
          string_value: ""
        }
    }
    ```

#### 8.2.3: 新增 `guided_decoding_backend`

- **問題**: 新版本的後端強制要求設定 `guided_decoding_backend` 參數，舊的設定檔沒有這個參數，導致載入失敗。
- **解決方案**: 在 `tensorrt_llm/config.pbtxt` 中新增此參數並設為 `"none"`，表示不使用 guided decoding 功能，以符合 LLaVA 教學範本的原始設定。

    ```pbtxt
    parameters: {
      key: "guided_decoding_backend"
        value: {
          string_value: "none"
        }
    }
    ```

#### 8.2.4: 關閉 `enable_kv_cache_reuse`

- **問題**: 新版後端預設可能開啟了 KV cache reuse 功能以提升效能，但此功能要求請求中必須包含 `prompt_table_extra_ids` 欄位。教學範本的 Python 客戶端腳本沒有產生這個欄位，導致請求驗證失敗。
- **解決方案**: 為了讓教學範本能順利執行，最直接的方法是在 `tensorrt_llm/config.pbtxt` 中明確地關閉此功能。

    ```pbtxt
    parameters: {
      key: "enable_kv_cache_reuse"
        value: {
          string_value: "false"
        }
    }
    ```
    > **注意**: 若未來有效能需求，想重新開啟此功能，則不能使用教學中的簡易版 Python 腳本，而需要修改客戶端程式碼或改用更完整的 `ensemble` 流程。

#### 8.2.5: 關閉 `decoupled` 模式以支援 HTTP/Curl

- **問題**: 當使用 `curl` 或透過 HTTP 發送請求時，可能會遇到 `HTTP end point doesn't support models with decoupled transaction policy` 的錯誤。這是因為 `llava-1.5` Python 後端模型的 `config.pbtxt` 預設啟用了 `decoupled` 模式，但 HTTP 端點不支援此模式。
- **解決方案**: 如果您需要使用 `curl` 或 HTTP 客戶端進行測試，需要手動關閉 `decoupled` 模式。請編輯 `llava-1.5/config.pbtxt` 檔案，修改或加入以下設定：

    ```pbtxt
    model_transaction_policy {
        decoupled: false
    }
    ```

### Step 8.3: 確認伺服器成功啟動

在修改完 `config.pbtxt` 後，請重新執行 Step 8.1 的啟動命令。重複此過程，直到所有必要的參數都已補全。當您在終端機看到以下訊息時，代表 Triton 伺服器已成功啟動並準備好接收推論請求：

```bash
...
I0825 09:05:40.721822 6320 grpc_server.cc:2562] "Started GRPCInferenceService at 0.0.0.0:8001"
I0825 09:05:40.722228 6320 http_server.cc:4789] "Started HTTPService at 0.0.0.0:8000"
I0825 09:05:40.798049 6320 http_server.cc:358] "Started Metrics Service at 0.0.0.0:8002"
```

若要停止容器內的 Triton Server，可以執行：

```bash
pkill tritonserver
```

## Step 9: 執行推論

伺服器啟動後，我們可以發送請求來進行推論，這邊有下面幾種方法。

### 1. Python 客戶端

```python
import requests
import json

# 準備請求的 payload
data = {
    "prompt": "USER: <image>\nQuestion: which city is this? Answer:",
    "image": "https://storage.googleapis.com/sfr-vision-language-research/LAVIS/assets/merlion.png",
    "max_tokens": 64,
    "temperature": 0.0,
    "top_k": 1,
    "frequency_penalty": 0.0,
    "seed": 0
}

# 發送 POST 請求
response = requests.post("http://localhost:8000/v2/models/llava-1.5/generate", json=data)

# 輸出結果
print(response.json())
```

You should expect the following response:

```bash
{'completion_tokens': 1, 'finish_reason': 'stop', 'model_name': 'llava-1.5', 'model_version': '1', 'prompt_tokens': 592, 'text': 'Singapore', 'total_tokens': 593}
```

### 2. Curl

```bash
curl -s -X POST http://localhost:8000/v2/models/llava-1.5/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "USER: <image>\nQuestion: which city is this? Answer:",
    "image": "https://storage.googleapis.com/sfr-vision-language-research/LAVIS/assets/merlion.png",
    "max_tokens": 64,
    "temperature": 0.0,
    "top_k": 1,
    "frequency_penalty": 0.0,
    "seed": 0
  }'
```

You should expect the following response:

```bash
{"completion_tokens":1,"finish_reason":"stop","model_name":"llava-1.5","model_version":"1","prompt_tokens":592,"text":"Singapore","total_tokens":593}
