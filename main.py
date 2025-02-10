import os
import uvicorn
from fastapi import FastAPI
from telegram_bot import app  # Importa o bot do Telegram

app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "Chatbot rodando no Render!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
