
# 💎 AURA — AI-Powered Virtual Jewelry Try-On (Smart Mirror)

**AURA** is a high-end, editorial-style virtual try-on application that transforms any device into a "Smart Mirror." By combining **Computer Vision** for real-time AR placement and **Generative AI** for personalized styling, AURA offers a seamless luxury shopping experience.

---

## 🌟 Key Features

* **✨ Virtual AR Try-On:** High-precision anchoring of earrings and necklaces using **MediaPipe** face landmark detection (anchors: chin, cheekbones, and jawline).
* **🤖 Hybrid AI Stylist:** A local RAG (Retrieval-Augmented Generation) system using **Gemma 3** and **Hugging Face** to provide expert fashion advice based on current inventory.
* **📂 Dynamic Inventory:** Managed via **MongoDB**, allowing for real-time updates to products, prices, and availability.
* **🎯 Drag-to-Adjust Engine:** An interactive canvas that allows users to manually fine-tune the position of jewellery for the perfect fit.
* **📸 Dual Mode Input:** Support for both high-quality image uploads and live webcam capture.

---

## 🛠️ Technical Architecture

AURA is built on a modern full-stack architecture designed for speed and scalability:

* **Backend:** FastAPI (Python)
* **AI Engine:** LangChain + ChromaDB (Vector Search)
* **Embeddings:** Hugging Face `all-MiniLM-L6-v2` (Local)
* **LLM:** Google Gemma 3-27B
* **CV:** MediaPipe & OpenCV
* **Database:** MongoDB
* **Frontend:** Vanilla JS, CSS3 (Luxury Editorial Theme), HTML5

---

## 📂 Directory Structure

```text
.
├── backend/
│   ├── routes/              # API Endpoints (Chat, Try-On, Products)
│   ├── static/jewellery/    # Product Image Assets
│   ├── utils/               # Database Seeding & RAG Sync scripts
│   ├── main.py              # FastAPI Entry Point
│   └── .env                 # Environment Variables
├── frontend/
│   ├── css/                 # Luxury UI Styles
│   ├── js/app.js            # Frontend Logic & AR Orchestration
│   └── index.html           # Main UI
├── requirements.txt         # Project Dependencies
└── README.md
```

---

## 🚀 Getting Started

### 1. Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Initialize Data
```bash
# Seed MongoDB with the jewelry collection
python backend/utils/seed_db.py

# Sync the AI Stylist's vector memory
python backend/utils/sync_rag.py
```

### 3. Launch Server
```bash
# Run the backend
uvicorn main:app --reload
```
*Access the frontend by opening `frontend/index.html` in your browser.*

---

## 👨‍💻 Developer
Developed with ❤️ by **Ayush Rajak**.

---

