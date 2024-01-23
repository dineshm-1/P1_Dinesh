import requests
from dotenv import load_dotenv
import os

import chatbot as bot



# Question about the context that LLM wouldn't know otherwise
user_question = "What is Auryn's favorite food?"

#TODO
prompt = input(user_question)

print(bot.query(prompt))