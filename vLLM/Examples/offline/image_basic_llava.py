import os
from pathlib import Path

from PIL import Image
from vllm import LLM, SamplingParams

os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def run_llava(
    image_path: str,
    model_name="llava-hf/llava-1.5-7b-hf"
):
    """
    使用 LLaVA 模型描述單張圖片的內容。

    這個函式會載入指定的 LLaVA 模型，處理輸入的圖片，
    並產生一段詳細的圖片描述文字，最後將結果印出。

    Args:
        image_path (str): 要描述的圖片檔案路徑。
        model_name (str, optional):
            要使用的 Hugging Face 模型名稱。
            預設為 "llava-hf/llava-1.5-7b-hf"。
    """
    # 1. 初始化 vLLM（無須 processor）
    llm = LLM(
        model=model_name,
        max_model_len=4096,
        dtype="auto",
        trust_remote_code=True,  # LLaVA 需要 remote code
    )

    # 2. 讀圖片
    img_path = Path(image_path)
    img = Image.open(img_path).convert("RGB")

    # 3. 定義 LLaVA 模型的提示模板 （prompt）
    prompt = (
        "USER: <image>\n"
        "Please describe this image in detail.\n"
        "ASSISTANT:"
    )

    # 4. sampling
    sampling_params = SamplingParams(
        temperature=0.0,
        top_p=1.0,
        max_tokens=256,
    )

    # 5. vLLM 呼叫（注意：image 要是 list）
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
    run_llava("test.jpg")
