import os
import fitz  # PyMuPDF para leitura de PDFs
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configuração do modelo de embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = None  # Inicializa o banco vetorial

# Controle de arquivos já indexados
arquivos_indexados = set()

def dividir_texto(texto):
    """Divide o texto em partes menores para melhor indexação."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # Define o tamanho do trecho a ser indexado
        chunk_overlap=50  # Sobreposição para manter contexto
    )
    return text_splitter.split_text(texto)

def extrair_texto_pdf(pdf_path):
    """Extrai texto de um arquivo PDF usando PyMuPDF."""
    texto = ""
    doc = fitz.open(pdf_path)
    for pagina in doc:
        texto += pagina.get_text("text") + "\n"
    return texto

def extrair_texto_planilha(excel_path):
    """Extrai dados de uma planilha Excel e os transforma em texto."""
    df = pd.read_excel(excel_path)  # Lê a planilha
    texto = ""
    for _, row in df.iterrows():
        texto += " ".join(map(str, row.values)) + "\n"  # Concatena todas as colunas de cada linha
    return texto

def processar_arquivos():
    """Lê PDFs e planilhas da pasta 'documentos_pdfs', divide os textos e os adiciona ao banco vetorial."""
    global arquivos_indexados
    documentos = []
    novos_arquivos = set(os.listdir("documentos_pdfs")) - arquivos_indexados

    if not novos_arquivos:
        return []  # Nenhum novo arquivo encontrado

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
    """Cria ou atualiza o banco vetorial FAISS a partir dos arquivos processados."""
    global db
    textos = processar_arquivos()
    if textos:  # Só cria ou atualiza o FAISS se houver novos textos
        if db is None:
            db = FAISS.from_texts(textos, embedding_model)
        else:
            db.add_texts(textos)
        print("✅ Banco vetorial atualizado!")

def buscar_resposta_rag(pergunta):
    """Busca informações relevantes nos documentos antes de enviar para a IA."""
    if db is None:
        return "O banco vetorial ainda não foi carregado."

    resultados = db.similarity_search(pergunta, k=5)  # Pega os 5 trechos mais relevantes

    if not resultados:
        return "Nenhuma informação relevante foi encontrada nos documentos."

    contexto_filtrado = [r.page_content for r in resultados if len(r.page_content) > 20]
    
    if not contexto_filtrado:
        return "Os documentos não contêm informações suficientes sobre esse tema."

    contexto = "\n".join(contexto_filtrado)
    return contexto
