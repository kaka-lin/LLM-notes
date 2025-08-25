# Triton Inference Server 介紹

> [!IMPORTANT]
> 版號說明[請點我](#版本號說明-versioning)

NVIDIA Triton Inference Server（前身為 TensorRT Inference Server）是一個專門用來部署 AI 模型的開源推論伺服器，能夠在 `CPU` 或 `GPU` 上同時服務多個不同框架的模型。它的主要目標是簡化 AI 模型到生產環境的落地，支援高效推論、彈性伸縮、以及與各種推論後端整合。

## 主要特色

1. **支援多種框架 (Multiple Frameworks Support):**
    Triton 支援所有主流的深度學習與機器學習框架，包含:

    - PyTorch (TorchScript, Torch-TensorRT)
    - TensorFlow (GraphDef, SavedModel, TensorRT Graph)
    - ONNX Runtime
    - TensorRT
    - OpenVINO
    - Python / C++ 自定義後端

    這讓您不需要為了不同的模型而更換不同的服務工具。

2. **多協議推論 API:**
    Triton 提供了以下標準的 API 介面，讓各種程式語言的客戶端都能輕鬆地與之整合。

    - HTTP/REST
    - gRPC
    - C API
    - Java API。

3. **高效能推論 (High Performance):**

    Triton 針對 NVIDIA GPU 進行了深度優化，能夠充分發揮硬體效能。它支援多種查詢排程與批次處理 (Batching) 策略，例如:

    - 動態批次 (Dynamic Batching): 可以將多個獨立的推論請求組合成一個批次進行處理，大幅提升 GPU 的利用率與吞吐量 (Throughput)。
    - 模型並行與多實例 (model instances): 可以在單一 GPU 或多個 GPU 上同時運行多個模型（或同一個模型的多個實例），最大化硬體資源的利用。
    - 支援 GPU / CPU 混合

4. **模型管理 (Model Management):**
    Triton 提供了一個模型倉庫 (Model Repository) 的概念，可以從本地檔案系統、Google Cloud Storage 或 Amazon S3 等來源載入模型。它支援模型的版本控制，並且可以在服務不中斷的情況下，動態地載入、卸載或更新模型。

5. **可擴展性 (Scalability):**
    Triton 可以輕易地與 Kubernetes、Docker Swarm 等容器編排工具整合，實現服務的自動擴展與負載平衡。

6. **即時監控 (Real-time Metrics):**
    Triton 透過 `Prometheus` 格式提供詳細的效能指標，例如 GPU 利用率、記憶體用量、推論延遲、吞吐量等，方便使用者監控服務狀態並進行效能調校。

## 使用教學

1. [Serving Models with the TensorRT-LLM Backend](./tensorrtllm_backend.md)

## 版本號說明 (Versioning)

您可能會注意到 Triton Inference Server 有兩種不同的版本號格式，例如 `25.07` 和 `2.59.0`。它們代表不同的層級：

1. **NGC 容器版本 (例如 `25.07`)**:
    - 這是您在 `docker pull` 時使用的版本，格式為 `YY.MM` (年.月)。
    - 它代表一個完整的軟體堆疊 (Software Stack)，其中包含了特定版本的 Triton Server，以及與之相容的 CUDA、cuDNN、TensorRT 和驅動程式等。
    - 使用此版本號可確保整個推論環境的一致性與穩定性。

2. **Triton 軟體版本 (例如 `2.59.0`)**:
    - 這是 Triton Server 軟體本身遵循語意化版本 (`MAJOR.MINOR.PATCH`) 的版本號。
    - 它內含在對應的 NGC 容器版本中。

簡單來說，`YY.MM` 的容器版本是一個包含了特定 `X.Y.Z` Triton 軟體版本的「發行版」。
