# Miniforge3 vs Miniconda

## 比較概述

| 項目 | Miniforge3 | Miniconda |
|------|------------|-----------|
| 開發者 | 社群 (conda-forge) | Anaconda 公司 |
| 預設通道 | conda-forge | defaults |
| 商業授權 | 無限制，開源友善 | 可能有授權限制 |
| 適用架構 | 支援 Apple Silicon 原生 ARM64 | 有時需透過 Rosetta |
| mamba 支援 | 預裝 | 額外安裝 |
| 使用情境 | 架構開放，套件更新快，適合 Apple M1/M2 | 傳統使用者或需用 Anaconda 套件者 |

## 為什麼推薦 Miniforge3 on Apple Silicon

- 原生支援 `arm64` 架構
- 使用社群套件來源 conda-forge，更新快、支援廣泛
- 避免 Anaconda 商用限制爭議

## 安裝步驟

```bash
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
bash Miniforge3-MacOSX-arm64.sh
# or bash Miniforge3-MacOSX-arm64.sh -b -p <YOU WANTS PATH>
```

## 初始化與切換

```bash
conda init zsh
source ~/.zshrc
```

## 查看架構是否正確

```bash
python -c "import platform; print(platform.machine())"
# 輸出應為 arm64
```
