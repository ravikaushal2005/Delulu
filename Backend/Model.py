import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # automatically loads .env

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found!")

client = Groq(api_key=api_key)

chat_history = [
    {"role": "system", "content": "You are Delulu."}
]

def ask_groq(question):
    chat_history.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=chat_history
    )

    reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})

    return reply