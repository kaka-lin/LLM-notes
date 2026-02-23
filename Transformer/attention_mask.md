# Attention Mask

在 Transformer 模型中，`Attention Mask` 是一個非常重要的機制，它主要用於在 Self-Attention 計算過程中，遮蔽掉那些我們不希望模型關注的資訊。

## 為什麼需要 Attention Mask？

在處理序列資料時，尤其是自然語言處理（NLP）任務，我們經常會遇到以下情況：

1. **Padding Tokens**：為了將不同長度的序列打包成一個批次（batch），我們通常會用特殊的 padding token 將較短的序列填充到與最長序列相同的長度。然而，這些 padding token 本身不包含任何有意義的資訊，我們不希望模型在計算 attention 時考慮它們。

2. **Causal Language Modeling**：在生成式任務中，例如語言模型，模型在預測下一個 token 時，只能看到前面的 token，而不能看到後面的 token。這種單向的特性被稱為 `"causal"` 或 `"autoregressive"`。為了實現這一點，我們需要遮蔽掉當前位置之後的所有 token。

## Attention Mask 的種類

### 1. Padding Mask

- 形狀：通常是 `(batch_size, sequence_length)`。
- 值：`1` 代表「有效 token」，`0` 代表「忽略/屏蔽」。
- 用途：避免模型在 self-attention 中去計算 padding 的位置。

在 attention 計算中，這個 mask 會被應用到 attention scores 上。通常的做法是將 mask 中為 0 的位置對應的 attention score 設為一個非常小的負數（例如 -1e9），這樣在經過 softmax 之後，這些位置的權重就會趨近於 0。

#### Example

假設輸入句子，以 BERT 為例：

```bash
"Hello world" -> [101, 7592, 2088, 102]   # 長度4
"Hi"          -> [101, 7632, 102,   0]    # 補齊成長度4
```
- `[101]`: `[CLS]`（句首標記）
- `[102]`: `[SEP]`（句尾標記）

Attention mask 就會是：

```bash
[1, 1, 1, 1]
[1, 1, 1, 0]
```

### 2. Causal Mask (or Look-ahead Mask) (未來遮罩)

- 在 GPT 這種自回歸模型裡，token 只能看到自己以及前面的 token，不能偷看未來。

- 這會生成一個上三角矩陣的遮罩。

#### Example

對於一個長度為 4 的序列，Causal Mask 會是：

```
[[1, 0, 0, 0],
 [1, 1, 0, 0],
 [1, 1, 1, 0],
 [1, 1, 1, 1]]
```

- 值為 1 的位置表示可以關注。
- 值為 0 的位置表示需要被遮蔽。

同樣地，這個 mask 也會被應用到 attention scores 上，將未來位置的 attention score 設為一個非常小的負數。
