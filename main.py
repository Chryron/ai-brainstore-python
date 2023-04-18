from brain import BrainInstance
from chatbot import create_chat_completion, learn

def create_context(documents):

    context = f"""You are given the following documents: {documents} 
    You can only use the given documents - do not recall info from your own memory. If the given documents are sufficient for an accurate answer, then use them to give an accurate, detailed answer. 
    If the given documents do not provide information about the question, ONLY respond with the following string: "INSUFFICIENT_DATA"."""
    return context

def get_documents(query):
    nearText = {"concepts": [query]}
    result = (
        BrainInstance.client.query
        .get("Documents", ["document_text"])
        .with_near_text(nearText)
        .with_limit(1)
        .do()
    )
    docs = result["data"]["Get"]["Documents"]
    documents = ""
    for doc in docs:
        documents += doc["document_text"] + "\n"
    return documents

def main():
    print("Welcome to the Encyclopedia Bot!")
    while True:
        print("What would you like to know?")
        query = input()
        documents = get_documents(query)
        assistant_reply = create_chat_completion(
            context=create_context(documents),
            content=query
        )
        if "INSUFFICIENT_DATA" in assistant_reply:
            print("I'm sorry, I don't know that yet. Please wait...")
            try:
                learn(query)
            except Exception:
                print("I'm sorry, I couldn't learn that.")
                continue
            else:
                print("I've learned that now!")
                documents = get_documents(query)
                assistant_reply = create_chat_completion(
                    context=create_context(documents),
                    content=query
                )
                print(assistant_reply)
        else:
            print(assistant_reply)

if __name__ == "__main__":
    main()