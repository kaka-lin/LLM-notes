# AGENTS.md 說明

## 📌 用途

AGENTS.md 是整個專案的 **AI 專案說明書（AI-oriented README）**。
提供給 AI coding assistants（如 Cursor、Claude Code、VSCode Copilot、Roo Code、Antigravity）理解：

- 專案架構
- 全域規範
- 使用到哪些技能
- 使用到哪些流程

它讓 AI 在你的 repo 裡「不迷路」。

> [!NOTE]
> AGENTS.md 通常放在專案根目錄，大多數工具不支援全域 AGENTS.md（Antigravity 除外）。

## AGENTS.md 規範

根據 [agents.md](https://agents.md/) 的官方規範，這項標準的核心精神是：「讓機器讀的 README」。

- **YAML Frontmatter**：可選，非強制要求
- **標題寫法**：官方範例通常直接使用 Markdown 的一級標題（`#`）來定義專案名稱

> [!IMPORTANT]
> 官方標準：回歸「純 Markdown」，保持簡潔易讀。

---

### 範例 1：最簡版

適合小型專案或快速上手：

```markdown
# My Project

## 專案概述（Overview）

這是一個使用 Python + FastAPI 的後端服務。

## 建置與執行（Build & Run）

- 安裝依賴：`pip install -r requirements.txt`
- 啟動服務：`uvicorn main:app --reload`
- 執行測試：`pytest`
- 程式碼檢查：`ruff check .`

## 程式碼風格（Code Style）

- 遵循 PEP 8
- 使用 type hints
- 使用 Conventional Commits
```

---

### 範例 2：完整版（Template）

適合大型專案或團隊協作：

```markdown
# <專案名稱>

## 專案概述（Project Overview）

描述專案核心目標、主要程式語言與技術架構。

## 開發環境提示（Dev Environment Tips）

- 使用 `pyenv` 或 `nvm` 管理語言版本
- 專案使用 `poetry` / `pnpm` 管理依賴
- 設定檔位於 `.env.example`，複製為 `.env` 後填入值

## 建置與測試指令（Build & Test Commands）

- 安裝依賴：`poetry install` 或 `pnpm install`
- 啟動開發：`pnpm dev` 或 `uvicorn main:app --reload`
- 執行測試：`pnpm test` 或 `pytest`
- 程式碼檢查：`pnpm lint` 或 `ruff check .`
- 型別檢查：`pnpm typecheck` 或 `mypy .`

## 測試說明（Testing Instructions）

- 測試設定檔位於 `pytest.ini` 或 `vitest.config.ts`
- 執行單一測試：`pytest -k "test_name"` 或 `pnpm vitest run -t "test name"`
- 提交前確保所有測試通過
- 修改程式碼時，同步更新相關測試

## 程式碼風格指南（Code Style Guidelines）

- 遵循專案的 Style Guide（PEP 8 / Airbnb / Google）
- 命名慣例：變數 `snake_case`、類別 `PascalCase`、常數 `UPPER_SNAKE_CASE`
- 使用 Prettier / Black 自動格式化

## PR 規範（PR Instructions）

- 標題格式：`[模組名稱] 簡短描述`
- 提交前執行 `pnpm lint && pnpm test`
- PR 需通過 CI 檢查後才能合併
- 重大變更需更新 README 或相關文件

## 安全性注意事項（Security Considerations）

- 不要在程式碼中硬編碼密鑰或憑證
- 使用環境變數管理敏感資訊
- 避免使用 `eval()` 或動態執行未知程式碼
- 處理使用者輸入時進行驗證與消毒
```

---

## 📚 參考來源

- 官方規範：[https://agents.md/](https://agents.md/)
