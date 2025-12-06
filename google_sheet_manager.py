from datetime import datetime

import gspread
from loguru import logger

class GoogleSheetManager:
    def __init__(self, credentials_file_path):
        self.client = gspread.service_account(filename=credentials_file_path)
        self.spreadsheet = self.client.open('Gym Data')
        self.worksheet = self.spreadsheet.worksheet('Sheet1')
        logger.info(f"Google Sheet loaded. Worksheet ID: {self.worksheet.id}")

    def get_workout_history(self, workout_date=None):
        try:
            records = self.worksheet.get_all_records()
            if workout_date:
                filtered_records = [record for record in records if record['Date'] == workout_date]
                return filtered_records
            return records
        except Exception as e:
            logger.error(f"Error retrieving workout history: {e}")
            return []

    def log_workout(self, workout_data):
        current_date = datetime.now().strftime("%Y-%m-%d")

        row_to_append = [
            current_date,
            workout_data.get("exercise"),
            workout_data.get("sets"),
            workout_data.get("reps"),
            workout_data.get("weight"),
            workout_data.get("comments")
        ]

        try:
            self.worksheet.append_row(row_to_append)
            return True
        except Exception as e:
            logger.error(f"Error logging workout: {e}")
            return False