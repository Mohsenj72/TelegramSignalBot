import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise RuntimeError("TOKEN environment variable not set")

def format_signal(line: str) -> str:
    parts = line.split()
    if len(parts) < 9:
        return "⚠️ Invalid line format"
    
    date = parts[0]
    pair = parts[1]
    session = parts[2]
    signal = parts[3]
    entry = parts[4]
    stoploss = parts[5]
    targets = parts[6:9]
    
    return f"""🗓 {date} ⏰ {session}

📊 #<b>{pair}</b> 📈 <b>{signal}</b>
🔹 Entry: {entry}

⚠️ Stop Loss: {stoploss}
🎯 Targets: {' / '.join(targets)}

     <b>Babak.FX.Gold</b>"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        lines = update.message.text.splitlines()
        for line in lines:
            await update.message.reply_text(format_signal(line), parse_mode="HTML")
    else:
        await update.message.reply_text("⚠️ Empty or unsupported message")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()
