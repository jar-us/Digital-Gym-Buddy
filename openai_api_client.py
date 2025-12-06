from datetime import datetime
from typing import List, Dict, Any

from openai import OpenAI
from loguru import logger
import json
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageParam, ChatCompletionSystemMessageParam, \
    ChatCompletionUserMessageParam


class OpenAiApiClient:
    def __init__(self, api_key):
        self.api_client = OpenAI(api_key=api_key)
        logger.info("Open AI client initialized.")

    # def transcribe_audio(self, audio_path):
    #     # We open the file in "read binary" (rb) mode
    #     with open(audio_path, "rb") as audio_file:
    #         transcription = self.client.audio.transcriptions.create(
    #             file=audio_file,
    #             model="whisper-1"
    #         )
    #         return transcription.text

    def generate_chat_response(self, text: str):
        messages: list[ChatCompletionMessageParam] = [
            ChatCompletionSystemMessageParam(
                role="system",
                content="""
                You are 'GymBuddy', an enthusiastic and supportive personal trainer. 
                Your goal is to motivate the user to stay consistent with their workouts.
                - Tone: High-energy, friendly, and concise. Use emojis occasionally (e.g., 💪, 🏃‍♂️).
                - Behavior: If the user is tired, emphasize the importance of recovery. If they succeed, celebrate their win.
                - Constraint: Keep responses under 3 sentences unless asked for a detailed explanation.
                """
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=text
            )
        ]

        logger.info(f"Generating chat response for message: {messages}")

        response = self.api_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Return the cleaned-up result
        return response.choices[0].message.content.strip()

    def determine_intent(self, text: str):
        messages: list[ChatCompletionMessageParam] = [
            ChatCompletionSystemMessageParam(
                role="system",
                # content="You are a helpful assistant. Classify the user's input into one of these categories: LOG_WORKOUT, QUERY_HISTORY, GENERAL_CHAT. Return only the category name."
                content= (
                    "You are a helpful assistant. Classify the user's input into one of these categories: "
                    "LOG_WORKOUT (if the user is providing workout details to log), "
                    "QUERY_HISTORY (if the user is asking about past workouts or workout history), "
                    "GENERAL_CHAT (if the input is general conversation). "
                    "Return only the category name."
                )
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=text
            )
        ]

        logger.info(f"Determining intent for message: {messages}")

        response = self.api_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Return the cleaned-up result
        return response.choices[0].message.content.strip()

    def extract_workout_data(self, text):
        system_prompt = """
        You are a fitness assistant. Extract workout details from the user's text.
        Return ONLY a raw JSON object with the following keys:
        - "exercise": (string) name of the exercise
        - "sets": (integer) number of sets
        - "reps": (integer) number of reps
        - "weight": (string) weight used (e.g., '80kg')
        - "comments": (string) any other notes, or null if none

        Do not output markdown code blocks. Just the JSON.
        """

        messages: list[ChatCompletionMessageParam] = [
            ChatCompletionSystemMessageParam(
                role="system",
                content=system_prompt
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=text
            )
        ]

        response = self.api_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        json_string = response.choices[0].message.content.strip()

        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            logger.info(f"Failed to decode JSON: {json_string}")
            return {}

    def get_date_from_natural_language(self, text):
        today_str = datetime.now().strftime("%Y-%m-%d")

        messages: list[ChatCompletionMessageParam] = [
            ChatCompletionSystemMessageParam(
                role="system",
                content=f"Today is {today_str}. Convert the time reference in the user's text to a YYYY-MM-DD date. Return ONLY the date string."
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=text
            )
        ]
        # 3. Call the API
        response = self.api_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        return response.choices[0].message.content.strip()
