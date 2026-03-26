# OpenClaw 安裝指南

OpenClaw 提供多種安裝方式，您可以根據自身需求以及伺服器環境選擇最適合的方法。

## 1. 使用 NPM 安裝 (推薦)

這是目前最快速且簡單的安裝方式。請確保您的環境已有 Node.js (22.16+ / 24+)：

```bash
npm install -g openclaw@latest
```

## 2. 使用 Docker 安裝 (官方推薦)

如果您希望在容器化環境中運行以保持系統乾淨，這是最完整的部署方式，會自動引導您完成 Token 產生與初始化設定。

### 方式 A：使用官方 Docker 腳本 (推薦)

```bash
# 1. 複製官方儲存庫
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 2. 指定映像檔版本並執行設定腳本
export OPENCLAW_IMAGE="ghcr.io/openclaw/openclaw:latest"
./scripts/docker/setup.sh
```

### 方式 B：直接使用 Docker Run (快速體驗)

若您不需要持久化設定檔，可直接執行：

```bash
docker run -d -p 3000:3000 --name openclaw ghcr.io/openclaw/openclaw:latest
```

### 方式 C：使用 Docker Compose (手動管理)

如果您需要直接透過 YAML 控制環境變數：

1. **複製儲存庫**：`git clone https://github.com/openclaw/openclaw.git`
2. **啟動服務**：`docker compose up -d`

## 3. 從原始碼建構 (進階開發)

如果需要修改 OpenClaw 程式碼：

```bash
# 複製原始碼
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 安裝依賴並建構
pnpm install
pnpm build
```
