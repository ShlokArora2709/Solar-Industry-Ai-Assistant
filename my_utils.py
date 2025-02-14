import os
from llama_index.core import Settings
import requests
import json
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
load_dotenv()
Settings.llm=None
HEADERS = {
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
    "Content-Type": "application/json",
}

def query_knowledge_base(query_text: str,index:VectorStoreIndex) -> str:
    query_engine = index.as_query_engine()
    response= query_engine.query(query_text)
    return str(response)


def query_openrouter(query_text: str, context: str) -> str:
    payload = {
        "model": "google/gemini-2.0-pro-exp-02-05:free",
        "messages": context + [{"role": "user", "content": query_text}],
        "max_tokens": 300,
    }

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers=HEADERS,
        data=json.dumps(payload)
    )

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"


def download_pdf(url:str, save_path:str) -> bool:   
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded: {save_path}")
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

