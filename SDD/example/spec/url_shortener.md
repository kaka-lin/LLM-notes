# URL Shortener — Spec

## 1. 目的與範圍

提供最小可用的 URL 短網址服務. 不在範圍內: 自訂短碼、過期時間、點擊統計、使用者帳號.

## 2. 名詞定義

- **原始 URL (original URL)**: 使用者送入的完整 URL.
- **短碼 (short code)**: 系統產生的代表字串.
- **對應 (mapping)**: 短碼到原始 URL 的關聯, 持久化於 SQLite.

## 3. 功能需求

- **REQ-001**: 系統應接受 `POST /shorten`, body 為 `{"url": <string>}`, 回傳 `{"short_code": <string>}`.
- **REQ-002**: `short_code` 長度應為 6 個字元, 由 `[a-zA-Z0-9]` 組成.
- **REQ-003**: 重複呼叫同一個原始 URL 應回傳相同 `short_code` (冪等性).
- **REQ-004**: 系統應接受 `GET /{short_code}`, 若存在則 302 重導至原始 URL, 否則 404.

## 4. 限制

- **CON-001**: URL 長度上限為 2048 字元, 超過回傳 400.
- **CON-002**: 無效 URL (缺少 scheme / host) 回傳 400.

## 5. 資料契約

- **DAT-001**: SQLite table `mappings`:

    ```sql
    CREATE TABLE mappings (
        short_code  TEXT PRIMARY KEY,
        original_url TEXT NOT NULL UNIQUE,
        created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```

## 6. 介面契約

- **REQ-001 Request** `POST /shorten`:

    ```json
    { "url": "https://example.com/some/path" }
    ```

- **REQ-001 Response** `200 OK`:

    ```json
    { "short_code": "aB3xZ9" }
    ```

- 錯誤回應一律 `{"error": <message>}` 配合對應 HTTP status.

## 7. 驗收條件

- **AC-001**: POST `/shorten` 同一個 URL 兩次, 兩次回傳的 `short_code` 必須相等 (對應 REQ-003).
- **AC-002**: GET `/abc999` (不存在的 code) 回傳 status 404 (對應 REQ-004).
- **AC-003**: POST `/shorten` 帶 2049 字元的 URL 回傳 status 400 (對應 CON-001).
- **AC-004**: POST `/shorten` 帶 `"not-a-url"` 回傳 status 400 (對應 CON-002).
- **AC-005**: POST `/shorten` 後 GET `/{short_code}` 回傳 302 並指向原始 URL (對應 REQ-004).

## 8. Deferred

- 自訂短碼 (custom alias) — TODO.
- TTL / 過期時間 — TODO.
- 點擊計數 — TODO.
- Rate limit — TODO.
- 多使用者隔離 — TODO.
