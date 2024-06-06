import os
from pathlib import Path

import anthropic
import base64
import httpx


if __name__ == "__main__":
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(
        # 預設為 os.environ.get("ANTHROPIC_API_KEY")
        api_key=api_key
    )

    # Image
    image_url = "https://raw.githubusercontent.com/kaka-lin/EfficientSAM-tf2-demo/main/images/dogs.jpg"
    image_media_type = "image/jpeg"
    image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image_media_type,
                            "data": image_data,
                        },
                    }
                ],
            }
        ],
    )
    print(message)

    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Hello!",
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": Path(__file__).parent.joinpath("images/dogs.jpg"),
                        },
                    },
                ],
            },
        ],
        model="claude-3-opus-20240229",
    )
    print(message.model_dump_json(indent=2))
