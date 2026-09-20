import os
from ollama import Client

temperature = 1.0

SYSTEM_PROMPT = """
You are a supportive conversational assistant.

Respond in a warm, empathetic, and conversational way.
Focus on listening and understanding.
Ask one thoughtful follow-up question at a time.
Keep responses relatively brief.
Avoid long lists of advice unless the user asks for suggestions.
Do not provide diagnoses or medical advice.
Do not claim to be a therapist.
"""

client = Client(
    host=os.getenv("OLLAMA_HOST", "http://localhost:11434")
)


def generate_reply(user_message, history=None):

    if history is None:
        history = []

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(history)

    messages.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat(
        model="llama3.2",
        messages=messages,
        options={
            "temperature": temperature
        }
    )

    return response["message"]["content"]