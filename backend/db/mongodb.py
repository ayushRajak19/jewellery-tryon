from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

# We will put your MongoDB URL in the .env file
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

# Create the client
client = AsyncIOMotorClient(MONGO_URL)

# Select the database (it will auto-create if it doesn't exist)
db = client.jewellery_store

# Select the collection (like a table in SQL)
jewellery_collection = db.get_collection("catalogue")
orders_collection = db.get_collection("orders")