# Ollama

> Get up and running with large language models locally.

Ollama 是一個讓使用者可以在自己的設備上運行、創建和分享大型語言模型的開源軟體。

##### Related Repo

- [open-webui/open-webui](./webui/README.md)
- [valiantlynx/ollama-docker](./webui-advance/README.md)

## Run With Docker

### CPU only

```sh
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

## Start Ollama

### Run model locally

啟動之後，你就可以進入 docker container 來運行相關的 LLM 模型，以下以運行 [Llama 3](https://ollama.com/library/llama3) 為例:

```sh
# 進入 docker container 並執行 command: ollama run llama3
docker exec -it ollama ollama run llama3
```

### REST API

> Ollama has a REST API for running and managing models.

#### Generate a response

第一種方式是生成出解答。

```bash
curl http://localhost:11434/api/generate -d '{
    "model": "llama3",
    "prompt":"Hello Ollama?"
}'

```

#### Chat with a model

第二種則是目前主流的方法，做對話生成。

```bash
curl http://localhost:11434/api/chat -d '{
    "model": "llama3",
    "messages": [
        { "role": "user", "content": "Hello Ollama?" }
    ]
}'
```
