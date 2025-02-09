import fitz
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = None  # Inicializa o banco vetorial

def inicializar_banco_vetorial():
    global db
    textos = processar_pdfs()  # Extrai os textos dos PDFs
    if textos:  # Só cria o FAISS se houver texto
        db = FAISS.from_texts(textos, embedding_model)
    else:
        print("Nenhum texto encontrado nos PDFs. O banco vetorial não será criado.")

inicializar_banco_vetorial()


def extrair_texto_pdf(pdf_path):
    """Extrai texto de um PDF usando PyMuPDF."""
    texto = ""
    doc = fitz.open(pdf_path)
    for pagina in doc:
        texto += pagina.get_text("text") + "\n"
    return texto

def processar_pdfs():
    """Lê PDFs do diretório e adiciona ao banco vetorial."""
    documentos = []
    for arquivo in os.listdir("documentos_pdfs"):
        if arquivo.endswith(".pdf"):
            caminho = os.path.join("documentos_pdfs", arquivo)
            texto = extrair_texto_pdf(caminho)
            documentos.append(texto)
    db.add_texts(documentos)

def buscar_resposta_rag(pergunta):
    """Busca informações nos documentos antes de responder."""
    resultados = db.similarity_search(pergunta, k=3)
    contexto = "\n".join([r.page_content for r in resultados])
    return contexto
