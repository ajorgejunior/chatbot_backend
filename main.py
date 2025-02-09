import uvicorn
import os
from fastapi import FastAPI, HTTPException
from openai_api import perguntar_chatgpt
from rag import buscar_resposta_rag

app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "Chatbot RAG rodando com GPT-3.5 Turbo!"}

@app.get("/pergunta")
def perguntar(pergunta: str):
    """1️⃣ Primeiro, tenta buscar nos PDFs e Planilhas (RAG)  2️⃣ Se não encontrar, usa GPT-3.5 Turbo"""
    try:
        contexto = buscar_resposta_rag(pergunta)
        
        if not contexto:
            contexto = "Nenhuma informação relevante encontrada nos documentos."

        resposta = perguntar_chatgpt(pergunta, contexto)

        return {"resposta": resposta}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar pergunta: {e}")

# Garantir que o Render detecte a porta corretamente
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Usa a porta definida pelo Render
    uvicorn.run(app, host="0.0.0.0", port=10000)
