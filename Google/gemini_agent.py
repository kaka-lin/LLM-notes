import os

from google import genai
from google.genai import types

from wav_utils import wave_file


class GeminiAgent:
    """
    Agent for various tasks via Google Gemini API,
    including ASR, translation, dialogue, Q&A, etc.
    """
    def __init__(
        self,
        model_name: str = "gemini-2.5-flash",
        live_model_name: str = "gemini-live-2.5-flash-preview",
        gemini_api_key: str = "",
        is_live: bool = False,
        is_audio: bool = False,
        temperature: float = 0.0,
        max_output_tokens: int = 100,
        timeout: int = 5,
    ):
        self.model_name = model_name
        self.live_model_name = live_model_name
        self.is_live = is_live
        self.is_audio = is_audio

        # Get agent configurations
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.timeout = timeout

        # Get Gemini API key from config or environment variable
        self.api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Gemini API key is not set. Please provide it in the config "
                "or as an environment variable."
            )

        # Initialize Gemini client
        self.client = genai.Client(api_key=self.api_key)

    def process(self, input_text: str) -> str:
        """使用 Google Gemini API 處理輸入"""
        if self.is_audio:
            return self._live_process_audio(input_text)
        elif self.is_live:
            return self._live_process(input_text)
        else:
            return self._process(input_text)

    def _process(self, input_text: str) -> str:
        """使用 Google Gemini 一般模型 API 處理輸入"""
        # ==================================================================
        #                        FOR ERROR TESTING
        # ==================================================================
        # Instructions: Uncomment the following lines to simulate
        #               a specific Gemini API error for testing purposes.
        # ------------------------------------------------------------------

        # 1. Simulate a Rate Limit Error (HTTP 429)
        # from google.api_core import exceptions
        # raise exceptions.ResourceExhausted(
        #     "Quota exceeded for aiplatform.googleapis.com/generate_content."
        # )
        # ==================================================================

        # ==================================================================
        #                        FOR THINKING CONFIG
        # ==================================================================
        # 2.5 Flash 和 Pro 模型預設啟用「思考」功能，以提升品質，但可能會導致執行時間拉長，並增加符記用量。
        # 使用 2.5 Flash 時，您可以將思考預算設為零，藉此停用思考功能。
        #
        # Turn off thinking:
        # thinking_config=types.ThinkingConfig(thinking_budget=0)
        #
        # Turn on dynamic thinking:
        # thinking_config=types.ThinkingConfig(thinking_budget=-1)
        # ==================================================================

        # Create a chat session, put system prompt in the session
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=input_text,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    thinking_budget=0
                ),  # Disables thinking
                system_instruction="You are a helpful assistant.",
                temperature=self.temperature,
                max_output_tokens=self.max_output_tokens,
            ),
        )

        # The response structure has also changed.
        # It's better to access the text via response.text
        return response.text.strip()

    async def _live_process(self, input_text: str):
        """使用 Google Gemini Live 模型 API 處理輸入"""
        config = {
            "response_modalities": ["TEXT"]
        }

        async with self.client.aio.live.connect(
            model=self.live_model_name, config=config
        ) as session:
            print(f"> {input_text}\n")
            await session.send_client_content(
                turns={"role": "user", "parts": [{"text": input_text}]},
                turn_complete=True
            )

            # For text responses, When the model's turn is complete it
            # breaks out of the loop.
            turn = session.receive()
            async for chunk in turn:
                if chunk.text is not None:
                    print(f'- {chunk.text}')

    @staticmethod
    async def async_enumerate(aiterable):
        """為非同步迭代器加上索引"""
        n = 0
        async for item in aiterable:
            yield n, item
            n += 1

    async def _live_process_audio(self, input_text: str):
        """使用 Google Gemini Live 模型 API 處理輸入"""
        config = {
            "response_modalities": ["AUDIO"]
        }

        async with self.client.aio.live.connect(
            model=self.live_model_name, config=config
        ) as session:
            file_name = 'audio.wav'
            with wave_file(file_name) as wav:
                print(f"> {input_text}\n")
                await session.send_client_content(
                    turns={"role": "user", "parts": [{"text": input_text}]},
                    turn_complete=True
                )

                # For text responses, When the model's turn is complete it
                # breaks out of the loop.
                turn = session.receive()
                async for n, response in self.async_enumerate(turn):
                    if response.data is not None:
                        wav.writeframes(response.data)

                        if n == 0:
                            inline_data = response.server_content.model_turn.parts[0].inline_data
                            print(inline_data.mime_type)
                        print('.', end='')
