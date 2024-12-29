import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
import random

# Your bot's API token from BotFather
API_TOKEN = 'API_link'

# List of motivational quotes categorized
quotes = {
    "inspirational": [
        "Duniya madarchod thi madarchod hai aur madarchod rahegi",
    ],
}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Use the environment variable or hardcoded token
TOKEN = API_TOKEN

# Function to start the bot
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Welcome! I'm your motivational quotes bot. Use /quote or /send_pdf_and_images to get a random motivational quote.\n"
        "You can also request specific types of quotes like."
    )

# Function to send a PDF and images
async def send_pdf_and_images(update: Update, context: CallbackContext):    # Define the path to your notes PDF and the folder containing images
    pdf_path = r'C:\Users\darsh\OneDrive\Desktop\python bot\pic\Duniya.pdf'  # Correct path to your PDF file
    image_folder = 'pic'  # Folder where your images are stored
    
    # Collect image paths (only .jpg or .png)
    image_paths = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if filename.endswith(('.jpg', '.png'))]
    
    if not image_paths:
        await update.message.reply_text("No images found to send along with the PDF.")
        return

    # Send the PDF file
    try:
        with open(pdf_path, 'rb') as pdf_file:
            await update.message.reply_document(pdf_file)
    except FileNotFoundError:
        await update.message.reply_text("PDF file not found. Please check the file path.")
        return

    # Send images one by one
    for image_path in image_paths:
        try:
            with open(image_path, 'rb') as image_file:
                await update.message.reply_photo(image_file)
        except FileNotFoundError:
            await update.message.reply_text(f"Image not found: {image_path}")

# Function to handle /quote command
async def quote(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        # If no category is specified, send a random quote
        category = random.choice(list(quotes.keys()))
        await update.message.reply_text(random.choice(quotes[category]))
    else:
        # If a category is specified, send the respective quote
        category = context.args[0].lower()
        if category in quotes:
            await update.message.reply_text(random.choice(quotes[category]))
        else:
            await update.message.reply_text("Sorry, I don't have quotes for that category yet. Try 'inspirational', 'success', or 'life'.")

# Function to handle unknown messages
async def unknown(update: Update, context: CallbackContext):
    await update.message.reply_text("Sorry, I didn't understand that command. Use /quote to get a motivational quote.")

# Main function to run the bot
def main():
    # Create an Application object and pass the bot's token
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quote", quote))
    application.add_handler(CommandHandler("send_pdf_and_images", send_pdf_and_images))  # Add handler for the PDF and images command

    # Register a handler for unknown messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    # Start polling for updates
    application.run_polling()

if __name__ == '__main__':
    main()
