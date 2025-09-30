import os
import pickle
import faiss
import numpy as np
import requests
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Hugging Face API
HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index and chunks
with open("vectorstore.pkl", "rb") as f:
    index, chunks = pickle.load(f)

def query_hf(prompt):
    """Send query to Hugging Face API safely"""
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

    if response.status_code != 200:
        return f"❌ API Error {response.status_code}: {response.text}"

    result = response.json()

    # Handle both summary_text and generated_text cases
    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]
    elif isinstance(result, list) and "summary_text" in result[0]:
        return result[0]["summary_text"]
    else:
        return str(result)


def chatbot(user_input, top_k=3):
    """Main chatbot function"""
    # Convert user query into embedding
    query_vec = embedding_model.encode([user_input])

    # Search in FAISS index
    distances, indices = index.search(query_vec, top_k)
    retrieved_chunks = [chunks[i] for i in indices[0]]

    # Build final prompt
    context = "\n".join(retrieved_chunks)
    prompt = f"Answer the question based on the context:\n\nContext:\n{context}\n\nQuestion: {user_input}\nAnswer:"

    # Get answer from Hugging Face
    answer = query_hf(prompt)
    return answer

if __name__ == "__main__":
    print("🤖 Chatbot ready! Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        response = chatbot(user_input)
        print("Bot:", response)
