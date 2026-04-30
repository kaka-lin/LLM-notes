# OpenClaw Sandbox 安全執行環境 (Docker-out-of-Docker)

在 OpenClaw 中，AI 代理人 (Agent) 擁有自主編寫程式碼與執行的強大能力。為了防止 LLM 推理層產生幻覺，或是不慎執行具有破壞性的指令（例如刪除檔案）或私自安裝套件，我們啟用了 Sandbox（沙盒）隔離技術。

## 1. 什麼是 Sandbox 沙盒？

> [!NOTE]
> 這是一個「閱後即焚」的無菌實驗室。
> 當 AI 需要測試或執行一段 Python / Node.js 程式碼時：
>
> 1. OpenClaw 會向宿主機借用控制 Docker 的權限。
> 2. 瞬間在背景開出一個全新、獨立的「臨時容器」。
> 3. 任由 AI 在這個臨時環境中盡情執行腳本或安裝依賴。
> 4. 任務結束後，OpenClaw 會立即銷毀該臨時容器。

這確保了所有高風險操作與套件依賴都被限制在隔離空間內，宿主機與核心系統依然能保持乾淨且安全。

## 2. 核心技術：DooD 而非 DinD

很多開發者會直覺以為這叫 Docker-in-Docker，但實際上 OpenClaw 採用的是更安全、效能更好的 **DooD (Docker-out-of-Docker)** 架構（又稱為「兄弟容器」Sibling Containers）。

### ❌ 危險的 DinD (Docker-in-Docker)

代表外層容器的「內部」運行了一套完整的 Docker 引擎。這要求外層容器必須掛載最高風險的 `--privileged` 特權模式，一旦外層容器遭入侵，整個伺服器的安全性將全面瓦解。

### ✅ 安全實踐 DooD (Docker-out-of-Docker)

> [!TIP]
> 我們透過將主機的通訊通訊套接字 `/var/run/docker.sock` 掛載進容器。
> 當 AI 開啟沙盒時，它其實是向宿主機的 Docker Daemon 發出指令，由主機負責產出一個新的沙盒容器。這意味著：
>
> - 沙盒容器與 OpenClaw 伺服器是以「兄弟」身分並列於宿主機上。
> - 完全不需要開啟危險的 `--privileged` 特權模式。
> - 系統管理更為透明，主機可直接監控所有沙盒狀態。

## 3. 防護深度與部署實踐

> [!IMPORTANT]
> 在 Linux 伺服器環境中，直接掛載 `/var/run/docker.sock` 給非 Root 使用者（如 `node`）通常會因為權限不足而引發 `Permission Denied`。

我們在 `setup.sh` 裡透過下列自動化機制解決了這點：

1. **動態 GID 解析**：主動偵測宿主機上 `docker.sock` 的真實群組 ID (`stat -c '%g'`)。
2. **動態注入授權**：將偵測到的 GID 寫入 `docker-compose.sandbox.yml` 並利用 `group_add` 將 `node` 使用者納入 Docker 授權。
3. **零信任防禦 (Zero-Trust)**：最重要的防線在於，若未在 `.env` 中開啟 `OPENCLAW_SANDBOX=1`，這些 Socket 綁定與授權機制打從一開始就不會生效，達到了真正的按需授權。

## 4. 實務挑戰與踩坑紀錄 (Troubleshooting)

雖然 DooD 架構設計精良，但在不同作業系統與網路環境下仍有一些常見限制：

> [!CAUTION]
> 在本專案目前的現階段開發中，我們**暫時將 `OPENCLAW_SANDBOX` 預設設為 `0`**，主要的目的是避免讓使用者陷入 Docker 權限與網路隔離的複雜排錯中，確保主流程（如 Browser 控制）能優先跑通。

### 常見問題 A：Docker Desktop (macOS) 的共享路徑限制

這是 macOS 獨有的限制。當沙盒嘗試掛載的主機路徑（Host Path）不位在 Docker Desktop 的 「File Sharing」白名單內時，掛載會失敗。

- **報錯現象**：`The path ... is not shared from the host and is not known to Docker.`

### 常見問題 B：Docker Runtime 依賴性

沙盒執行依賴於環境中具備正確的 `docker` 指令執行能力。如果 Agent 容器內部缺乏可用指令，會導致沙盒執行失敗。

- **報錯現象**：`Sandbox mode requires Docker, but the "docker" command was not found in PATH.`

### 常見問題 C：網路隔離與 DNS 解析

沙盒與瀏覽器執行環境會引入獨立的網路與 DNS 邊界。這可能導致：

- 常見的 `ENETUNREACH` 網路不可達錯誤。
- 無法解析特定的外部網域（如 Threads, Telegram）。
- **報錯現象**：`Could not resolve host` 或 `ENETUNREACH`。

### 常見問題 D：隔離環境下的服務控制

在受限的沙盒環境下，Agent 若嘗試跨越邊界去控制宿主機服務（如 CDP 遠端瀏覽器偵錯）可能會失敗。

- **報錯現象**：`Failed to bind socket: Operation not permitted`。

---

**相關參考：**

- [詳細部署深度研究 (OpenClaw Server)](https://github.com/kaka-lin/openclaw-server/tree/main/docs/deployment/setup-deep-dive.md)
- [OpenClaw 核心原理與架構筆記 (LLM-notes)](../README.md)
