import os
import telebot
from openai_api import perguntar_chatgpt
from rag import buscar_resposta_rag

# 🔑 Pegue seu Token do Telegram do BotFather e defina como variável de ambiente
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def enviar_boas_vindas(message):
    bot.reply_to(message, "🤖 Olá! Eu sou seu Assistente. Pergunte-me algo!")

@bot.message_handler(func=lambda msg: True)
def responder_pergunta(message):
    pergunta = message.text.strip()

    # 1️⃣ Primeiro, tenta buscar nos documentos (RAG)
    contexto = buscar_resposta_rag(pergunta)

    if not contexto:
        contexto = "Nenhuma informação relevante encontrada nos documentos."

    # 2️⃣ Se não encontrar, usa GPT-3.5 Turbo
    resposta = perguntar_chatgpt(pergunta, contexto)

    bot.reply_to(message, resposta)

# Inicia o bot
bot.polling()
