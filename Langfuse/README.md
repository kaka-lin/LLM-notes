# Langfuse (AI Observability 觀測平台)

Langfuse 是一個開源的 AI 觀測平台，專門用於監控、評估與優化大語言模型 (LLM) 的應用開發流程。

## 🎯 核心功能

- **Observability**: 紀錄完整 Traces 追蹤 AI 請求生命週期。

- **Evaluation**: 使用人類評分或模型評量機制評估輸出品質。

- **Metrics**: 統計 Token 消耗、費用成本與延遲時效。

- **Prompt Registry**: 在平台管理、測試與版本化 Prompts。

## 🏗️ 技術架構 (V3 版本)

自 V3 版本起，Langfuse 整合了現代化的大數據分析架構，導入多樣化的資料儲存組件：

1. **PostgreSQL**: 核心關聯式資料庫（管理帳號、專案、Prompt）。

2. **ClickHouse**: 高效能列式分析資料庫（儲存 Traces 日誌、大數據統計）。

3. **MinIO (S3)**: 物件儲存 (Object Storage) - 管理附件、圖片、大型 Payload。

4. **Redis**: 快取與異步任務隊列。

## 📚 延伸閱讀 (技術深潛)

- [**數據與儲存架構深潛**](./architecture-deep-dive.md)：ClickHouse、Postgres 與 MinIO 的技術解析。

- [**Docker 網路安全與綁定**](./docker-network-security.md)：127.0.0.1 綁定原則與容器內部網路安全。
