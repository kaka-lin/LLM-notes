# LLM Chat Memory

## Introduction

- [LLM Chat Memory 常見方式整理](./LLM_chat_memory.md)

## Example

This repo uses **Jinja2** templates inside TOML prompt files (see [template.toml](./template.toml)).
The basic idea is:

1. You have a *template* string (contains `{{ var }}` and `{% if ... %}` blocks)
2. You have a *variables dict* (e.g. `{"user_input": "..."}`)
3. Render = template + variables → final prompt text

This directory contains minimal demos:

### Render a `.toml` file that contains Jinja2 templates

This is closer to how PR-Agent stores prompts (TOML keys containing template strings).

Files:

- `template.toml`
- `render_template_toml.py`

Run:

```bash
python render_template_toml.py
```
