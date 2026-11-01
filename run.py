import os
import subprocess
from dotenv import load_dotenv
from src.rag_engine import KnowledgeBase
from src.agent import ZentroMartAgent

load_dotenv()

def main():
    print("1. Starting ZentroMart AI Brain...")
    kb = KnowledgeBase()
    kb.ingest_documents()
    agent = ZentroMartAgent(rag_engine=kb)
    
    print("\n2. AI is ready! Press 'Fn' twice to dictate, or type your question.")
    print("(Type 'quit' when you want to stop)\n")
    
    while True:
        user_input = input("Customer You: ")
        
        if user_input.lower() == 'quit':
            print("Shutting down. Goodbye!")
            break
            
        if user_input.strip() == "":
            continue
            
        print("Agent Thinking...")
        reply = agent.process_turn(user_input)
        print(f"ZentroMart AI: {reply}\n")
        
        # This command makes your Mac speak the response out loud
        subprocess.run(["say", reply])

if __name__ == "__main__":
    main()