# WORKFLOW.md 說明

## 📌 用途

Workflow 是 **多步驟流程編排**，用於定義一系列順序執行的任務。
讓 AI 知道「如何一步步完成複雜任務」。

AI 會把 workflow 當成：
→「一組有順序的操作指南」

## 📂 檔案位置

| 工具 | Local（專案配置） | Global（個人配置） |
|------|-----------------|------------------|
| **Antigravity** | `.agent/workflows/` | `~/.gemini/antigravity/global_workflows/` |
| **VSCode + Copilot** | `.github/workflows/` | - |
| **Claude Code** | 支援（無固定路徑） | - |

> [!NOTE]
> Workflow 主要由 **Antigravity（Gemini CLI）** 完整支援，其他工具部分支援。

## WORKFLOW.md 規範

根據 [Antigravity 官方文件](https://antigravity.google/docs/rules-workflows)，Workflow 由 **YAML Frontmatter** + **Markdown Body** 組成。

### YAML Frontmatter 欄位

| 欄位 | 必填 | 說明 |
|------|:----:|------|
| `title` | ✅ | Workflow 名稱，也是觸發的 slash command（如 `/deploy`） |
| `description` | ✅ | 簡短描述這個 workflow 的用途 |

### Markdown Body

包含一系列順序執行的步驟：
- 使用編號列表或標題定義步驟
- 每個步驟描述具體的操作指令
- 可使用 `/workflow-name` 呼叫其他 workflow

### 限制

- 每個 Workflow 檔案最大 **12,000 字元**

---

### 範例 1：最簡版

適合簡單的自動化流程：

```markdown
---
title: Test
description: 執行專案測試
---

# Steps

1. 執行 lint 檢查：`npm run lint`
2. 執行單元測試：`npm test`
3. 檢查測試覆蓋率是否達標
```

---

### 範例 2：完整版（Template）

適合複雜的部署或發布流程：

```markdown
---
title: Production Release
description: 驗證、建置、部署應用程式的完整流程
---

# Production Release Workflow

## 前置檢查

1. 確認當前分支為 `main`
2. 確認沒有未提交的變更：`git status`

## 測試與驗證

3. 執行完整測試套件：`npm test`
4. 檢查 lint 錯誤：`npm run lint`
5. 執行型別檢查：`npm run typecheck`

## 建置

6. 如果測試通過，建置生產版本：`npm run build`
7. 驗證建置產物完整性

## 部署準備

8. 根據 commits 產生 changelog
9. 更新版本號
10. 等待使用者確認後推送到 `production` 分支

## 注意事項

- 部署前務必確認所有測試通過
- 重大變更需通知相關團隊成員
```

---

## 📚 參考來源

- Antigravity 官方文件：[https://antigravity.google/docs/rules-workflows](https://antigravity.google/docs/rules-workflows)
