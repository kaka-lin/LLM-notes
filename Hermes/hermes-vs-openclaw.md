# Hermes vs OpenClaw：大方向差異

兩個專案乍看都是「自主 AI 代理 + 多訊息平台 + 可擴展技能」，但**設計哲學**截然不同。本文不做逐項 feature 對照，只談**為什麼兩者長得不一樣**，以及怎麼挑。

> 細節欄位（記憶字元上限、Session Key 格式、CLI 子指令名稱等）請看各自的 concept 文件，這份只談「大方向」。

## 1. 一句話定位

- **Hermes ≈ 工程化的 Agent Harness**：把 LLM 當基礎設施，圍繞它打造「能自己迭代自己」的 agent runtime。
- **OpenClaw ≈ 可塑造的 AI Persona 工作站**：把 agent 當作「會養成的個人助手」，由使用者塑造人格與工作流。

換句話說：

| | Hermes | OpenClaw |
| --- | --- | --- |
| 核心比喻 | 一台**自帶最佳化能力的 agent 引擎** | 一個**會被使用者養大的 AI 同事** |
| 誰主導迭代 | **Agent 自己**（會生 skill、會改 memory、會壓縮對話） | **使用者**（寫 SOUL.md、寫 SKILL.md、養 MEMORY.md） |
| 工程重心 | Harness / Context engineering（frozen snapshot、prefix cache、硬上限） | Persona / 自動化（Daily Notes、Dreaming、多 agent 分工） |

## 2. Hermes 的核心思維：Harness Engineering

Hermes 的設計處處體現「把 LLM 行為**工程化**」的取捨：

- **Frozen snapshot**：memory 一旦進入 session 就鎖定，不再變動。為的是讓 prefix cache 命中、token 成本可預期。
- **硬性字元上限**：`MEMORY.md` 2,200 字、`USER.md` 1,375 字。逼使用者（與 agent）只留下真正重要的事。
- **Multi-frontend 共用同一個 `AIAgent`**：CLI、Gateway、ACP、Batch、API server 都呼叫同一份核心。前端只是 IO，agent 行為一致。
- **Agent 自己管自己**：agent 透過 `memory` tool 自己 add/replace/remove 記憶；透過 `skills` 機制自己安裝 / 啟用 skill；context 滿了由 `ContextEngine` 自動壓縮並建立 session lineage。

> 📝 換個角度說：**Hermes 把「怎麼讓 LLM 在生產環境穩定運作」當成第一性問題**，再回過頭設計 memory / session / skills 系統。它的克制與精簡（單一 agent、frozen memory、硬上限）都是這個取捨的副產品。

對應的特徵：

- 預設 fail-closed、allowlist + pairing 才放行
- 18 個訊息平台 adapter，但**只有一個 agent**接所有平台
- Skill 由 agent 在運行時動態啟用 / 安裝，prompt 結構穩定可 cache

## 3. OpenClaw 的核心思維：Persona & 富表達自動化

OpenClaw 的設計則處處體現「讓使用者**塑造**自己的 AI」的取捨：

- **多 Agent 原生**：可以同時養 Coder、Reviewer、Researcher 等多個 agent，每個有獨立 workspace 與 `SOUL.md` 定義人格與任務。
- **記憶分層 + 背景整合**：`MEMORY.md` 是長期事實、`memory/YYYY-MM-DD.md` 是每日筆記、`DREAMS.md` 是背景 Dreaming 整合產出。記憶會「自己長」。
- **Skill 由使用者寫、市集分發**：ClawHub 是社群驅動的市集，使用者下載／發布 skill；agent 不太「自己生 skill」，而是「執行使用者選好的 skill」。
- **Session Key 自由組合**：可依平台 / 頻道 / Cron job / Webhook 任意拼接，使用者掌握隔離邊界。

> 📝 換個角度說：**OpenClaw 把「怎麼讓使用者擁有並塑造一個個人化 AI」當成第一性問題**。它願意付出較複雜的設定（多 agent、多目錄、多 plugin）來換取「我的 AI 越用越懂我」的個人化體驗。

對應的特徵：

- 每天 04:00 自動重置 session、Daily Notes 自動產生
- 多 agent 共用 workspace、用 allowlist 控制誰能用哪些 skill
- ClawRouter 獨立成專案、強調成本最佳化

## 4. 「Agent 會自己生 Skill」這件事

這是兩者最直觀的氣質差異：

- **Hermes 的 agent 比較「主動」**：它會在對話中決定要不要更新 memory、要不要安裝某個 skill、什麼時候該壓縮對話。整套系統假設 agent 是迭代主體。
- **OpenClaw 的 agent 比較「乖」**：它在使用者塑造的框架下運作，由使用者寫 SOUL.md 定義人格、寫 / 裝 skill、設 cron。Dreaming 是少數「agent 自己跑」的背景任務，但仍受 plugin 設定約束。

這不是「誰比較聰明」的問題，而是**控制權**的取捨：

- 想要 agent 自我演化、減少手動介入 → Hermes
- 想要使用者掌控、agent 可預期地執行任務 → OpenClaw

## 5. 多前端 vs 多 Agent

從架構角度看，兩者選了正交的擴張方向：

```text
Hermes：    1 個 agent  ×  多個前端（CLI / Gateway / ACP / Batch / API）
OpenClaw： 多個 agent  ×  共用前端（每個 agent 獨立 workspace / SOUL.md）
```

- Hermes 認為「**人格與記憶該統一**」，無論你從哪個平台找 bot，他都是同一個 bot。
- OpenClaw 認為「**人格該按情境分化**」，Coder 跟 Reviewer 應該是不同的人。

## 6. 怎麼選？

不是「誰比較好」，而是看**你想解什麼問題**：

| 你的情境 | 推薦 |
| --- | --- |
| 想要一個能跨多個訊息平台的「我的 bot」，且希望 agent 自己處理 memory / context 工程細節 | **Hermes** |
| 想要養一群分工合作的 AI agent，每個有獨立人格與記憶 | **OpenClaw** |
| 想要強自動化的 daily 筆記與背景記憶整合 | **OpenClaw** |
| 想要精簡可預期、token 成本好控制的 production agent | **Hermes** |
| 想要嚴格的訊息平台授權（allowlist + pairing） | **Hermes** |
| 想要強 Provider routing 與成本最佳化 | **OpenClaw**（ClawRouter） |
| 想用 RL 訓練個人代理 | **OpenClaw**（OpenClaw-RL） |

## 7. 兩者其實可以共存

兩個專案都是 [agentskills.io](https://agentskills.io) 的 reference implementation，**SKILL.md 標準一致**，多數 skill 在兩邊都能用（只要不依賴各自獨家工具）。

實務上常見的組合：

- **Hermes 當訊息平台前端、OpenClaw 當工作站**：用 Hermes 接 Telegram / Discord，背後跑 OpenClaw 的 agent 群。
- **共用 skill 庫**：自寫的 `SKILL.md` 同時放進兩邊的 skills 目錄。
- **Memory 不要互通**：兩邊的 memory 設計差太多，硬要同步只會混亂。

## 8. 相關文件

- [Gateway 與 Agent Loop](concepts/gateway-and-agent-loop.md)
- [Memory 系統](concepts/memory-system.md)
- [Session 管理](concepts/session-management.md)
- 對照：[OpenClaw README](../OpenClaw/README.md)
