from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import pandas as pd
import os

# =====================
# === CONFIGURATION ===
# =====================
BOT_TOKEN = "8271690385:AAEm-B2RLmfhfauvZLkYTtyiXSxQJd4N0Ww"  # Replace with your BotFather token
FILE_NAME = "responses.csv"  # CSV file to store messages

# ===========================
# === INITIALIZE CSV FILE ===
# ===========================
if not os.path.exists(FILE_NAME):
    pd.DataFrame(columns=["username", "user_id", "message"]).to_csv(FILE_NAME, index=False)


# ===========================
# === BOT HANDLER FUNCTIONS ===
# ===========================

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I'm your Message Tracker Bot 🤖\n"
        "Send me a message and I'll save it.\n"
        "You can also use /broadcast <your message> to send messages to all users."
    )


# Save user messages
async def save_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    # Load CSV
    df = pd.read_csv(FILE_NAME)

    # Append new message
    new_row = {"username": user.username, "user_id": user.id, "message": text}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)

    await update.message.reply_text("✅ Got it! Your response has been saved.")


# /broadcast command
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    df = pd.read_csv(FILE_NAME)

    # Join command arguments into one message
    message_text = " ".join(context.args)

    if not message_text:
        await update.message.reply_text("⚠️ Usage: /broadcast <your message>")
        return

    sent_count = 0
    for user_id in df["user_id"].unique():
        try:
            await context.bot.send_message(chat_id=int(user_id), text=message_text)
            sent_count += 1
        except Exception as e:
            print(f"Could not send message to {user_id}: {e}")

    await update.message.reply_text(f"✅ Message sent to {sent_count} users!")


# ===========================
# === BOT INITIALIZATION ===
# ===========================
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_response))

print("🤖 Bot is running... Press Ctrl+C to stop")
app.run_polling()
