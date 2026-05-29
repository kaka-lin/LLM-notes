# superpowers

[superpowers](https://github.com/obra/superpowers) 是「**流程紀律**」式的 AI coding skill 框架，強制 AI 走 TDD、原子任務、系統化除錯。重點不是給觀點，而是釘死製程紀律（methodology）。

> 它強調 **TDD 強制執行** 與 **根因除錯紀律**，定位給想要「可重複、可審計 AI 開發流程」的工程師。

## 支援平台

跨多種 AI coding agent 都能用，但每個 agent 的安裝管道（plugin marketplace / CLI extension / 對話式安裝）都不一樣：

- Claude Code（官方 plugin marketplace 或 Superpowers marketplace）
- Cursor（內建 plugin 系統）
- Codex CLI（`/plugins` 搜尋）
- Codex App（側邊欄 Plugins）
- Google Gemini CLI（`gemini extensions install`）
- OpenCode（自訂安裝流程：丟連結叫 OpenCode 自己照 `INSTALL.md` 跑）
- Factory Droid（`droid plugin install`）
- GitHub Copilot CLI（Superpowers marketplace）

如果同時用多個 agent，**要分別安裝**。貢獻指南明確要求 skill 更新「必須在所有支援的 agent 間運作」。

## 安裝

superpowers 沒有像 gstack 那樣的單一 setup 腳本，而是把工作丟給各 agent 的 plugin 機制。所以「安裝方式」其實就是「你用什麼 agent」的對照表。指令、路徑、踩坑點整理在這裡：

→ [install.md](./install.md)

或直接看官方原文：<https://github.com/obra/superpowers>

## 核心理念

整個框架圍繞兩條 iron law：

1. **NO CODE WITHOUT A FAILING TEST FIRST**（沒有失敗的測試就不准寫功能）
2. **NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**（沒找到根因就不准修 bug）

如果 AI 試圖偷跑（沒測試就寫功能），Superpowers 的機制**會直接刪除這段程式碼**，強迫 AI 退回測試階段。

## 核心 skill 分類

14+ 個 skill，分布在幾個階段：

### 測試

- `test-driven-development` —— **入口 skill**。紅綠重構強制執行，沒 failing test 不准進實作

### 除錯

- `systematic-debugging` —— **4 階段根因除錯流程**（root-cause-tracing、defense-in-depth、condition-based-waiting）
- `verification-before-completion` —— 完成前驗證

### 規劃與協作

- `brainstorming` —— 設計階段完成前禁止寫 code
- `writing-plans` —— **原子化計畫**，每任務 2-5 分鐘
- `executing-plans`
- `dispatching-parallel-agents` —— 並行子代理
- `subagent-driven-development`

### 程式碼審查

- `requesting-code-review`、`receiving-code-review`

### 分支與發佈

- `using-git-worktrees`
- `finishing-a-development-branch`

### Meta

- `writing-skills` —— 寫新 skill 的 skill
- `using-superpowers`

## 推薦工作流

README 推薦的七階段流程：

```text
Brainstorm → Worktree → Plan → Subagent Build → TDD → Review → Branch Completion
```

每階段都有對應 skill 把關，跳階段被視為違規。

核心思想：**先 reframe 問題 → 隔離分支 → 拆成 2-5 分鐘原子任務 → 子代理執行 → 紅綠重構 → 嚴格審查 → 驗證後合併**

### systematic-debugging 4 階段（節錄）

代表性 skill。當遇到 bug、test failure、預期外行為時，**必須**依序：

1. **Root Cause Investigation** —— 仔細讀錯誤訊息、穩定重現、看 recent commits、跨元件邊界 log、trace data flow
2. **Pattern Analysis** —— 找類似 working code、比對差異、釐清依賴與假設
3. **Hypothesis and Testing** —— 形成單一假設、做最小變更、驗證後再進
4. **Implementation** —— **先寫 failing test**、實作單一根因修復、3 次修不好就回頭質疑架構

官方聲稱「systematic 方式達 95% first-time fix rate vs. 隨機修法 40%」。

## 適用情境

- **生產級程式碼**：高測試覆蓋率要求、需可審計開發流程的專案
- **協作型專案**：多人 review、有規範性要求
- **AI 容易出錯的領域**：複雜資料管線、外部 API 整合、需要嚴密除錯紀律的場景

## 不適用情境

- **原型 / hackathon**：紅綠重構會拖節奏 3-5x
- **探索性程式設計**：方向都還沒定下，TDD 浪費時間
- **單檔小工具**：殺雞用牛刀

## 已知 trade-off

- Token cost 比裸 Claude Code 高 **3-5x**（每個 feature 都先寫測試 + sub-agent 來回）
- 學習曲線高，要熟「七階段切換」與每個 skill 觸發時機
- 對開發節奏的衝擊很大，新手會卡在 stage 切換

## 與 gstack 的關係

兩者方向不同、可互補：

- gstack 管「**做什麼 / 為什麼這樣設計**」（方向、決策、角色觀點）
- superpowers 管「**怎麼做、怎麼避免犯錯**」(流程、紀律、製程)
