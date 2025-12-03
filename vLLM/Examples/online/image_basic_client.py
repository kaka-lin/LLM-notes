import time
import argparse
import base64

from pathlib import Path
from openai import OpenAI


def load_image_as_data_url(path: str) -> str:
    """把 local 圖片轉成 data:image/...;base64,xxx 格式"""
    p = Path(path)

    if not p.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    ext = p.suffix.lower()
    if ext in [".jpg", ".jpeg"]:
        mime = "image/jpeg"
    elif ext == ".png":
        mime = "image/png"
    else:
        raise ValueError(f"Unsupported image type: {ext}")

    with open(p, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    return f"data:{mime};base64,{b64}"


def main(image_source: str):
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="unused",
    )

    # 如果是 URL 就照用；如果是 local 檔案就轉成 data URL
    if image_source is None:
        image_url = "https://cdn.17app.co/F14CAC10-49A4-4136-BB89-6CB290534EEF.jpg"
    else:
        if image_source.startswith("http://") or image_source.startswith("https://"):
            image_url = image_source
        else:
            image_url = load_image_as_data_url(image_source)

    start_time = time.time()
    response = client.chat.completions.create(
        model="google/gemma-3-4b-it",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI assistant with strong image understanding. "
                    "Describe the image in clear, concise traditional Chinese."
                ),
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "請幫我用繁體中文詳細描述這張圖片的內容、場景與人物。",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        },
                    },
                ],
            },
        ],
        max_tokens=512,
        temperature=0.0,
    )

    print(f"\nRequest took {(time.time() - start_time) * 1000:.0f} ms.")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image",
        type=str,
        help="URL or local image file path",
    )
    args = parser.parse_args()

    main(args.image)
