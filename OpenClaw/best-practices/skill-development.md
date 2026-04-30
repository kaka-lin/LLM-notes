# Skill 開發與設計心法 (Best Practices)

開發 OpenClaw Skill 時，除了滿足格式規範（如 `SKILL.md` 的 YAML 宣告），更重要的是設計出「直覺、安全且易於維護」的 AI 指令。
以下整理自官方文件與 `langlive-growth-engine` 專案開發過程中的血淚實戰經驗。

## 1. Prompt 撰寫心法：精簡與明確

相較於過去寫粗略的人設，在 Skill 開發中更講求「工程化指示」。

- **要精簡直接**：告訴模型「你要做什麼 (Instruct on what to do)」，而不是花費長篇大論叫它「扮演成什麼樣的 AI」。
- **步驟絕對化**：把複雜流程切分為 `步驟 1`、`步驟 2`。建議在 `SKILL.md` 的每個步驟開頭，強制模型先 `[輸出當前狀態進度]`，讓你能隨時追蹤。
- **人設抽離**：將純業務邏輯寫在主 `SKILL.md` 中；如果需要客製化大量的對話語氣，把這部分的 prompt 分拆到 `SOUL.md` 或其他 bootstrap 檔，保持主檔簡潔乾淨。

## 2. 安全性第一 (Safety First)

很多自動化腳本會用到外部終端指令（例如呼叫 Python 或 Bash 腳本）。

- **防禦 Command Injection**：如果在 `SKILL.md` 中允許模型組合自訂文字去執行 `exec` 或 `bash` 工具，請確保提示詞能防堵未受信任的使用者輸入被惡意當成指令執行。
- **依賴門檻清楚**：用 `metadata.openclaw.requires.bins` / `requires.env` / `requires.config` 宣告載入條件，讓缺少依賴的環境不會載入該 Skill。這只是 load-time gating，不等於 OS 權限控制；涉及 `exec`、`bash` 或外部腳本時，仍要搭配 sandbox、allowlist 與明確的工具邊界。

## 3. 開發與測試循環模式

千萬不要在沒有經過測試的情況下直接丟上線。

1. **獨立測試 Prompt**：在本地環境使用 CLI 快速驗證你的腳本邏輯是否通順。
   - 測試指令：`openclaw agent --message "觸發關鍵字..."`
2. **驗證 Metadata 依賴**：在沒有具備環境變數或相依執行檔的機器上跑一次，觀察系統是否有正確的拒絕啟動，確保 Gating 機制運作正常。
3. **佈署與發布**：等到在本地端測試都能穩定發揮後，這時再將整個資料夾透過 ClawHub 封裝發布，讓其他環境也能 `openclaw skills update` 享受這些功能。
