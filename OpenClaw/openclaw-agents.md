# 關於 openclaw-agents

`openclaw-agents` 是一個專為 OpenClaw 生態系所設計的**多代理 (Multi-agent) 預先設定部署包**。

只要執行簡單的安裝指令，就能一次部署 **9 個擁有各自領域專長的 AI 助理團隊**，而不需要慢慢手動調整每一個系統分工的提示詞。

## 1. 內建的 9 大專業 AI (Core Fleet)

它預設配置了 9 個擁有專屬識別與使命的 AI，例如：

- `main` (主助理)
- `planner` (任務規劃)
- `ideator` (點子發想)
- `critic` (評論員/守門員)
- `surveyor` (資料調研員)
- `coder` (程式工程師)
- `writer` (內容寫手)
- `reviewer` (審閱者)
- `scout` (前邊情報員)

每一個代理都會獲得各自專屬的 `.agents/<agent_id>/` 工作區資料夾，內部皆自帶 `soul.md` (人格設定) 與歷史記憶檔。

## 2. 核心機制與特色

### 2.1 對抗性協作 (Adversarial Collaboration)

專案內建了「SHARP 品鑑節點」的設計思維。不同角色之間不僅會合作，也會互相制衡：

- **發想者 (Ideator) ↔ 評論員 (Critic)**：會互相腦力激盪並檢視點子的可行性。
- **寫手 (Writer) ↔ 審閱者 (Reviewer)**：會在產出正式內容之前先互相審稿。

這種分佈式監督的架構能確保產出的成品質量符合嚴格的標准。

### 2.2 兩種運作模式

- **頻道模式 (Channel Mode)**：讓這群 AI 共同加入您的 Feishu、WhatsApp、Telegram 或 Discord 群組中為您工作。
- **本地工作流模式 (Local Workflow Mode)**：完全不依賴外部通訊軟體。AI 能自動透過內在專屬的 `agentToAgent` 工具進行協商並完成大型任務。

### 2.3 多種實用工作流 (Workflows)

內建多種情境樣板讓代理們可以立刻開工：

- **Paper Pipeline** (論文研讀與摘要產線)
- **Daily Digest** (每日資訊匯總)
- **Brainstorm** (頭腦風暴大會)
- **Rebuttal** (反駁與辯論演練)

### 2.4 安全合併 (Safe Merge)

您可以放心安裝，安裝過程並不會覆蓋或破壞您原本 `OpenClaw` 的基礎設定 (`BOOTSTRAP.md`)，而是以附加的方式融入。

## 3. 快速安裝與使用

若您尚未設定過，可以使用以下腳本一鍵初始化您的多代理團隊：

```bash
# 複製代理工具包
git clone https://github.com/shenhao-stu/openclaw-agents.git
cd openclaw-agents

# 賦予執行權限並執行設定腳本
chmod +x setup.sh
sudo ./setup.sh --channel <您的目標頻道> --group-id <群組ID>
```
