from fastapi import FastAPI, HTTPException
from db import conectar_db
from rag import buscar_resposta_rag
from openai_api import perguntar_chatgpt
import uvicorn
import os

app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "Chatbot RAG rodando no Render!"}

@app.get("/eventos")
def listar_eventos():
    """Busca eventos acadêmicos no banco de dados."""
    try:
        conexao = conectar_db()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM eventos;")
        eventos = cursor.fetchall()
        conexao.close()

        if not eventos:
            return {"mensagem": "Nenhum evento encontrado."}

        return {"eventos": eventos}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar banco de dados: {e}")

@app.get("/pergunta")
def perguntar(pergunta: str):
    """1️⃣ Primeiro, tenta buscar no PostgreSQL  2️⃣ Se não encontrar, consulta PDFs  3️⃣ Se nada for útil, chama GPT"""
    try:
        conexao = conectar_db()
        cursor = conexao.cursor()

        # 🔥 Tenta encontrar uma resposta diretamente no banco
        cursor.execute("SELECT resposta FROM respostas WHERE pergunta ILIKE %s LIMIT 1;", (f"%{pergunta}%",))
        resposta_bd = cursor.fetchone()
        conexao.close()

        if resposta_bd:
            return {"resposta": resposta_bd[0]}  # Retorna a resposta encontrada no banco

        # 🔥 Se não encontrou no banco, busca nos PDFs (RAG)
        contexto = buscar_resposta_rag(pergunta)
        if not contexto or contexto.strip() == "":
            contexto = "Nenhuma informação relevante encontrada nos documentos."

        # 🔥 Chama o GPT-3.5 Turbo com o contexto do RAG
        resposta = perguntar_chatgpt(pergunta, contexto)

        if not resposta or resposta.strip() == "":
            resposta = "A IA não conseguiu gerar uma resposta com base nos dados disponíveis."

        return {"resposta": resposta}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar pergunta: {e}")


# Garantir que o Render detecte a porta corretamente
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Usa a porta definida pelo Render
    uvicorn.run(app, host="0.0.0.0", port=10000)
