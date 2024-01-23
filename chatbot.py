import requests
from dotenv import load_dotenv
import os

def query(UserInput):
    load_dotenv()
    api_url = os.environ['api_url']
    api_key = os.environ['api_key']


    req_header = {
        "Authorization": f"Bearer {api_key}"
    }

    # TODO: For additional configuration, go to https://huggingface.co/docs/api-inference/detailed_parameters#text-generation-task

    # Additional information that LLM does not know
    context = """
        Auryn is a gray, medium hair cat born in March, 2012. She is a maine coon mix who sports a medium sized mane and cute tufts on her ears and toes. She is clicker trained, and she can perform tricks such as sit, sit pretty, high five, high ten, and turn. She loves to eat, except when she is nervous. Her favorite food is chicken and pork. 
    """
    #context = """Imagine  you are Sales Agent"""

    req_body = {
        "inputs": UserInput,
        "context" : context
    }
    response = requests.post(api_url, json=req_body, headers=req_header)
    return response.json()

