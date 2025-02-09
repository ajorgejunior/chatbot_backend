from fastapi import FastAPI
from db import conectar_db
from rag import buscar_resposta_rag
from deepseek import perguntar_deepseek

app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "Chatbot RAG rodando no Render!"}

@app.get("/eventos")
def listar_eventos():
    """Busca eventos acadêmicos no banco de dados."""
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM eventos;")
    eventos = cursor.fetchall()
    conexao.close()
    return {"eventos": eventos}

@app.get("/pergunta")
def perguntar(pergunta: str):
    """Faz uma busca nos PDFs (RAG) e chama a IA para responder."""
    contexto = buscar_resposta_rag(pergunta)
    resposta = perguntar_deepseek(pergunta, contexto)
    return {"resposta": resposta}
