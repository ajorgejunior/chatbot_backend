import requests
import os
from dotenv import load_dotenv

# Carregar a chave da API
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

def perguntar_deepseek(pergunta, contexto=""):
    """Envia a pergunta para a API do DeepSeek."""
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Você é um assistente acadêmico."},
            {"role": "user", "content": f"Contexto: {contexto}\nPergunta: {pergunta}"}
        ]
    }
    resposta = requests.post(url, headers=headers, json=data)
    return resposta.json()["choices"][0]["message"]["content"]
