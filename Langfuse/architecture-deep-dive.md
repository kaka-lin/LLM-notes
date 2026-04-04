# Langfuse V3 技術架構深潛 (Data & Storage)

本篇紀錄了 Langfuse V3 版本中，各個數據組件的運作原理以及為何需要這些技術棧的深度解析。

## 🐘 PostgreSQL (核心關聯式資料庫)

### 核心用途

管理所有的使用者帳號、專案權限關係、API Keys 以及 Prompt 管理。這是整個系統的「大腦」，負責確保資料的強一致性。

### 效能關鍵：Named Volumes

在 Docker 環境下（尤其是 Mac），讀寫資料庫檔案時，主機與容器間的掛載效能是最大的瓶頸。

- **為什麼要 Named Volumes**：它由 Docker 引擎原生管理，繞過了宿主機作業系統的檔案系統同步開銷。

- **效能提升**：能極大幅度提升 PostgreSQL 的 WAL (寫入前日誌) 寫入速度，避免啟動時發生 IO 逾時。

## 🚀 ClickHouse (分析型大數據庫)

ClickHouse 是 Langfuse V3 為了應對百萬量級 Traces 而引入的核心轉變。

### 單機模式 (Standalone) 的技術平衡

Langfuse 預設開發了叢集功能，但在個人或單機部署環境下，啟動 Zookeeper/Keeper 會增加高昂的 **記憶體 (RAM)** 開銷。

- **`CLICKHOUSE_CLUSTER_ENABLED=false`**：透過此變數，讓 ClickHouse 回歸最簡單的 `MergeTree` 引擎。

- **資源效益**：這在不需要跨機器備援的場景下，能以最低的資源換取最高的查詢效能。

## 📦 MinIO (S3 物件儲存)

### 物件與資料庫的分離

在 V2 以前，大檔案 (Media) 與大型 Payload 若存入 PostgreSQL 會造成備份困難且資料庫體積膨脹。

- **角色定位**：MinIO 作為本機端的 S3 替代方案，負責承接所有非結構化的「冷資料」。

- **安全約束**：MinIO 對於 Secret Key 有長度 8 位的強制檢查，這是在設定時最容易被忽略的初始化雷區。

## ⚡ Redis (異步任務與快取)

- **緩衝機制**：Langfuse 使用 Redis 作為消息佇列 (Queue)，將 Web 端收集到的 Traces 先行快取，再由 Worker 定時刷入 ClickHouse。

- **效能優勢**：這樣的設計能確保在高流量併發時，Web 本身不會因為資料庫寫入過慢而變慢。
