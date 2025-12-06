from telegram import Bot
import asyncio
from loguru import logger


class TelegramInterface:
    def __init__(self, api_token):
        self.api_token = api_token
        self.TelegramBotClient = Bot(token=api_token)
        logger.info("TelegramInterface initialized.")

    async def send_text(self, chat_id, text):
        try:
            logger.info(f"Sending message to {chat_id}: {text}")
            await self.TelegramBotClient.send_message(chat_id=chat_id, text=text)
        except Exception as e:
            logger.info(f"Error sending message: {e}")

    async def get_message(self, offset=None):
        try:
            logger.info(f"Asking Telegram for new messages.")
            return await self.TelegramBotClient.get_updates(offset=offset, timeout=30, allowed_updates=["message"])
        except Exception as e:
            logger.info(f"Error fetching messages from Telegram: {e}")
            return []

    async def download_file_locally(self, file_id):
        try:
            print(f"Getting file with ID: {file_id}")
            file_info = await self.TelegramBotClient.get_file(file_id)
            file_path = await file_info.download_to_drive(f"digital_gym_buddy_voice_note_downloaded_{file_id}")
            return file_path
        except Exception as e:
            print(f"Error getting file: {e}")
            return None
