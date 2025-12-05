from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Define the command handler function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # This sends a message back to the user
    await update.message.reply_text(f'Hello {update.effective_user.first_name}!')

# Define the help command handler function
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # This sends a message back to the user
    await update.message.reply_text(f'I am here to help you, {update.effective_user.first_name}!')
    
# Define the message handler function
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # This sends a message back to the user
    await update.message.reply_text(f'You said: _*{update.message.text}*_', parse_mode='MarkdownV2')

# Set up the application
# IMPORTANT: Replace 'YOUR_TOKEN_HERE' with your actual API token
app = ApplicationBuilder().token("8342947440:AAEfKNKDu8xrzXbtFlDVjxQB-E4JkwJARYA").build()

# Connect the command handler to the application
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Run the bot
print("Bot is polling...")
app.run_polling()