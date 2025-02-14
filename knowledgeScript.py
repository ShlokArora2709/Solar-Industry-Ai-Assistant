import os
import time
from my_utils import download_pdf
from googlesearch import search
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
PDF_DIR = "pdf_files"
os.makedirs(PDF_DIR, exist_ok=True)
VECTOR_DB_DIR = "vector_db"
os.makedirs(VECTOR_DB_DIR, exist_ok=True)


Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)
topics = [
    "Solar Panel Technology",
    "Installation Processes of solar panels",
    "Maintenance Requirements of solar panels",
    "Cost & ROI Analysis of solar panels",
    "Industry Regulations for solar panels",
    "market trends of solar panels",
]



pdf_files = []
for topic in topics:
    query = f'"{topic}" filetype:pdf'
    print(f"Searching PDFs for topic: {topic}")

    try:
        for url in search(query, num_results=8):
            pdf_filename = f"{PDF_DIR}/{topic.replace(' ', '_')}_{len(pdf_files)}.pdf"
            if download_pdf(url, pdf_filename):
                pdf_files.append(pdf_filename)
    except Exception as e:
        print(f"Error searching for {topic}: {e}")
    time.sleep(3)


documents = SimpleDirectoryReader(PDF_DIR,filename_as_id=True).load_data()
index = VectorStoreIndex.from_documents(documents)
index.set_index_id("vector_index")
index.storage_context.persist(persist_dir=VECTOR_DB_DIR)

print("\nVector store saved successfully!")
