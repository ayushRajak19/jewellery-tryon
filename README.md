
````markdown
# 💎 AI-Powered Virtual Jewelry Try-On (Smart Mirror)

## 📌 Overview
This project is a full-stack, real-time virtual jewelry try-on web application. Inspired by services like Lenskart, it acts as a "Smart Mirror" that allows users to digitally wear jewelry (such as earrings and necklaces) using their webcam. 

Beyond standard augmented reality overlay, this application integrates Generative AI to act as a virtual stylist, analyzing user context to recommend the perfect accessories.

## ✨ Features
* **Real-Time Anatomical Mapping:** Uses precise facial and body landmark detection to find ears, necklines, and collarbones.
* **Dynamic Compositing:** Automatically scales, rotates, and blends jewelry images onto the user's video feed adapting to head movements.
* **Automated Asset Processing:** Seamlessly removes backgrounds from raw jewelry product images using AI-based background removal.
* **Generative AI Stylist:** Features an integrated chatbot that recommends specific jewelry pieces based on user occasion, outfit, or preferences.

## 🛠️ Tech Stack
* **Computer Vision:** MediaPipe (Face Mesh/Pose), OpenCV
* **AI & LLMs:** LangChain, Groq API (for low-latency stylist inference)
* **Image Processing:** `rembg` (Background removal)
* **Backend:** FastAPI, Uvicorn, Python
* **Frontend:** React.js / HTML5 (Webcam integration)
* **Deployment Setup:** Docker, AWS EC2 (Planned)

## 🧠 Architecture & Workflow
1. **Capture:** The frontend captures the user's video feed and transmits frames to the backend.
2. **Detect:** MediaPipe extracts 468 3D facial landmarks to pinpoint exact attachment coordinates (e.g., earlobes).
3. **Process:** OpenCV applies a homography matrix to resize and rotate the jewelry PNG, performing alpha blending to seamlessly overlay it onto the user.
4. **Style (Gen AI):** The LangChain agent processes natural language inputs to query the jewelry database and dynamically trigger the display of recommended items.

## 🚀 Local Setup & Installation

### Prerequisites
* Python 3.9+
* Webcam access

### Installation Steps
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ayushRajak19/jewellery-tryon.git](https://github.com/ayushRajak19/jewellery-tryon.git)
   cd jewellery-tryon
````

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the FastAPI server:**

    ```bash
    uvicorn main:app --reload
    ```

## 🔮 Future Scope

  * Implement realistic shadow generation using Diffusion models.
  * Add multi-item try-on (e.g., wearing earrings and a necklace simultaneously).
  * E-commerce integration for direct checkout.

-----

## 👤 Author

**Ayush Rajak** \* GitHub: [@ayushRajak19](https://www.google.com/search?q=https://github.com/ayushRajak19)

```
```
