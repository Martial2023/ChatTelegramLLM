from telegram import Update
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
from utils import *
from threading import Thread
from fastapi import FastAPI, Request
import httpx
import uvicorn


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

api = FastAPI()

@api.get("/", include_in_schema=False)
@api.head("/", include_in_schema=False)
async def root():
    return {"status": "Bot en ligne"}

##### Fonctions pour Whatsapp #####
@api.get("/webhook")
async def verify_webhook(request: Request):
    args = dict(request.query_params)
    if args.get("hub.mode") == "subscribe" and args.get("hub.verify_token") == VERIFY_TOKEN:
        return int(args.get("hub.challenge"))
    return {"error": "Invalid verification"}

@api.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    print("Données reçues :", data)

    # Extraction du message texte
    try:
        entry = data["entry"][0]
        message = entry["changes"][0]["value"]["messages"][0]
        text = message["text"]["body"]
        sender_id = message["from"]
    except Exception as e:
        print("Message invalide :", e)
        return {"status": "ignored"}

    if sender_id not in histories:
        histories[sender_id] = [SYSTEM_PROMPT]
    
    histories[sender_id].append({"role": "user", "content": message})
    response = ask_llama(histories[sender_id])
    histories[sender_id].append({"role": "assistant", "content": response})

    # Gérer historique (limite max 20 échanges)
    if len(histories[sender_id]) > 41:
        histories[sender_id] = [histories[sender_id][0]] + histories[sender_id][-40:]

    save_histories(histories)
    
    # Répondre à l'utilisateur via WhatsApp API
    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages",
            headers={
                "Authorization": f"Bearer {WHATSAPP_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "messaging_product": "whatsapp",
                "to": sender_id,
                "type": "text",
                "text": {"body": response}
            }
        )
    return {"status": "done"}


#### Fonctions pour Telegram 

def run_api():
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(api, host="0.0.0.0", port=port)

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
    

# Init Telegram bot
def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot Telegram lancé.")
    app.run_polling()
    
# Run bot and FastAPI in parallel
if __name__ == "__main__":
    Thread(target=run_api).start()
    run_bot()