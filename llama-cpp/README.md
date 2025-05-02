# llama.cpp

## 🦙 什麼是 `llama.cpp`

> Inference of Meta's LLaMA model (and others) in pure C/C++

`llama.cpp` 是由 Georgi Gerganov 開發的開源 C/C++ 專案，能在 CPU 上執行 Meta 的 LLaMA 模型，特別適合在資源有限的環境中部署 LLM。

## 核心特點

- 支援 `GGUF` 模型格式
- 支援多種後端：Metal（macOS）、CUDA、OpenBLAS、Vulkan 等
- 模型量化支援（Q2_K、Q4_K、Q5_K、Q8_0 等）
- 可用於 CLI 推理與嵌入式裝置部署

## 編譯與推理流程

```bash
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make

# 推理
./main -m models/llama-2-7b-chat.gguf -p "Hello, world"
```

