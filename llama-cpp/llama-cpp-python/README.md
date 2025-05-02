# Python Bindings for [llama.cpp](https://github.com/ggml-org/llama.cpp) (llama-cpp-python)

## 🐍 簡介

`llama-cpp-python` 是 `llama.cpp` 的 Python bindings，支援使用 Python 輕鬆載入、推理、並呼叫 OpenAI 介面的伺服器。

## 功能特色

- 使用 `ctypes` 綁定原生 C 函式庫
- 提供高層級 LLM API
- 提供 OpenAI 相容伺服器 (`llama-cpp-python --server`)
- 支援 `n_gpu_layers` 啟用 Metal/CUDA 加速

- GitHub: [abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python)

## Installtion

- Python 3.8+
- C compiler
    - Linux: gcc or clang
    - Windows: Visual Studio or MinGW
    - MacOS: Xcode

To install the package, run:

```sh
$ pip install llama-cpp-python
```
This will also build llama.cpp from source and install it alongside this python package.

### 在 macOS 安裝 llama-cpp-python（Apple Silicon）

Detailed `MacOS Metal GPU` install documentation is available at [docs/install/macos.md](https://llama-cpp-python.readthedocs.io/en/latest/install/macos/)

#### 1. 前置條件

```bash
$ xcode-select --install
```

#### 2. 建議使用 Miniforge 安裝 Conda

```bash
$ wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
$ bash Miniforge3-MacOSX-arm64.sh
```

#### 3. 建立 conda 環境

```bash
$ conda create -n llama python=3.10
$ conda activate llama
```

#### 4. 安裝 llama-cpp-python + Metal GPU 加速

```bash
$ CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 pip install --upgrade --force-reinstall --no-cache-dir llama-cpp-python
```
- FORCE_CMAKE=1：​強制使用 CMake 重新編譯，確保應用新的設定。​

> If encount error:  `(mach-o file, but is an incompatible architecture (have 'x86_64', need 'arm64'))`

Try installing with:

```bash
$ CMAKE_ARGS="-DCMAKE_OSX_ARCHITECTURES=arm64 -DCMAKE_APPLE_SILICON_PROCESSOR=arm64 -DGGML_METAL=on" pip install --upgrade --verbose --force-reinstall --no-cache-dir llama-cpp-python
```

## Example

```python
from llama_cpp import Llama

llm = Llama(
      model_path="./models/7B/llama-model.gguf",
      # n_gpu_layers=-1, # Uncomment to use GPU acceleration
      # seed=1337, # Uncomment to set a specific seed
      # n_ctx=2048, # Uncomment to increase the context window
)
output = llm(
      "Q: Name the planets in the solar system? A: ", # Prompt
      max_tokens=32, # Generate up to 32 tokens, set to None to generate up to the end of the context window
      stop=["Q:", "\n"], # Stop generating just before the model would generate a new question
      echo=True # Echo the prompt back in the output
) # Generate a completion, can also call create_completion
print(output)
```

By default llama-cpp-python generates completions in an OpenAI compatible format:

```sh
{
  "id": "cmpl-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "object": "text_completion",
  "created": 1679561337,
  "model": "./models/7B/llama-model.gguf",
  "choices": [
    {
      "text": "Q: Name the planets in the solar system? A: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune and Pluto.",
      "index": 0,
      "logprobs": None,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 14,
    "completion_tokens": 28,
    "total_tokens": 42
  }
}
```
