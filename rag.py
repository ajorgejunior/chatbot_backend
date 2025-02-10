import os
import time
import threading
import fitz  # PyMuPDF para leitura de PDFs
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Modelo de embeddings para o banco vetorial
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = None  # Banco vetorial inicializado como None

# Variável global para armazenar os arquivos já indexados
arquivos_indexados = set()

def dividir_texto(texto):
    """Divide o texto em partes menores para melhor indexação"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # Tamanho dos trechos
        chunk_overlap=50  # Sobreposição para manter contexto
    )
    return text_splitter.split_text(texto)

def extrair_texto_pdf(pdf_path):
    """Extrai texto de um PDF usando PyMuPDF."""
    texto = ""
    doc = fitz.open(pdf_path)
    for pagina in doc:
        texto += pagina.get_text("text") + "\n"
    return texto

def extrair_texto_planilha(excel_path):
    """Extrai dados de uma planilha."""
    df = pd.read_excel(excel_path)  # Lê a planilha como DataFrame
    texto = ""
    for _, row in df.iterrows():
        texto += " ".join(map(str, row.values)) + "\n"  # Concatena todas as colunas de cada linha
    return texto

def processar_arquivos():
    """Lê PDFs e planilhas da pasta 'documentos_pdfs', divide os textos e os adiciona ao banco vetorial"""
    global arquivos_indexados

    documentos = []
    novos_arquivos = set(os.listdir("documentos_pdfs")) - arquivos_indexados

    if not novos_arquivos:
        return []  # Nenhum novo arquivo foi encontrado

    print(f"📂 Novos arquivos detectados: {novos_arquivos}")

    for arquivo in novos_arquivos:
        caminho = os.path.join("documentos_pdfs", arquivo)
        if arquivo.endswith(".pdf"):
            texto = extrair_texto_pdf(caminho)
        elif arquivo.endswith(".xlsx") or arquivo.endswith(".xls"):
            texto = extrair_texto_planilha(caminho)
        else:
            continue  # Ignora arquivos não suportados

        # Divide o texto em partes menores e adiciona à lista de documentos
        documentos.extend(dividir_texto(texto))
    
    # Atualiza a lista de arquivos já indexados
    arquivos_indexados.update(novos_arquivos)

    return documentos

def inicializar_banco_vetorial():
    """Cria o banco vetorial FAISS a partir dos arquivos da pasta 'documentos_pdfs'."""
    global db
    textos = processar_arquivos()
    if textos:  # Só cria ou atualiza o FAISS se houver novos textos
        if db is None:
            db = FAISS.from_texts(textos, embedding_model)
        else:
            db.add_texts(textos)
        print("✅ Banco vetorial atualizado!")

# ✅ Agendador para verificar novos arquivos a cada 5 minutos
def monitorar_pasta():
    """Verifica a pasta a cada 5 minutos e atualiza os dados."""
    while True:
        inicializar_banco_vetorial()
        time.sleep(300)  # Espera 5 minutos antes de rodar de novo

# 🚀 Executa a função de monitoramento em segundo plano
threading.Thread(target=monitorar_pasta, daemon=True).start()

def buscar_resposta_rag(pergunta):
    """Busca informações relevantes nos documentos antes de responder."""
    if db is None:
        return "O banco vetorial ainda não foi carregado."

    # Ajustar o número de respostas mais relevantes (k=5)
    resultados = db.similarity_search(pergunta, k=5)

    # Se não encontrar muitos resultados, informar o usuário
    if not resultados:
        return "Nenhuma informação relevante foi encontrada nos documentos."

    # Filtrar trechos muito curtos ou irrelevantes
    contexto_filtrado = [r.page_content for r in resultados if len(r.page_content) > 20]
    
    if not contexto_filtrado:
        return "Os documentos não contêm informações suficientes sobre esse tema."

    contexto = "\n".join(contexto_filtrado)
    return contexto



