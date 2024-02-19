import requests
from dotenv import load_dotenv
import os

def query_llm(UserInput):
    load_dotenv()
    api_url = os.environ['EMBEDDING_URL']
    api_key = os.environ['HF_TOKEN']

    #print("api_url :" + api_url)
    #print("api_key :" + api_key)


    req_header = {
        "Authorization": f"Bearer {api_key}"
    }


    req_body = {
        "inputs": UserInput,
        "parameters": {
            "max_new_tokens":500,
            "temperature": 1
        }
    }

    response = requests.post(api_url, json=req_body, headers=req_header)
    return response.json()

