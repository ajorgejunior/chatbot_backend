import os
import requests
import logging
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
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

async def start(update: Update, context):
    """Comando /start para iniciar o bot"""
    await update.message.reply_text("Olá! Eu sou seu assistente acadêmico. Pergunte algo!")

async def responder(update: Update, context):
    """Recebe perguntas dos usuários e processa via RAG + GPT"""
    pergunta = update.message.text
    contexto = buscar_resposta_rag(pergunta)  # RAG busca informações nos documentos
    resposta = perguntar_chatgpt(pergunta, contexto)  # OpenAI gera resposta

    await update.message.reply_text(resposta)

def iniciar_bot():
    """Inicia o bot do Telegram e configura handlers"""
    app_telegram = ApplicationBuilder().token(TOKEN).build()

    # Comandos
    app_telegram.add_handler(CommandHandler("start", start))
    
    # Responder a qualquer mensagem recebida
    app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print("🤖 Bot do Telegram iniciado!")
    app_telegram.run_polling()

if __name__ == "__main__":
    iniciar_bot()

