import os
from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv

current_dir = Path(__file__).resolve().parent.parent
env_path = current_dir / ".env"
load_dotenv(dotenv_path=env_path)

def seed_database():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(mongo_uri)
    db = client["aura_db"]
    collection = db["products"]

    collection.delete_many({}) # Clear old data

    sample_jewelry = [
        # --- EARRINGS ---
        {
            "id": "e1",
            "name": "Classic Gold Studs",
            "type": "earring",
            "price": 2500,
            "original_price": 3500,
            "rating": 4.5,
            "reviews": 85,
            "description": "Timeless 18k gold studs for everyday elegance.",
            "image": "earring1.png"
        },
        {
            "id": "e2",
            "name": "Silver Tear-Drop Earrings",
            "type": "earring",
            "price": 3200,
            "original_price": 4500,
            "rating": 4.7,
            "reviews": 56,
            "description": "Elegant sterling silver teardrops with diamond accents.",
            "image": "earring2.png"
        },
        {
            "id": "e3",
            "name": "Emerald Floral Studs",
            "type": "earring",
            "price": 5000,
            "original_price": 6500,
            "rating": 4.9,
            "reviews": 42,
            "description": "Exquisite emerald stones set in a floral gold pattern.",
            "image": "earring3.png"
        },
        # --- NECKLACES ---
        {
            "id": "n1",
            "name": "Royal Kundan Choker",
            "type": "necklace",
            "price": 12000,
            "original_price": 15000,
            "rating": 4.8,
            "reviews": 124,
            "description": "A heavy traditional choker featuring premium Kundan stones.",
            "image": "necklace1.png"
        },
        {
            "id": "n2",
            "name": "Rose Gold Heritage Haar",
            "type": "necklace",
            "price": 8500,
            "original_price": 11000,
            "rating": 4.6,
            "reviews": 78,
            "description": "A long, statement rose gold piece for formal evenings.",
            "image": "necklace2.png"
        },
        {
            "id": "n3",
            "name": "Minimalist Diamond Pendant",
            "type": "necklace",
            "price": 4500,
            "original_price": 5500,
            "rating": 4.4,
            "reviews": 210,
            "description": "A delicate silver chain with a single brilliant-cut diamond.",
            "image": "necklace3.png"
        }
    ]

    collection.insert_many(sample_jewelry)
    print(f"✅ Successfully inserted {len(sample_jewelry)} products into MongoDB!")

if __name__ == "__main__":
    seed_database()