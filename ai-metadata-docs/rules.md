# RULES.md 說明

## 📌 用途

Rules 是 **可重複使用的行為規範**，用於引導 AI 的行為模式。
讓 AI 知道「在特定情境下該如何表現」。

AI 會把 rule 當成：
→「持久的上下文指引，影響回應的風格與行為」

## 📂 檔案位置

| 工具 | Local（專案配置） | Global（個人配置） |
|------|-----------------|------------------|
| **Antigravity** | `.agent/rules/` | `~/.gemini/GEMINI.md`<br>`~/.gemini/antigravity/rules/` |
| **Roo Code** | `RULES.md` | `~/.roo/` |
| **Cursor** | `.cursor/rules/*.mdc` | Cursor Settings |
| **Claude Code** | `CLAUDE.md` | `~/.claude/CLAUDE.md` |

> [!NOTE]
> 不同工具使用不同的規則檔案格式。本文主要說明 **Antigravity** 的 Rules 規範。

## RULES 規範

根據 [Antigravity 官方文件](https://antigravity.google/docs/rules-workflows)，Rules 由 **YAML Frontmatter** + **Markdown Body** 組成。

### YAML Frontmatter 欄位

| 欄位 | 必填 | 說明 |
|------|:----:|------|
| `title` | ✅ | Rule 的顯示名稱 |
| `description` | ✅ | 描述何時應用此規則（對 `model_decision` 啟動方式很重要） |
| `activation` | ✅ | 啟動方式（見下方說明） |
| `glob` | ⚠️ | 當 `activation: glob` 時必填，檔案匹配模式 |

### Activation 啟動方式

| 值 | 說明 |
|------|------|
| `manual` | 手動啟動，透過 `@RuleName` 在對話中提及 |
| `always_on` | 永遠啟用，每次互動都套用 |
| `model_decision` | 由 AI 根據 description 自動判斷是否套用 |
| `glob` | 當處理符合 glob 模式的檔案時自動啟用 |

### Markdown Body

包含具體的規範內容：
- 程式碼風格指南
- 命名慣例
- 安全性規範
- 專案特定限制

### 特殊功能

- 可使用 `@filename` 語法引用其他檔案作為上下文
- 每個 Rule 檔案最大 **12,000 字元**

---

### 範例 1：最簡版

適合簡單的風格規範：

```markdown
---
title: Python Style
description: Python 程式碼風格規範
activation: model_decision
---

# Python Coding Standards

- 遵循 PEP 8
- 使用 type hints
- 使用 `ruff` 進行 linting
- 變數命名使用 snake_case
```

---

### 範例 2：完整版（Template）

適合需要條件觸發的複雜規則：

```markdown
---
title: React Component Guidelines
description: 當撰寫或重構 React 元件時套用，確保程式碼品質與一致性
activation: glob
glob: "**/*.tsx"
---

# React Component Standards

## 元件結構

- 使用 Functional Components + Hooks
- 優先使用 `const` 箭頭函數定義元件
- Props 型別定義在元件上方

## 命名慣例

- 元件檔案：PascalCase（如 `UserProfile.tsx`）
- Hook 檔案：camelCase 加 use 前綴（如 `useAuth.ts`）
- 樣式檔案：與元件同名（如 `UserProfile.module.css`）

## 狀態管理

- 簡單狀態使用 `useState`
- 複雜狀態使用 `useReducer`
- 全域狀態使用 Context 或 Zustand

## 效能考量

- 使用 `React.memo` 避免不必要的重新渲染
- 使用 `useMemo` 和 `useCallback` 優化效能
- 避免在 render 中建立新物件或函數

## 測試

- 每個元件都需要對應的測試檔案
- 使用 React Testing Library
- 測試使用者行為而非實作細節
```

---

## 📚 參考來源

- Antigravity 官方文件：[https://antigravity.google/docs/rules-workflows](https://antigravity.google/docs/rules-workflows)
