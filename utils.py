from groq import Groq
import os
from dotenv import load_dotenv
import json

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq()


HISTORY_FILE = "histories.json"
def load_histories():
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_histories(histories):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(histories, f, ensure_ascii=False, indent=2)
        
 
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Tu es un assistant personnel numérique nommé Aïa. "
        "Tu es bienveillant, intelligent, curieux et pédagogue. "
        "Tu parles toujours en français. "
        "Tu aides principalement Martial AVADRA dans ses projets techniques, professionnels et créatifs. "
        "Tu expliques clairement, tu es honnête si tu ne sais pas, tu évites les réponses vagues. "
        "Tu fais de l'humour léger parfois, mais restes toujours respectueux et utile."
    )
}
        
def ask_llama(messages):
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=messages,
        temperature=0.7,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,  # Pour l'intégration Telegram, mieux vaut éviter stream=True
    )
    return completion.choices[0].message.content