import fitz  # PyMuPDF para PDF
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def extrair_texto_pdf(pdf_path):
    """Extrai texto de um PDF usando PyMuPDF."""
    texto = ""
    doc = fitz.open(pdf_path)
    for pagina in doc:
        texto += pagina.get_text("text") + "\n"
    return texto

def extrair_texto_planilha(planilha_path):
    """Lê planilhas (CSV ou Excel) e extrai os textos."""
    textos = []
    try:
        if planilha_path.endswith(".csv"):
            df = pd.read_csv(planilha_path)
        elif planilha_path.endswith(".xlsx") or planilha_path.endswith(".xls"):
            df = pd.read_excel(planilha_path)
        else:
            return []

        # Concatena todas as colunas em uma string para cada linha
        for _, row in df.iterrows():
            linha_texto = " | ".join(str(valor) for valor in row if pd.notna(valor))
            textos.append(linha_texto)

    except Exception as e:
        print(f"Erro ao processar planilha {planilha_path}: {e}")

    return textos

def processar_documentos():
    """Lê PDFs e Planilhas do diretório e gera os embeddings dinamicamente."""
    documentos = []

    for arquivo in os.listdir("documentos_pdfs"):
        caminho = os.path.join("documentos_pdfs", arquivo)
        
        if arquivo.endswith(".pdf"):
            texto = extrair_texto_pdf(caminho)
            documentos.append(texto)

        elif arquivo.endswith(".csv") or arquivo.endswith(".xlsx") or arquivo.endswith(".xls"):
            textos_planilha = extrair_texto_planilha(caminho)
            documentos.extend(textos_planilha)

    return documentos

def buscar_resposta_rag(pergunta):
    """Recarrega os documentos e busca informações antes de responder."""
    textos = processar_documentos()  # 🔥 Recarrega os documentos toda vez que for chamado

    if not textos:
        return "Nenhuma informação relevante encontrada nos documentos."

    db = FAISS.from_texts(textos, embedding_model)  # 🔥 Cria um novo FAISS dinâmico
    resultados = db.similarity_search(pergunta, k=3)
    
    contexto = "\n".join([r.page_content for r in resultados])
    return contexto
