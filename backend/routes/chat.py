from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from pathlib import Path
from dotenv import load_dotenv
# --- UPDATED IMPORTS ---
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma

# Force load .env from backend root
current_dir = Path(__file__).resolve().parent.parent
env_path = current_dir / ".env"
load_dotenv(dotenv_path=env_path)

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
async def chat_with_stylist(request: ChatRequest):
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file")

        # 1. Load the AI's Brain (Using LOCAL Hugging Face to match your sync_rag.py)
        # This fixes the 404 NOT_FOUND error!
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        vector_db = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings
        )

        # 2. Setup Gemma 3 as the Chatbot via API (Keep this for the "Personality")
        llm = ChatGoogleGenerativeAI(
            model="gemma-3-27b-it",
            temperature=0.7,
            google_api_key=api_key  # Explicitly pass the key here too
        )

        # 3. Retrieval: Find the top 2 pieces of jewelry
        docs = vector_db.similarity_search(request.message, k=2)
        context = "\n\n".join([doc.page_content for doc in docs])

        # 4. The Expert Prompt Template
        prompt = f"""
        You are the "Aura AI Stylist," a world-class jewelry and beauty expert.
        Recommend jewelry from the context below and provide expert styling tips.

        Focus on how the piece complements skin tones or face shapes mentioned.

        CONTEXT FROM STORE:
        {context}

        USER QUERY: {request.message}

        STYLING ADVICE:
        """

        response = llm.invoke(prompt)

        return {
            "reply": response.content,
            "recommended_products": [doc.metadata for doc in docs]
        }

    except Exception as e:
        # This will now show the actual error in Swagger if something else fails
        raise HTTPException(status_code=500, detail=str(e))