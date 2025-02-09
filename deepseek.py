import requests
import os

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

def perguntar_deepseek(pergunta, contexto=""):
    """Faz uma requisição para a API do DeepSeek e retorna a resposta."""
    url = "https://api.deepseek.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Você é um assistente para um professor universitário."},
            {"role": "user", "content": f"Pergunta: {pergunta}\nContexto: {contexto}"}
        ],
        "max_tokens": 500,  # Define um limite para evitar respostas longas demais
        "temperature": 0.7  # Ajuste de criatividade (0 = mais conservador, 1 = mais criativo)
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        # Verifica se a resposta contém 'choices' e se há conteúdo
        if "choices" not in response_data or not response_data["choices"]:
            return "Erro: A API do DeepSeek não retornou uma resposta válida."

        return response_data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        return f"Erro ao acessar a API do DeepSeek: {e}"