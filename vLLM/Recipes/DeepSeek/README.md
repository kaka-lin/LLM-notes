# Running DeepSeek with vLLM

This guide shows how to run the **DeepSeek** model using **vLLM** in Docker, with GPU acceleration and an OpenAI-compatible API.

## Prerequisites

- **Docker** (24+)

- **NVIDIA GPU** with CUDA + **NVIDIA Container Toolkit**

- A **Hugging Face access token** stored as an environment variable:

  ```bash
  export HUGGING_FACE_HUB_TOKEN=hf_xxx_your_token
  ```

## ⚙️ Command

Run the following command to start the DeepSeek model with vLLM:

### 1. **[DeepSeek-LLM-7B-Chat](https://huggingface.co/deepseek-ai/deepseek-llm-7b-chat)**

```bash
docker run --rm \
    --gpus all \
    -e PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
    -p 8000:8000 \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    -e HUGGING_FACE_HUB_TOKEN=${HUGGING_FACE_HUB_TOKEN} \
    --ipc=host \
    vllm/vllm-openai:latest \
    --model deepseek-ai/deepseek-llm-7b-chat
```
- 「**PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True**」：smoother memory allocation on CUDA
- 「**--ipc=host**」：larger shared memory (helpful for big models)
