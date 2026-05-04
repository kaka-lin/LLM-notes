# Hermes Agent

Hermes Agent 是 [NousResearch](https://nousresearch.com) 推出的開源自主 AI 代理（Autonomous AI Agent），透過大語言模型（LLM）執行廣泛任務，並能與多種訊息平台無縫整合。設計上強調**訊息平台原生**、**會話持久化**、**技能可擴展**與**安全 fail-closed**。

> 📚 官方文件：<https://hermes-agent.nousresearch.com/docs>

## 1. 概覽

Hermes 將「聊天介面」當成一級 UI：使用者透過 Telegram、Discord、Slack、WhatsApp、Signal、Matrix 等任一平台對 bot 對話，背後則是統一的 agent loop 處理推理、工具呼叫、記憶讀寫與排程任務。它和 OpenClaw、Claude Code、Open Interpreter 等工具有不少設計理念重疊（如 Skills 系統、自然語言 CLI、安全沙箱），但**訊息平台優先**與**harness engineering 思維**是 Hermes 的鮮明特色。

## 2. 主要特色

- **多平台 Gateway**：官方目前內建 18 個訊息平台 adapter，統一 session routing 與授權檢查。
- **Memory 系統**：`MEMORY.md`（2,200 字元）+ `USER.md`（1,375 字元）在 session 開始時 frozen 注入，保留 LLM prefix cache。
- **Skills 系統**：`SKILL.md` 形式的可擴展能力包，支援 Skills Hub 安裝、安全掃描、平台限制。
- **Session 管理**：SQLite + FTS5 全文索引、parent/child lineage tracking、跨平台隔離。
- **Cron / Heartbeat**：原生支援排程任務與心跳事件，可附帶 skill。
- **Pluggable architecture**：Memory provider、context engine、hooks 都可寫 plugin 擴充。
- **MCP 整合**：可動態載入 Model Context Protocol server 作為工具來源。
- **Fail-closed 安全模型**：未授權使用者預設拒絕，pairing flow 動態加人。

## 3. 安裝與部署

- [官方 Installation](https://hermes-agent.nousresearch.com/docs/getting-started/installation)
- [Hermes 部署設定 (hermes-server)](https://github.com/kaka-lin/hermes-server/tree/main/docs/deployment/setup.md)：

    涵蓋本機環境的具體設定（如 Telegram Bot、瀏覽器自動化等）

- [Hermes 專案文件中心 (hermes-server)](https://github.com/kaka-lin/hermes-server/tree/main/docs/README.md)

## 4. 使用方式與範例

### 4.1 客製化代理人個性

Hermes 透過 `~/.hermes/config.yaml` 與 `personality` 設定影響 agent 對話語氣，可結合 `MEMORY.md` 注入長期偏好，並用 skills 將特定任務模式固化下來。

- **詳細設定**：請參閱官方 [Personality](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality) 與 [Skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) 文件。

### 4.2 常用 CLI 子指令

Hermes 提供完整的 CLI（pairing 授權、session 操作、memory provider 切換、skills 管理、cron 排程等）。

- **完整指令**：請參閱官方 [CLI Reference](https://hermes-agent.nousresearch.com/docs) 與 [hermes-server 文件中心](https://github.com/kaka-lin/hermes-server/tree/main/docs/README.md)。

## 5. 架構系統

Hermes 的架構主要由以下層次組成：

1. **Gateway (閘道層)**：18 個平台 adapter，處理訊息收發、session 路由、授權檢查、slash command dispatch；對應官方類別 `GatewayRunner`。
2. **Agent Loop (推理協調)**：`AIAgent` 類別，platform-agnostic core；同一份核心被 CLI、Gateway、ACP、Batch、API server (OpenAI 相容) 共用。
3. **Reasoning Layer (推理層)**：`PromptBuilder` 拼接 personality / memory / skills / context 成 system prompt，超出 context window 時由 `ContextEngine` 觸發 compression。
4. **Memory (記憶系統)**：`MEMORY.md` + `USER.md` + 8 個內建可插拔 memory provider（Honcho、OpenViking、Mem0、Hindsight、Holographic、RetainDB、ByteRover、Supermemory）。
5. **Skills & Execution (技能與執行層)**：豐富的內建 toolsets（web、terminal、browser、vision、memory、cronjob、messaging、skills…）+ skills 提供可組合的高層能力。
6. **Session (會話)**：`SessionStore` 以 SQLite + FTS5 持久化儲存、lineage tracking、原子寫入。
7. **Scheduler (排程)**：Cron job、Heartbeat、Webhook event 整合到同一 agent task pipeline。
8. **Hooks**：`on-startup` / `on-message-received` / `on-message-sent` 等生命週期掛點，支援 plugin 擴充。
9. **MCP Bridge**：動態載入 MCP server 作為 tool 來源。

## 6. 文件導覽

### 6.1 Concepts

核心觀念與系統行為，適合先建立心智模型。

- [Gateway 與 Agent Loop](./concepts/gateway-and-agent-loop.md)：訊息流經整個系統的順序、Gateway 與 core agent 的職責分割、為何兩段分離、完整訊息生命週期。
- [Memory 系統](./concepts/memory-system.md)：`MEMORY.md` / `USER.md` 的 frozen snapshot 設計、字元上限、memory tool（add / replace / remove）、8 個 pluggable memory provider、ContextEngine 壓縮機制。
- [Session 管理](./concepts/session-management.md)：SQLite + FTS5 選擇理由、lineage tracking、平台隔離、`/new`（與 `/reset` alias）行為、session CLI 操作。

### 6.2 跨專案對照

- [Hermes vs OpenClaw](./hermes-vs-openclaw.md)：兩個專案的設計哲學差異 —— harness engineering vs persona 工作站。

## 7. 生態系

在 GitHub 上，Hermes 相關專案：

- **hermes-agent**：核心 repo（Gateway + Agent Loop）。
- **agentskills.io**：開放的 skill 標準，Hermes 也是 reference implementation 之一。
- **claude-code、openclaw**：理念相近的兄弟專案，部分 skill 與 prompt 模式可互通（詳見 [Hermes vs OpenClaw](./hermes-vs-openclaw.md)）。

## 8. 安全性考量

雖然 Hermes 功能強大，但強烈建議使用者操作時保持謹慎：

- **Allowlist 必設**：Hermes 預設 fail-closed，但仍要主動配置平台 allowlist。**生產環境禁用** `GATEWAY_ALLOW_ALL_USERS=true`。
- **Token 不入 git**：API key、bot token 寫進 `~/.hermes/.env`（不要提交到 repo）。
- **Skill 安全掃描**：Skills Hub 安裝會自動掃描；自製 skill 注意 prompt injection 與 destructive command。
- **Sandbox 隔離**：執行任意命令時建議用 `terminal.backend: docker` 或 SSH backend。
- **Pairing 撤銷**：定期 `hermes pairing list` 檢查授權狀態。
- **Port 不對外**：本機部署時把 8642/9119 綁到 `127.0.0.1`，需要對外用 reverse proxy 加認證。
