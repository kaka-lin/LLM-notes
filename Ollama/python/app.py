import ollama


if __name__ == '__main__':
    response = ollama.chat(
        model='llama3',
        messages=[
            {
                'role': 'user',
                'content': 'Hello Ollama?'
            },
        ])
    print(response['message']['content'])
