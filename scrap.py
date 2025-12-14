import re
from telethon import TelegramClient
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

API_ID = 35062884
API_HASH = "8400559866:AAGU48t-KDPJyu0kmWxjVi-fryc2LTtYZ48"
BOT_TOKEN = "BOT_TOKEN"

pattern = re.compile(r"\d{12,16}\|\d{2}\|\d{2,4}\|\d{3,4}")

client = TelegramClient("session", API_ID, API_HASH)

async def scrap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /scrap @channel")
        return

    channel = context.args[0]
    await update.message.reply_text("🔍 Scraping started...")

    await client.start()

    entity = await client.get_entity(channel)
    async for msg in client.iter_messages(entity, limit=200):
        if msg.text:
            matches = pattern.findall(msg.text)
            for m in matches:
                await update.message.reply_text(m)

    await update.message.reply_text("✅ Scraping finished")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("scrap", scrap))

app.run_polling()