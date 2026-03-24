# OpenClaw 安裝指南

OpenClaw 提供多種安裝方式，您可以根據自身需求以及伺服器環境選擇最適合的方法。

## 1. 使用 NPM 安裝 (推薦)

這是最快速且適用於多數使用者的安裝方式。請確保您的環境已有 Node.js：

```bash
npm install -g openclaw@latest
```

## 2. 使用 Docker 安裝

如果您希望將 OpenClaw 運行在容器化環境中以保持系統乾淨，Docker 是非常棒的選擇。我們提供直接取得映像檔或是透過 Docker Compose 組態的兩種方式。

### 方式 A：直接使用 Docker Pull 與 Run (快速容器體驗)

若您不需要客製化設定檔，可直接從 GitHub Container Registry 取得最新映像檔並執行：

```bash
# 1. 取得最新映像檔
docker pull ghcr.io/openclaw/openclaw:latest

# 2. 在背景執行容器 (預設使用 Port 3000)
docker run -d -p 3000:3000 --name openclaw ghcr.io/openclaw/openclaw:latest
```

### 方式 B：使用 Docker Compose (進階管理)

若您需要更完整的環境變數與擴充設定，推薦使用 Docker Compose 進行部署：

1. **確認環境**：請確保系統已安裝 Docker 與 Docker Compose v2，並且至少保留 2 GB 的 RAM 供使用。
2. **複製官方儲存庫並啟動**：

```bash
# 複製官方儲存庫
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 使用 Docker Compose 啟動
docker compose up -d
```

## 3. 從原始碼建構 (進階)

如果您需要完全的控制權或想要修改 OpenClaw，可以從 GitHub 複製原始碼來建構（建議使用 Node.js 24 或 22.16+）：

```bash
# 複製官方儲存庫
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 安裝依賴套件與建構
pnpm install
pnpm build
```
