import asyncio

from gym_buddy_app import GymBuddyApp
from dotenv import load_dotenv
import os
from loguru import logger

load_dotenv()
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
openai_voice_to_text_api_key = os.getenv("OPENAI_API_KEY")
google_sheet_service_account_file_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE_PATH")
if __name__ == "__main__":
    logger.info("Starting GymBuddyApp...")
    logger.info("Telegram Token loaded. Token length: {}", len(telegram_token) if telegram_token else 0)
    logger.info("OpenAI API Key loaded. Key length: {}", len(openai_voice_to_text_api_key) if openai_voice_to_text_api_key else 0)
    logger.info("Google Sheets Credentials File loaded. File path: {}", google_sheet_service_account_file_path)
    app = GymBuddyApp(
        telegram_api_token=telegram_token,
        openai_api_key=openai_voice_to_text_api_key,
        sheet_creds_file=google_sheet_service_account_file_path
    )

    asyncio.run(app.run())  # Use asyncio.run to execute the coroutine
