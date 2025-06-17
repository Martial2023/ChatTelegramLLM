from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")  # Utilisé pour vérifier le webhook
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

@app.get("/webhook")
async def verify_webhook(request: Request):
    args = dict(request.query_params)
    if args.get("hub.mode") == "subscribe" and args.get("hub.verify_token") == VERIFY_TOKEN:
        return int(args.get("hub.challenge"))
    return {"error": "Invalid verification"}

@app.post("/webhook")
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

    # Appel LLM (Groq) ici
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": text}],
        temperature=0.7,
        max_completion_tokens=512,
    )
    reply = response.choices[0].message.content

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
                "text": {"body": reply}
            }
        )
    return {"status": "done"}
