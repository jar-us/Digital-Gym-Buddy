import asyncio

from loguru import logger

from google_sheet_manager import GoogleSheetManager
from openai_api_client import OpenAiApiClient
from telegram_interface import TelegramInterface


class GymBuddyApp:
    def __init__(self, telegram_api_token, openai_api_key, sheet_creds_file):
        self.telegram = TelegramInterface(telegram_api_token)
        self.openai_processor = OpenAiApiClient(openai_api_key)
        self.google_sheet_manager = GoogleSheetManager(sheet_creds_file)
        logger.info("GymBuddyApp is ready to rock! 🚀")

    async def run(self):
        offset = None
        logger.info("Listening for messages...")

        while True:
            messages = await self.telegram.get_message(offset=offset)
            for message in messages:

                offset = message.update_id + 1

                if message.message:
                    if message.message.audio is not None:
                        print(
                            f"Received a voice message in chat {message.message.audio.file_id}, but voice processing is not implemented yet.")
                    elif message.message.text:
                        await self.process_text(message)
            await asyncio.sleep(1)

    async def process_voice(self, message):
        logger.info(f"Received voice note: {message}")


    async def process_text(self, message):
        message_text = message.message.text
        chat_id = message.message.chat.id
        logger.info(f"Processing text: {message_text}")

        # 1. Determine what the user wants
        intent = self.openai_processor.determine_intent(message_text)
        logger.info(f"Intent detected: {intent}")

        if intent == "LOG_WORKOUT":
            # A. Extract the data
            workout_data = self.openai_processor.extract_workout_data(message_text)
            logger.info(f"Extracted workout data: {workout_data}")

            success = self.google_sheet_manager.log_workout(workout_data)  # I filled this one in as an example
            logger.info(f"Log workout success: {success}")

            if success:
                await self.telegram.send_text(chat_id, "✅ Workout logged successfully!")
            else:
                await self.telegram.send_text(chat_id, "❌ Error logging workout.")

        elif intent == "QUERY_HISTORY":
            worked_date = self.openai_processor.get_date_from_natural_language(message_text)
            workout_history = self.google_sheet_manager.get_workout_history(worked_date)
            if workout_history:
                response_lines = ["📋 Your Workout History:"]
                for record in workout_history:
                    line = f"- {record['Date']}: {record['Exercise']} - {record['Sets']} sets of {record['Reps']} reps at {record['Weight']} ({record['Comments']})"
                    response_lines.append(line)
                response_text = "\n".join(response_lines)
            else:
                response_text = "No workout history found for the specified date."
            await self.telegram.send_text(chat_id, response_text)
        #
        else:
            # General Chat
            reply = self.openai_processor.generate_chat_response(message_text)
            await self.telegram.send_text(chat_id, reply)
