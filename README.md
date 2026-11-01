# ZentroMart VoiceOps 🎙️🤖

An AI-powered customer support backend for e-commerce, built with Python, FastAPI, and Google Gemini. 

## 📖 Overview
ZentroMart VoiceOps is an intelligent, voice-ready backend designed to handle customer queries automatically. It utilizes a Retrieval-Augmented Generation (RAG) architecture to answer questions based on internal company policies, and features secure tool-calling to fetch real-time customer and order data.

## ✨ Features
- **RAG Knowledge Base:** Powered by ChromaDB to accurately retrieve context-specific company policy information.
- **Advanced AI:** Integrated with the Google Gemini API for natural language understanding and response generation.
- **Real-Time Data:** Uses tool-calling to securely fetch live order statuses and customer details.
- **Voice Capabilities:** Includes a local Mac text-to-speech fallback (`run.py`) for voice interactions.

## 🛠️ Tech Stack
- **Backend Framework:** Python, FastAPI, Uvicorn
- **AI / LLM:** Google Gemini API
- **Vector Database:** ChromaDB

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/lata-yadav20/zentromart-voiceops.git](https://github.com/lata-yadav20/zentromart-voiceops.git)
   cd zentromart-voiceops



   3. **Install the required packages:**
   ```bash
   pip install fastapi uvicorn chromadb google-generativeai

   python3 -m venv venv
source venv/bin/activate


GEMINI_API_KEY=your_api_key_here

uvicorn server:app --reload

python run.py

