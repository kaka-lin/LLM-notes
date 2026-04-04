# Langfuse Docker 網路安全與綁定指南

本篇紀錄了如何安全地在 Docker Compose 中配置連通埠，以防止機密資料庫暴露於外部網路。

## 🔒 127.0.0.1 綁定原則 (The Loopback Principle)

在業界標準開發環境中，我們會對基礎設施進行「硬性隔離」：

- **資料庫 (Postgres, Clickhouse, Redis)**：僅監聽 `127.0.0.1` 埠號。這麼做能確保即使您的 Mac 連上了公共 Wi-Fi 或辦公室網域，外界也無法透過任何手段連線到您的資料庫。

- **對外門戶 (Web Portal, Gateway)**：僅開放必要的 Web 存取埠 (如 3000)。如果是為了方便區網測試，通常會考慮使用反向代理或是 Tailscale 加密隧道，而不是直接開放資料庫埠。

## 🌐 服務間的內部網路 (Internal Networking)

在同一個 `docker-compose.yml` 檔案中的容器，會進入同一個「虛擬私有網路」。

- **容器通訊**：當 Web 端需要連接 Postgres 時，它使用的是 `postgres:5432` 這種「容器名稱別名」，走的是 Docker 建立的私有橋接網路。

- **隱密性**：這在實體網卡上是 invisible (不可見) 的，具有極高的安全性。
