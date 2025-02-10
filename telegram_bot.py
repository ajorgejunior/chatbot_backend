import os
import requests
from fastapi import FastAPI, Request
from rag import buscar_resposta_rag
from openai_api import perguntar_chatgpt

# Configuração do bot do Telegram
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# Inicializa FastAPI
app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    """Recebe mensagens do Telegram e responde via API"""
    try:
        data = await request.json()

        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            pergunta = data["message"]["text"]

            # Busca a resposta usando RAG + OpenAI
            contexto = buscar_resposta_rag(pergunta)
            resposta = perguntar_chatgpt(pergunta, contexto)

            # Envia a resposta de volta para o Telegram
            requests.post(f"{BASE_URL}/sendMessage", json={"chat_id": chat_id, "text": resposta})

        return {"status": "ok"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
def home():
    """Página inicial para verificar se o servidor está rodando"""
    return {"mensagem": "Bot do Telegram rodando via Webhook!"}
