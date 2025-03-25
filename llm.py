import ollama


def chat_with_ollama():
    print("Ollama Chatbot - Type 'exit' to end the conversation")
    model = "llama3.2"
    history = []
    history.append(
        {
            "role": "system",
            "content": "You will act as a NAO robot assistant to give encouragement to the user. Make your response concise and positive.",
        }
    )

    # Send initial context to the model
    response_stream = ollama.chat(model=model, messages=history, stream=True)
    print("Bot:", end=" ")
    reply = ""

    for chunk in response_stream:
        content = chunk["message"]["content"]
        print(content, end="", flush=True)
        reply += content
    print()

    history.append({"role": "assistant", "content": reply})

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        history.append({"role": "user", "content": user_input})

        response_stream = ollama.chat(
            model=model, messages=[{"role": "user", "content": user_input}], stream=True
        )
        print("Bot:", end=" ")
        reply = ""

        for chunk in response_stream:
            content = chunk["message"]["content"]
            print(content, end="", flush=True)
            reply += content
        print()

        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    chat_with_ollama()
