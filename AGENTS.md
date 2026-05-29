# AGENTS.md

這份規則適用於整個 repo.

## Project Context

This repo is **learning notes + small runnable examples** for LLM tooling, inference engines, agent workflows, and observability.

There is **no unified build/test system at the repo root**. Treat each top-level folder as its own mini-project — install per-folder dependencies, run from that folder.

## Core Rules

- Keep changes small, local, and example-focused.
- Touch only the folder required by the task.
- Do not refactor unrelated folders or "standardize" the whole repo.
- Prefer readable, runnable scripts over frameworks; avoid unnecessary abstractions.
- Do not commit secrets. `.env` files are gitignored (note: `Google/.env` exists and is sensitive).

## Repo Map

Topic folders:

- `AI-Coding-Skills/` — Notes comparing skill / workflow packages for AI coding agents (gstack, superpowers).
- `Anthropic/` — Anthropic SDK examples (Python).
- `Conda/` — Notes on Conda / Miniforge / Miniconda.
- `GGUF/` — Notes on the GGUF model format.
- `Google/` — Google Gemini Developer API examples (incl. live + audio/ASR).
- `Hermes/` — Notes on Hermes (vs. OpenClaw comparison).
- `LLM-Chat-Memory/` — Chat memory template rendering utilities.
- `Langfuse/` — Langfuse architecture + deployment notes.
- `LiteLLM/` — LiteLLM sync/async examples + chat-memory CLI.
- `Ollama/` — Ollama notes, Python example, Open WebUI compose.
- `OpenClaw/` — OpenClaw concepts, deployment, best practices.
- `SDD/` — Spec-Driven Development notes + URL shortener example.
- `TensorRT-LLM/` — TensorRT-LLM notes + OpenAI-compatible client snippet.
- `Transformer/` — Notes on Transformer internals (attention mask, etc.).
- `Triton Inference Server/` — Triton notes + TensorRT-LLM backend.
- `ai-metadata-docs/` — Notes on AI metadata standards.
- `llama-cpp/` — llama.cpp + llama-cpp-python notes.
- `vLLM/` — vLLM notes + server/client snippets.

When adding a new top-level folder, add a one-line entry here.

## Tooling

Dependencies are **not pinned at repo level**; install what each script / its README mentions.

Recommended Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
```

Example runs (see each folder's README for canonical commands):

```bash
# LiteLLM
python -m pip install litellm openai
python LiteLLM/chat.py

# Anthropic
python -m pip install anthropic httpx
python Anthropic/python/examples/messages.py

# Google Gemini
python -m pip install google-genai
python Google/main.py

# vLLM (server + client)
python -m pip install vllm openai
vllm serve openai/gpt-oss-20b
python vLLM/chat.py
```

Docker / Compose (where applicable):

```bash
# Open WebUI + Ollama (run from Ollama/webui or Ollama/webui-advance)
docker compose up -d
```

## Code Style

Python style follows the user's global rules at `~/.claude/rules/python-code-style.md`:

- Lint + format with **Ruff** (not Black / isort / flake8).
- Line length **100**.
- **Absolute imports** only.
- `X | None` instead of `Optional[X]` (Python 3.10+).
- Google-style docstrings on public APIs.
- Type-annotate public functions and reusable helpers.
- Catch specific exceptions; never bare `except:`.

Markdown style follows `~/.claude/rules/markdown-code-style.md`:

- 2-space indent for unordered lists, 4-space for ordered.
- Blank lines around headings, lists, code blocks.
- Fenced code blocks with language identifier.

Repo-specific additions:

- Keep scripts runnable from the repo root or from their own folder; avoid `sys.path` hacks.
- Snippets in markdown should be copy/paste-runnable.

## Secrets / Configuration

- Never hardcode API keys.
- Prefer env vars: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, etc.
- `.env` is gitignored; do not add or commit secrets.

## Testing

- No tests currently exist at repo level.
- If adding tests, prefer `pytest` inside the affected folder.

```bash
python -m pip install pytest
pytest <folder>/
```

## Cursor / Copilot Rules

- No `.cursor/rules/` or `.cursorrules` present.
- No `.github/copilot-instructions.md` present.
- This `AGENTS.md` is the authoritative agent instruction file.
