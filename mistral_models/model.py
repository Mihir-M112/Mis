import requests
from dotenv import load_dotenv
import os

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")


def query(payload, model_name, token=HF_TOKEN):
    
    API_URL = f"https://api-inference.huggingface.co/models/mistralai/{model_name}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(API_URL, headers=headers, json=payload)
    response = response.json()    
    output = response
    return output