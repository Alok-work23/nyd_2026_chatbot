import os
import json
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pytesseract
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import pickle

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def read_dataset_file(path):
    """Read file and extract text depending on file type"""
    ext = os.path.splitext(path)[1].lower()
    text = ""

    try:
        if ext in [".txt", ".md", ".rtf"]:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

        elif ext == ".json":
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                text = json.dumps(data, indent=2)

        elif ext == ".csv":
            df = pd.read_csv(path)
            text = df.to_string()

        elif ext == ".xlsx":
            df = pd.read_excel(path)
            text = df.to_string()

        elif ext == ".pdf":
            reader = PdfReader(path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        elif ext == ".docx":
            doc = Document(path)
            for para in doc.paragraphs:
                text += para.text + "\n"

        elif ext in [".jpg", ".jpeg", ".png"]:
            img = Image.open(path)
            text = pytesseract.image_to_string(img)

        else:
            print(f"⚠️ Unsupported format: {ext}")
            return ""

    except Exception as e:
        print(f"❌ Error reading {path}: {e}")
        return ""

    return text.strip()

def load_datasets(dataset_folder="datasets"):
    """Load all files from datasets folder"""
    documents = []
    for filename in os.listdir(dataset_folder):
        path = os.path.join(dataset_folder, filename)
        if os.path.isfile(path):
            doc_text = read_dataset_file(path)
            if doc_text:
                documents.append(doc_text)
                print(f"✅ Loaded {filename} ({len(doc_text)} chars)")
            else:
                print(f"⚠️ Skipped {filename}")
    return documents

def create_vector_store(documents, save_path="vectorstore.pkl"):
    """Convert documents into embeddings + save FAISS index"""
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = []
    for doc in documents:
        chunks.extend(splitter.split_text(doc))

    # Create embeddings
    embeddings = embedding_model.encode(chunks)

    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save index + chunks
    with open(save_path, "wb") as f:
        pickle.dump((index, chunks), f)

    print(f"✅ Vector store saved to {save_path} with {len(chunks)} chunks")

if __name__ == "__main__":
    docs = load_datasets()
    if docs:
        create_vector_store(docs)
    else:
        print("⚠️ No valid datasets found in /datasets")
