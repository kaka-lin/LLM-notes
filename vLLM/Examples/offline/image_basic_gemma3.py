import os
from pathlib import Path

from PIL import Image
from transformers import AutoProcessor
from vllm import LLM, SamplingParams

os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def run_gemma3(
    image_path: str,
    model_name: str = "google/gemma-3-4b-it",
):
    """
    使用 Gemma 3 (google/gemma-3-4b-it) 模型描述單張圖片的內容。

    這個函式會載入指定的 Gemma 3 多模態模型，處理輸入的圖片，
    並產生一段詳細的圖片描述文字，最後將結果印出。

    Args:
        image_path (str): 要描述的圖片檔案路徑。
        model_name (str, optional):
            要使用的 Hugging Face 模型名稱。
            預設為 "google/gemma-3-4b-it"。
    """

    # 1. 初始化 vLLM
    llm = LLM(
        model=model_name,
        max_model_len=8192,   # Gemma 3 建議的 context size，可依你的 GPU 調整
        dtype="auto",
        trust_remote_code=True,
    )

    # 2. 載入圖片
    img_path = Path(image_path)
    img = Image.open(img_path).convert("RGB")

    # 3. 使用 AutoProcessor 產生符合 Gemma 3 chat template 的文字 prompt
    processor = AutoProcessor.from_pretrained(model_name)

    user_text = "Please describe this image in detail."

    # 這裡的 "image" 欄位只是一個 placeholder（不需要放真正的內容），
    # 真正的影像會透過 multi_modal_data 傳給 vLLM。
    chat_message = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": "image_1"},
                {"type": "text", "text": user_text},
            ],
        },
        {
            "role": "assistant",
            "content": [],
        },
    ]

    prompt = processor.apply_chat_template(
        chat_message,
        tokenize=False,
        add_generation_prompt=True,
    )

    # 4. sampling 參數
    sampling_params = SamplingParams(
        temperature=0.0,
        top_p=1.0,
        max_tokens=256,
    )

    # 5. 呼叫 vLLM（注意：image 一樣要是 list）
    outputs = llm.generate(
        {
            "prompt": prompt,
            "multi_modal_data": {"image": [img]},
        },
        sampling_params,
    )

    print(outputs[0].outputs[0].text)


if __name__ == "__main__":
    # 使用名為 "test.jpg" 的圖片進行測試
    run_gemma3("test.jpg")
