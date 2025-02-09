from fastapi import FastAPI, HTTPException
from db import conectar_db
from rag import buscar_resposta_rag
from deepseek import perguntar_deepseek
import uvicorn
import os

app = FastAPI()

@app.get("/")
def home():
    """Endpoint para verificar se a API está online."""
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
    """Faz uma busca nos PDFs (RAG) e chama a IA para responder."""
    try:
        contexto = buscar_resposta_rag(pergunta)
        if not contexto or contexto.strip() == "":
            contexto = "Nenhuma informação relevante encontrada nos documentos."

        resposta = perguntar_deepseek(pergunta, contexto)
        if not resposta or resposta.strip() == "":
            resposta = "A IA não conseguiu gerar uma resposta com base nos dados disponíveis."

        return {"resposta": resposta}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar pergunta: {e}")

# Garantir que o Render detecte a porta corretamente
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Usa a porta definida pelo Render
    uvicorn.run(app, host="0.0.0.0", port=10000)
