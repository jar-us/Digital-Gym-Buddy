from telegram import Update
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

resetButton = InlineKeyboardButton("Reset", callback_data='clear')


# Define the start command handler function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # This sends a message back to the user
    await update.message.reply_text(f'Hello {update.effective_user.first_name}!')


# Define the help command handler function
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # This sends a message back to the user
    await update.message.reply_text(f'I am here to help you, {update.effective_user.first_name}!')


# Define the text message handler function and style the response in MarkdownV2
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # This sends a message back to the user
    count = context.user_data.get('count', 0)
    context.user_data['count'] = count + 1
    await update.message.reply_text(f'You said: _*{update.message.text} Total: {context.user_data['count']}*_',
                                    parse_mode='MarkdownV2', reply_markup=InlineKeyboardMarkup([[resetButton]]))


# Define the cat command handler function to send photo from URL
async def cat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # This handles any errors that occur during the update processing
    await update.message.reply_photo(
        photo='https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg',
        caption='Meow! 🐱'
    )


# Define dog command handler function to send a photo from a local system
async def dog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_photo(
        photo=open('../dog.jpg', 'rb'),
        caption='Woof! 🐶'
    )

async def clear_count(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 1. Get the query info
    query = update.callback_query
    await query.answer()

    # 2. Check the data and perform logic
    if query.data == "clear":
        # YOUR CODE HERE: How do you clear the dictionary?
        context.user_data['count'] = 0
        pass

    # 3. Update the message to show the new state
    await query.edit_message_text(text="Count reset to 0!")


# Set up the application
# IMPORTANT: Replace 'YOUR_TOKEN_HERE' with your actual API token
app = ApplicationBuilder().token("8342947440:AAEfKNKDu8xrzXbtFlDVjxQB-E4JkwJARYA").build()

# Connect the command handler to the application
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.add_handler(CommandHandler("cat", cat))
app.add_handler(CommandHandler("dog", dog))
app.add_handler(CallbackQueryHandler(clear_count))

# Run the bot
print("Bot is polling...")
app.run_polling()
