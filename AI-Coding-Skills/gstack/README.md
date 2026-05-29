# gstack

[gstack](https://github.com/garrytan/gstack) 是「**虛擬團隊**」式的 AI coding skill 套件，把大師級的創業、產品、工程觀點注入到 AI 中，讓 AI 不只是寫 code 的外包工人，而像一個完整的早期創業團隊。

> 它強調 **策略決策** 與 **架構審查**，定位給 founder-engineer / solo builder。

## 支援平台

跨 10 種 AI coding agent 都能用：

- Claude Code（預設，主力平台）
- OpenClaw（透過 ACP 生 Claude Code session，外加 4 個 ClawHub 原生 skill）
- OpenAI Codex CLI
- OpenCode
- Cursor
- Factory Droid
- Slate
- Kiro
- Hermes
- GBrain

## 安裝

gstack 的安裝方式依「你用什麼 agent」「單人 / 團隊」會分成 5 種變化，光看官方 README 容易混亂。完整心智模型、決策樹、指令參考整理在這裡：

→ [install.md](./install.md)

或直接看官方原文：<https://github.com/garrytan/gstack#install--30-seconds>

## 核心 skill 分類

23+ 個 slash command，分布在幾個階段：

### 規劃與設計

- `/office-hours` —— **入口 skill**。六個強制問題（demand reality / status quo / desperate specificity / narrowest wedge / observation / future-fit）逼你 reframe 問題，產出 design doc
- `/plan-ceo-review` —— 從業務擴張、功能精簡等四個維度審查功能規劃
- `/plan-eng-review` —— 資深架構師視角，鎖定架構、規劃 data flow
- `/plan-design-review`、`/plan-devex-review`
- `/design-consultation`、`/design-shotgun`、`/design-html`

### 開發與測試

- `/review` —— 程式碼審查
- `/investigate` —— 根因調試
- `/qa` —— 完整 QA 測試（甚至會開瀏覽器點擊測試）
- `/qa-only` —— 純 bug 報告

### 發佈與部署

- `/ship`、`/land-and-deploy`、`/canary`、`/benchmark`

### 文件與安全

- `/document-release`、`/document-generate`
- `/cso` —— 首席安全官（OWASP + STRIDE）

### 協作與工具

- `/browse` —— AI 透過真實 Chrome 瀏覽網頁
- `/retro`、`/codex`、`/pair-agent`
- `/setup-gbrain`、`/sync-gbrain` —— 持久化知識庫
- `/gstack-upgrade`

### 安全凍結

- `/careful`、`/freeze`、`/guard`、`/unfreeze`

### 進階工作流

- `/autoplan`、`/spec`、`/learn`

## 推薦工作流

README 推薦的 startup 序列：

1. `/office-hours` ← 從這裡開始
2. `/plan-ceo-review`
3. `/review`（任何分支）
4. `/qa`（staging URL）

核心思想：**思考 → 規劃 → 構建 → 評審 → 測試 → 發佈 → 反思**

## 適用情境

- **身兼多職的 founder-engineer**：沒有 PM / 工程主管，需要 AI 幫忙補位策略與架構角色
- **新功能規劃前**：用 `/office-hours` 砍掉不切實際的範疇
- **上線前 QA**：用 `/review` + `/qa` 雙重把關

## 不適用情境

- **已經有真人 PM / 設計師 / 工程主管的團隊**：層級重疊，反而拖節奏
- **單純需要寫測試 / 嚴格 TDD**：這不是 gstack 的強項，去看 [`superpowers`](../superpowers/)
- **要小步快跑 / hackathon**：六問會拖節奏

## 已知 trade-off

- Token cost 比裸 Claude Code 高 1.5-2x（思考流程比較長）
- 學習曲線中等（23+ 個指令需要時間記它們的用途）
- 對「已知要做什麼」的明確任務反而會拖節奏
