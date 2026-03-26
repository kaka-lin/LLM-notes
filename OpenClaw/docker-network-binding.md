# OpenClaw Docker 網路綁定與執行模式 (LAN vs Loopback)

在 Docker 環境下部署 OpenClaw 時，網路介面綁定 (Network Binding) 非常重要。錯誤的綁定會導致無法從外部（例如 Mac 實體機的瀏覽器）連線到容器內的 Gateway API 或儀表板。

## 1. 網路綁定 (Network Binding)

OpenClaw 透過環境變數 `OPENCLAW_GATEWAY_BIND` 來決定 Gateway 的監聽策略：

### `lan` (Local Area Network) - 推薦設定

- **設定方式**：`OPENCLAW_GATEWAY_BIND=lan`
- **作用**：允許 Gateway 綁定到所有網路介面（相當於 `0.0.0.0`）。
- **結果**：搭配 `docker-compose.yml` 的 `ports: ["18789:18789"]`，您可以從 Host 主機的瀏覽器輸入 `http://127.0.0.1:18789` 順利存取 Control UI。這也是官方 `setup.sh` 安裝腳本預設會採用的防呆設定。

### `loopback` (預設安全限制)

- **設定方式**：`OPENCLAW_GATEWAY_BIND=loopback`
- **作用**：嚴格鎖死只綁定在 `127.0.0.1`，不對外開放。
- **結果**：只有「和這個容器身處同一個 Docker 內部網路」的其他容器能存取它。您的 Host 電腦（Mac）若嘗試用 `curl` 或瀏覽器連線，會遭到 `Connection reset by peer` 的拒絕。

## 2. 執行模式 (Gateway Mode)

您可能會在文件中看到 `--mode local` 或是 `gateway.mode=local` 的設定。

- **作用**：這與 IP 網路綁定無關，而是決定核心架構的部署方式。
- **意義**：`local` 模式代表您要把「Gateway（負責對外通訊）」與「Agent（負責執行思考與操作的 AI）」全包在同一個實體（或同個 Docker 容器）內運作。這對於個人開發環境或輕量級伺服器而言是標準的配置方式。

## 3. 常見問題排除

**當您遇到 `curl: (56) Recv failure: Connection reset by peer`：**

1. 請確認 `.env` 中有設定 `OPENCLAW_GATEWAY_BIND=lan`。
2. 確認 `docker-compose.yml` 有透過 `env_file: - .env` 載入設定。
3. 如果剛剛改完設定，務必要徹底重建容器：

    ```bash
    docker compose down
    docker compose up -d
    ```

4. 利用 `docker compose logs | grep "listening on"` 確認是否有正確綁定到 `0.0.0.0`。
