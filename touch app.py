import ollama

print("🤖 MoltBot Started! Type 'exit' to stop.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = ollama.chat(
        model='llama3',
        messages=[{'role': 'user', 'content': user_input}]
    )

    print("Bot:", response['message']['content'])