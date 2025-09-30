import os, requests
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

data = {"inputs": "Hello, how are you?"}
response = requests.post(API_URL, headers=headers, json=data)

print("Status code:", response.status_code)
print("Raw text:", response.text)
