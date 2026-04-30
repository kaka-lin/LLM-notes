# OpenClaw

OpenClaw 是一個免費且開源的自主 AI 代理（Autonomous AI Agent），利用大語言模型（LLM）來執行各種廣泛的任務。它最初由 Peter Steinberger 以「Clawdbot」為名發布，讓使用者能在自己的裝置上運行專屬的個人 AI 助理。

## 1. 概覽

OpenClaw 能夠與多種通訊平台整合，例如 WhatsApp、Telegram、Slack 以及 Discord。它可以理解使用者的指令，並使用您所選擇的外部 LLM 來進行回覆與處理，支援的模型包含 Claude、DeepSeek 或 OpenAI 的 GPT 系列模型等。

## 2. 主要特色

- **多樣化的任務執行**：能執行各種任務，從網頁搜尋、資料摘要，到解決 GitHub Issues 以及建立 Pull Requests。

- **平台整合**：與主流的通訊軟體無縫接軌。

- **模型彈性**：支援將請求路由 (Routing) 至不同的外部 LLM，讓使用者可以針對效能或成本進行最佳化。

## 3. 安裝指南

- [OpenClaw 完整安裝指南 (openclaw-server)](https://github.com/kaka-lin/openclaw-server/tree/main/docs/deployment/setup.md)

## 4. 實作與部署 (Implementation)

關於本機環境的具體設定（如 Telegram Bot、瀏覽器控制等），請參考：

- [OpenClaw 專案文件中心 (openclaw-server)](https://github.com/kaka-lin/openclaw-server/tree/main/docs/README.md)

## 5. 使用方式與範例

### 5.1 啟動基礎代理伺服器

安裝完成後，您可以使用以下指令來初始化並安裝背景執行常駐程式 (Daemon)，這會讓您的 AI 代理保持在背景持續運作：

```bash
openclaw onboard --install-daemon
```

### 5.2 客製化代理人與人格設定 (SOUL.md)

OpenClaw 核心內建強大的多代理 (Multi-agent) 路由能力。您可以透過建立 `SOUL.md` 檔案來定義 AI 的「人格」與主要任務，並直接原生打造專屬的自動化工作流（例如浪live自動引流腳本）。

- **詳細設定與範例**：請參閱內建的 [代理人設計細節 (Built-in Agents)](./guides/built-in-agents.md)。

## 6. 架構系統

OpenClaw 的架構主要由四個層次組成：

1. **Gateway (閘道層)**：負責處理來自各個平台的訊息調度與串接。

2. **Reasoning (推理層)**：使用連接的 LLM 來處理與推論請求內容。

3. **Memory (記憶系統)**：在不同的互動過程中提供持久化的上下文 (Context) 記憶。

4. **Skills & Execution (技能與執行層)**：負責採取實際行動（例如：執行程式碼、網頁搜尋等）。

## 7. 文件導覽

### 7.1 Concepts

核心觀念與系統行為，適合先建立心智模型。

- [會話隔離與重置機制 (Session Management)](./concepts/session-management.md)：Session Key 隔離、`/new` 與 `/reset` 指令、記憶系統（MEMORY.md、Daily Notes、Dreaming）、各平台最佳實踐。

- [Heartbeat 心跳機制](https://github.com/kaka-lin/openclaw-server/tree/main/docs/guides/heartbeat-config.md)：Gateway 定時喚醒的執行與投遞分離設計、Multi-Agent 繼承規則、`HEARTBEAT.md` 用法與省錢技巧。

- [自動化與 Cron 排程](https://github.com/kaka-lin/openclaw-server/tree/main/docs/guides/automation-config.md)：Cron Job 設定方式（聊天 / CLI）、排程類型、與 Heartbeat 的選擇判斷。

- [Skills 與 ClawHub](./concepts/skills-and-clawhub.md)：技能系統的建立、管理與市集運作。

### 7.2 Guides

操作指南與日常查閱，適合需要「怎麼做」時使用。

- [代理人設計細節 (Built-in Agents)](./guides/built-in-agents.md)：SOUL.md、agent 目錄架構與多代理協作。

- [斜線指令 (Slash Commands) 指南](./guides/slash-commands-guide.md)：純文字指令與原生指令的差異、核心內建指令、權限認證機制。

- [OpenClaw Tools 內建工具整理](./guides/openclaw-tools-guide.md)：詳細介紹內建工具分類 (Runtime, Browser, Web, FS, Sessions 等) 與其查詢方式。

### 7.3 Reference

規格型文件，適合實作整合或查 API 細節。

- [OpenClaw APIs 呼叫指南](./reference/openclaw-apis.md)：提供 OpenAI 相容 API、原生 OpenResponses API 與 Tools Invoke API 的完整規範。

### 7.4 Deployment

部署、安全與網路設定。

- [Sandbox 隔離架構說明](./deployment/sandbox-architecture.md)：分析 OpenClaw 如何透過 Sandbox 與 Docker 進行執行環境隔離。

- [Docker 網路綁定與部署](./deployment/docker-network-binding.md)：關於 Docker 網路通訊、容器連結與對外開放連接埠的詳細說明。

### 7.5 Best Practices

開發經驗與設計心法。

- [Skill 開發與設計心法](./best-practices/skill-development.md)：Skill prompt、安全邊界、metadata gating 與測試流程。

## 8. 生態系

在 GitHub 上，OpenClaw 專案包含了幾個相關的儲存庫：

- **OpenClaw-RL**：專為訓練個人化 AI 代理所設計的強化學習 (Reinforcement Learning) 框架。

- **ClawRouter**：專為 OpenClaw 打造的 LLM 路由器，用於優化模型選擇並大幅降低成本。

- **Claw Hub**：一個外掛程式與擴充技能的市集。

## 9. 安全性考量

雖然 OpenClaw 功能強大，但強烈建議使用者在操作時保持謹慎：

- **外掛安全**：在 Claw Hub 中曾發現過惡意外掛，安裝前請務必驗證其安全性。

- **環境隔離**：執行代理程式時，建議使用安全的實驗方式，例如容器隔離 (Container Isolation)。

- **避免直接曝露憑證**：請勿將 API Keys 等機密資訊直接寫在腳本中。

- **NemoClaw**：NVIDIA 提供了一個名為 NemoClaw 的開源參考堆疊 (Reference Stack)，可以進一步提升執行 OpenClaw 時的安全性。
