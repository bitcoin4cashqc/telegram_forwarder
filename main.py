from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Add your bot token
TOKEN = "7405006462:AAF1elX7mAZpKJeGXOTtsSrhVsVd_rXfgx8"

# List of groups/channels to forward the messages to (either username or chat ID)
TARGET_GROUPS = [
    {"chat_id": -1002375678860, "topic_id": None},  # Group with no topic
    {"chat_id": -1002370612441, "topic_id": 40},  # Group with no topic
    {"chat_id": -1002293550563, "topic_id": None},  # Private Channel
    
    
]
# List of users whose messages will be forwarded (optional, relevant for groups)
ALLOWED_USERS = ["SoliditySam"]





async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Bot started! It will forward messages from this group or channel.")

# Function to get the group/channel ID
async def get_group_id(update: Update, context: CallbackContext):
    user = update.message.from_user.username if update.message.from_user else None

    # Check if the user is in the allowed list (only applicable for groups)
    if ALLOWED_USERS and user and user not in ALLOWED_USERS:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    # Get the ID of the group/channel
    chat_id = update.message.chat.id
    chat_title = update.message.chat.title if update.message.chat.title else "This chat"
    await update.message.reply_text(f"The ID of {chat_title} is: {chat_id}")

    if update.message.message_thread_id:
            topic_id = update.message.message_thread_id
            await update.message.reply_text(f"Topic ID: {topic_id}")

# Function to handle forwarded messages and extract channel ID
async def handle_forwarded_message(update: Update, context: CallbackContext):
    user = update.message.from_user.username if update.message.from_user else None

    # Check if the message is forwarded and the user is allowed
    if user in ALLOWED_USERS:
        if update.message.forward_origin and update.message.forward_origin.chat:
            # This is a forwarded message from a channel
            forwarded_chat = update.message.forward_origin.chat
            chat_id = forwarded_chat.id
            chat_title = forwarded_chat.title if forwarded_chat.title else "Unknown Channel"
            
            # Reply with the forwarded channel ID
            await update.message.reply_text(f"The forwarded message is from {chat_title}. The ID is: {chat_id}")
        else:
            await update.message.reply_text("This message was not forwarded from a channel.")
    else:
        await update.message.reply_text("You are not authorized to extract this information.")

# Function to forward messages from allowed users or from channels to other groups/channels
async def forward_message(update: Update, context: CallbackContext):
   
    # Check if the message is from a channel using 'channel_post'
    if update.channel_post:
        chat_type = update.channel_post.chat.type  # Get the type of chat (channel in this case)
        chat_id = update.channel_post.chat.id  # Get the ID of the channel where the message was sent
        text = update.channel_post.text if update.channel_post.text else ""

        if chat_type == "channel":
            chat_title = update.channel_post.chat.title if update.channel_post.chat.title else "Channel"
            for target in TARGET_GROUPS:
                if chat_id != target["chat_id"]:  # Prevent forwarding to the same channel
                    # Forward the message from the channel to all other target groups/channels
                    await context.bot.send_message(
                        chat_id=target["chat_id"],
                        text=f"Message from {chat_title}: {text}",
                        message_thread_id=target["topic_id"]  # Send to the correct topic if it exists
                    )
    
    # Handle messages from groups and allowed users
    elif update.message:
        chat_type = update.message.chat.type  # Get the type of chat (group or channel)
        chat_id = update.message.chat.id  # Get the ID of the group or channel where the message was sent
        text = update.message.text if update.message.text else ""
        
        if chat_type in ["group", "supergroup"]:
            user = update.message.from_user.username if update.message.from_user else None

            # Forward the message only if it's from an allowed user
            if user in ALLOWED_USERS:
                for target in TARGET_GROUPS:
                    if chat_id != target["chat_id"]:  # Prevent forwarding to the same group
                        # Forward the message to all target groups/channels
                        await context.bot.send_message(
                            chat_id=target["chat_id"], 
                            text=f"From @{user}: {text}",
                            message_thread_id=target["topic_id"]  # Send to the correct topic if it exists
                        )

def main():
    # Initialize the application (v20+ of python-telegram-bot)
    application = Application.builder().token(TOKEN).build()

    # Command to start the bot
    application.add_handler(CommandHandler("start", start))

    # Command to get the group/channel ID
    application.add_handler(CommandHandler("get_group_id", get_group_id))

    # Handler for forwarded messages to detect private channel ID
    application.add_handler(MessageHandler(filters.FORWARDED, handle_forwarded_message))

    # Handler to forward messages from channels and groups to the target groups
    application.add_handler(MessageHandler(filters.ALL, forward_message))  # Listen to all message types

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()