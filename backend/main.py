from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
from pymongo import MongoClient

# --- NEW: Import the tryon router ---
from routes.chat import router as chat_router
from routes.tryon import router as tryon_router # Ensure this file exists in routes/

load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "Aura Jewellery Try-On API"),
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Product Route
@app.get("/api/products")
async def get_products():
    try:
        client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
        db = client["aura_db"]
        products = list(db["products"].find({}, {"_id": 0}))
        return products
    except Exception as e:
        return {"error": str(e)}

# --- NEW: Include both routers ---
app.include_router(chat_router, prefix="/api")
app.include_router(tryon_router, prefix="/api") # This fixes the 'Not Found' error

@app.get("/")
def root():
    return {"message": "Aura API running with Hybrid GenAI Stylist"}