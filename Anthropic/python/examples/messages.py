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

    # Message
    message = client.messages.create(
        model="claude-3-opus-20240229", # 模型型號
        max_tokens=1024, # 選用，回傳token的最大長度，避免爆預算
        messages=[
            {"role": "user", "content": "我想學習 deep learning 要從哪邊下手"}
        ]
    )
    print(message.content)

    message_dict = message.model_dump()
    # Checking if the response has a content field which is a list
    if "content" in message_dict and isinstance(message_dict["content"], list):
        # Extracting the text from each TextBlock in the content list
        formatted_output = "\n".join(text_block["text"] for text_block in message_dict["content"] if "text" in text_block)
        # Writing the formatted output to a text file
        with open("output.txt", "w") as file:
            file.write(formatted_output)
        print("Output has been successfully saved to 'output.txt'.")
    else:
        print("Response content is not in the expected list format:", message_dict)
