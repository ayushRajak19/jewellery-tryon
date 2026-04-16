import os
from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

current_dir = Path(__file__).resolve().parent.parent
env_path = current_dir / ".env"
load_dotenv(dotenv_path=env_path)


def sync_mongodb_to_vector_db():
    print("Starting sync process...")

    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(mongo_uri)
    db = client["aura_db"]
    products_col = db["products"]

    products = list(products_col.find({}))
    if not products:
        print("❌ No products found in MongoDB. Please add some first!")
        return

    documents = []
    for p in products:
        content = f"Product: {p.get('name', 'Unknown')}. Type: {p.get('type', 'Jewelry')}. " \
                  f"Price: ₹{p.get('price', 0)}. Description: {p.get('description', '')}. " \
                  f"Tags: {', '.join(p.get('tags', []))}"

        metadata = {
            "product_id": str(p['_id']),
            "image": p.get('image', ''),
            "name": p.get('name', ''),
            "price": float(p.get('price', 0))
        }
        documents.append(Document(page_content=content, metadata=metadata))

    print("Loading Local Hugging Face memory...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vector_db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

    print(f"✅ Success! Synced {len(documents)} products locally using Hugging Face.")


if __name__ == "__main__":
    sync_mongodb_to_vector_db()