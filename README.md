# nyd_2026_chatbot
NYD 2026 Hackathon – Phase 1

✅ Features

Plug-and-play chatbot → just drop datasets into /datasets/, no code edits needed.

Supports multiple formats:

.txt, .md, .rtf (plain text)

.json, .csv, .xlsx (structured data)

.pdf, .docx (documents)

.jpg, .jpeg, .png (OCR from images)

Uses sentence-transformers (all-MiniLM-L6-v2) for embeddings.

Stores embeddings in FAISS vector database for fast retrieval.

Uses Hugging Face Inference API (facebook/bart-large-cnn) for answer generation.

Lightweight → runs on local CPU, no heavy models required.

⚡ Installation
1. Clone Repo
git clone https://github.com/<your-username>/nyd2026_chatbot.git
cd nyd2026_chatbot

2. Create Virtual Environment
python -m venv venv
# Activate
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

3. Install Requirements
pip install -r requirements.txt

4. Setup Hugging Face Token

Create a token at Hugging Face

Check ✅ “Make calls to Inference Providers”.

Create a .env file in project root:

HUGGINGFACE_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx

🚀 Usage
1. Add Datasets

Place your datasets inside the /datasets/ folder.
Examples provided:

gita_sample.txt (text)

ramayana.json (JSON)

quotes.csv (CSV)

sample.pdf (PDF)

note.docx (Word)

scan.jpg (Image with OCR text)

2. Run Loader
python loader.py


This builds the vector store (vectorstore.pkl) from all dataset files.

3. Run Chatbot
python chatbot.py


Example interaction:

🤖 Chatbot ready! Type 'quit' to exit.

You: What does Krishna say about duty?
Bot: You have a right to perform your duty, but not to the fruits of action...

You: Why did Rama go to the forest?
Bot: Rama accepted exile to honor his father’s promise, with Sita and Lakshmana accompanying him.

🔧 Project Structure
nyd2026_chatbot/
│── datasets/           # Drop any dataset files here
│   ├── gita_sample.txt
│   ├── ramayana.json
│   ├── quotes.csv
│   ├── sample.pdf
│   ├── note.docx
│   └── scan.jpg
│
│── loader.py           # Loads datasets, creates vector store
│── chatbot.py          # Chatbot core (retrieval + API call)
│── requirements.txt    # Python dependencies
│── .env                # Hugging Face API token
│── README.md           # Documentation

📊 Code Pipeline

Dataset Loader (loader.py)

Detect file format → extract text (txt, json, csv, pdf, docx, jpg OCR).

Split into chunks (500 tokens).

Convert chunks → embeddings (all-MiniLM-L6-v2).

Save embeddings in FAISS vector store.

Chatbot Core (chatbot.py)

Load FAISS index + chunks.

Convert user query → embedding.

Retrieve top-k most relevant chunks.

Build final prompt = context + question.

Send to Hugging Face API (bart-large-cnn).

Return answer.

🤖 Models Used

sentence-transformers/all-MiniLM-L6-v2 → embeddings

facebook/bart-large-cnn → answer generation

⚡ Challenges

Some Hugging Face models (e.g., flan-t5-small) returned 404 / errors.
→ Fixed by switching to bart-large-cnn.

OCR from images produced noisy text.
→ Basic cleaning added, but can be improved.

Handling multiple file types required many libraries (PyPDF2, python-docx, pytesseract).

🚀 Future Improvements

Add support for more formats (HTML, PPTX, EPUB, audio with Whisper).

Use stronger LLMs like Mistral-7B-Instruct for better Q&A.

Deploy as a Flask/React web app (Phase 3).

Use cloud vector DB (Pinecone/Weaviate) for scalability.

Add evaluation metrics for answer quality.
