# vLLM Examples

此 repo 用來整理 vLLM 的各種實作範例。依照 vLLM 官方文件，examples 主要分成三大類：

1. **Offline Inference**：在 Python 程式中直接呼叫 `vllm.LLM` 進行離線 / 批次推論。
2. **Online Serving**：啟動 vLLM 的 OpenAI 相容 API Server，透過 HTTP / WebSocket 從外部服務呼叫。
3. **Others**：進階功能示範，例如 LMCache、Tensorizer 等。

本 repo 目前主要涵蓋：

- **Offline Inference**：基本文字生成與多模態（LLaVA）圖片理解。
- **Online Serving**：使用 OpenAI 相容 API 的 chat / streaming / image + JSON 輸出等範例。
