# OpenClaw

OpenClaw 是一個免費且開源的自主 AI 代理（Autonomous AI Agent），利用大語言模型（LLM）來執行各種廣泛的任務。它最初由 Peter Steinberger 以「Clawdbot」為名發布，讓使用者能在自己的裝置上運行專屬的個人 AI 助理。

## 概覽

OpenClaw 能夠與多種通訊平台整合，例如 WhatsApp、Telegram、Slack 以及 Discord。它可以理解使用者的指令，並使用您所選擇的外部 LLM 來進行回覆與處理，支援的模型包含 Claude、DeepSeek 或 OpenAI 的 GPT 系列模型等。

## 主要特色

- **多樣化的任務執行**：能執行各種任務，從網頁搜尋、資料摘要，到解決 GitHub Issues 以及建立 Pull Requests。
- **平台整合**：與主流的通訊軟體無縫接軌。
- **模型彈性**：支援將請求路由（Routing）至不同的外部 LLM，讓使用者可以針對效能或成本進行最佳化。

## 安裝指南

OpenClaw 提供多種安裝方式，包含 NPM、Docker Compose 以及從原始碼建構。

詳細的安裝步驟與環境需求，請參閱 [setup.md](./setup.md)。

## 使用方式與範例

### 1. 啟動基礎代理服務器

安裝完成後，您可以使用以下指令來初始化並安裝背景執行常駐程式 (Daemon)，這會讓您的 AI 代理保持在背景持續運作：

```bash
openclaw onboard --install-daemon
```

### 2. 建立客製化代理與自動化工作流

OpenClaw 核心內建強大的多代理（Multi-agent）路由能力。您可以透過基礎的設定檔或安裝 Marketplace 中的 Plugins，直接原生打造專屬的自動化任務（例如我們設計的浪live自動引流腳本）。

> **延伸參考：社群外部開源專案 `openclaw-agents`**
>
> 針對極度複雜的大型專案，若您不想從零設定，社群提供了一個獨立的目標儲存庫名為 `openclaw-agents`。該專案預設封裝了 9 個各司其職的 AI 角色。請注意，這是一個外部開發的擴充包，與 OpenClaw 輕便的原生體驗不同。詳情請移步參閱 [openclaw-agents.md](./openclaw-agents.md)。

### 3. 自訂代理人格 (建立 SOUL.md)

當您將 OpenClaw 部署到 GitHub 或是作為獨立助理時，您可以在環境中建立一個 `SOUL.md` 檔案來定義該 AI 的「人格」與主要任務。例如：

```markdown
# Agent Identity

你是一個資深的開源專案維護者。
你的任務是自動審查 GitHub 上的 Pull Requests，並對新的 Issues 提供初步的分類與友善的回覆。
```

AI 代理在回覆訊息與分析問題時，就會嚴格遵守 `SOUL.md` 中所定義的規則。

## 架構

OpenClaw 的架構主要由四個層次組成：

1. **Gateway（閘道層）**：負責處理來自各個平台的訊息調度與串接。
2. **Reasoning（推理層）**：使用連接的 LLM 來處理與推論請求內容。
3. **Memory（記憶系統）**：在不同的互動過程中提供持久化的上下文（Context）記憶。
4. **Skills & Execution（技能與執行層）**：負責採取實際行動（例如：執行程式碼、搜尋網頁等）。

## 生態系

在 GitHub 上，OpenClaw 專案包含了幾個相關的儲存庫：

- **OpenClaw-RL**：專為訓練個人化 AI 代理所設計的強化學習（Reinforcement Learning）框架。
- **ClawRouter**：專為 OpenClaw 打造的 LLM 路由器，用於優化模型選擇並大幅降低成本。
- **Claw Hub**：一個外掛程式與擴充技能的市集。

## 安全性考量

雖然 OpenClaw 功能強大，但強烈建議使用者在操作時保持謹慎：

- **外掛安全**：在 Claw Hub 中曾發現過惡意外掛，安裝前請務必驗證其安全性。
- **環境隔離**：執行代理程式時，建議使用安全的實驗方式，例如容器隔離（Container Isolation）。
- **避免寫死憑證**：請勿將 API Keys 等機密資訊寫死在腳本中。
- **NemoClaw**：NVIDIA 提供了一個名為 NemoClaw 的開源參考堆疊（Reference Stack），可以進一步提升執行 OpenClaw 時的安全性。
