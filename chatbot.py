from ollama import chat
import os
# Change this to 1.0 for the high-temperature condition
temperature = 1.0

messages = [
    {
        "role": "system",
        "content": """
You are a supportive conversational assistant.

Respond in a warm, empathetic, and conversational way.
Focus on listening and understanding.
Ask one thoughtful follow-up question at a time.
Keep responses relatively brief.
Avoid long lists of advice unless the user asks for suggestions.
Do not provide diagnoses or medical advice.
Do not claim to be a therapist.
"""
    }
]

print("\nSupportive Chat")
print("Type 'end' when you want to finish the conversation.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "end":
        break

    # Add user's message to temporary conversation history
    messages.append({
        "role": "user",
        "content": user_input
    })

    # Generate response
    response = chat(
        model="llama3.2",
        messages=messages,
        options={
            "temperature": temperature
        }
    )

    assistant_message = response["message"]["content"]

    # Add Llama's response to conversation history
    messages.append({
        "role": "assistant",
        "content": assistant_message
    })

    print("\nChatbot:", assistant_message, "\n")


# Save a copy of the transcript for your professor
filename = f"example_conversation_temp_{temperature}.txt"

with open(filename, "w", encoding="utf-8") as file:
    file.write(f"TEMPERATURE: {temperature}\n")
    file.write("=" * 60 + "\n\n")

    for message in messages:
        # Skip the hidden system prompt
        if message["role"] == "system":
            continue

        if message["role"] == "user":
            file.write("USER:\n")
            file.write(message["content"] + "\n\n")

        elif message["role"] == "assistant":
            file.write("CHATBOT:\n")
            file.write(message["content"] + "\n\n")

print(f"\nConversation saved as: {filename}")