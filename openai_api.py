import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def perguntar_chatgpt(pergunta, contexto):
    """Faz a pergunta à OpenAI usando o contexto do RAG."""
    prompt = f"Contexto relevante:\n{contexto}\n\nPergunta: {pergunta}\n\nResposta:"
    
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente acadêmico."},
                {"role": "user", "content": prompt}
            ]
        )
        return resposta.choices[0].message.content
    except Exception as e:
        return f"Erro ao acessar OpenAI: {str(e)}"
