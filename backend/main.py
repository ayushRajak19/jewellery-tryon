from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

from routes.detect import router as detect_router
from routes.tryon  import router as tryon_router
from routes.shop   import router as shop_router

load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "Jewellery Try-On API"),
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(detect_router, prefix="/api")
app.include_router(tryon_router,  prefix="/api")
app.include_router(shop_router,   prefix="/api")

@app.get("/")
def root():
    return {"message": "Jewellery Try-On API running"}