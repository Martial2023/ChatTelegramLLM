from telegram import Update
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
from utils import *

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

histories = load_histories()
# 🚀 Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Salut, comment puis-je t'aider?")
    
# 🔁 Commande /reset
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    histories[user_id] = [SYSTEM_PROMPT]
    save_histories(histories)
    await update.message.reply_text("🔄 Mémoire effacée. On recommence à zéro.")
    
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_message = update.message.text
    #await update.message.reply_text("Je réfléchis... 🤔")
    if user_id not in histories:
        histories[user_id] = [SYSTEM_PROMPT]
    
    histories[user_id].append({"role": "user", "content": user_message})
    try:
        response = ask_llama(histories[user_id])
        histories[user_id].append({"role": "assistant", "content": response})

        # Gérer historique (limite max 20 échanges)
        if len(histories[user_id]) > 41:
            histories[user_id] = [histories[user_id][0]] + histories[user_id][-40:]

        save_histories(histories)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text("Une erreur s'est produite.")
    
    
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
print("✅ Bot en cours d'exécution...")
app.run_polling()