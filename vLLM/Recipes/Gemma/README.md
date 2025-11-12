# Running Gemma with vLLM

This guide shows how to run the **Gemma** model using **vLLM** in Docker, with GPU acceleration and an OpenAI-compatible API.

## Prerequisites

- **Docker** (24+)
- **NVIDIA GPU** with CUDA + **NVIDIA Container Toolkit**
- A **Hugging Face access token** stored as an environment variable:

  ```bash
  export HUGGING_FACE_HUB_TOKEN=hf_xxx_your_token
  ```

## ⚙️ Command

Run the following command to start the Gemma model with vLLM:

### 1. **[gemma-3-4b-it](https://huggingface.co/google/gemma-3-4b-it)**

```bash
docker run --rm \
    --gpus device=0 \
    -e PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
    -p 8000:8000 \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    -e HUGGING_FACE_HUB_TOKEN=${HUGGING_FACE_HUB_TOKEN} \
    --ipc=host \
    vllm/vllm-openai:latest \
    --model google/gemma-3-4b-it \
    --enable-multimodal
```
- 「**PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True**」：smoother memory allocation on CUDA
- 「**--ipc=host**」：larger shared memory (helpful for big models)
- 「**--enable-multimodal**」: enables multimodal capabilities for the model

## Example of Usage

### 🖼️ Multimodal Example (Image)

You can directly provide an image URL in your request. However, it's crucial to use the **direct link to the raw image file**, not a link to a webpage displaying the image.

> For example, a GitHub link like `https://github.com/.../image.png` is an HTML page. You need to use the "raw" version of the URL.

#### `curl` Command with Image URL

```bash
curl http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "google/gemma-3-4b-it",
        "messages": [
            {
                "role": "system",
                "content": "You are an advanced AI assistant. You can only respond in JSON format."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://storage.googleapis.com/sfr-vision-language-research/LAVIS/assets/merlion.png"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Which city is this?"
                    }
                ]
            }
        ],
        "max_tokens": 1024,
        "temperature": 0
    }'
```
