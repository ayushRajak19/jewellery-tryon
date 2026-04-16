from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from utils.landmark import detect_landmarks
from typing import Optional
import cv2
import numpy as np
import traceback
import json
import os

router = APIRouter()

ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg", "image/webp"]


@router.post("/tryon")
async def tryon(
        file:        UploadFile    = File(...),
        earring_id:  Optional[str] = Form(None),
        necklace_id: Optional[str] = Form(None)
):
    try:
        # Validate selection
        if not earring_id and not necklace_id:
            return JSONResponse(
                status_code=400,
                content={"detail": "Please select at least one jewellery item."}
            )

        # Read and validate image
        image_bytes = await file.read()
        nparr       = np.frombuffer(image_bytes, np.uint8)
        img         = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return JSONResponse(
                status_code=400,
                content={"detail": "Invalid image file."}
            )

        h, w     = img.shape[:2]
        center_x = w // 2
        center_y = h // 2

        # Detect face landmarks
        # detect_landmarks returns dict with keys:
        # left_ear, right_ear, nose_tip, chin, neck_center → each {"x": int, "y": int}
        landmarks = detect_landmarks(image_bytes)
        if not landmarks:
            return JSONResponse(
                status_code=422,
                content={"detail": "No face detected. Use a clear front-facing photo."}
            )

        # Safe coordinate reader
        # landmarks already contain PIXEL coordinates — do NOT multiply by w/h again
        def get_point(key, fallback_x, fallback_y):
            try:
                pt = landmarks[key]
                return int(pt["x"]), int(pt["y"])
            except (KeyError, TypeError):
                return fallback_x, fallback_y

        # Calculate face width for proportional sizing
        left_ear_x,  left_ear_y  = get_point("left_ear",  center_x - 120, center_y)
        right_ear_x, right_ear_y = get_point("right_ear", center_x + 120, center_y)
        chin_x,      chin_y      = get_point("chin",      center_x,       center_y + 150)
        neck_x,      neck_y      = get_point("neck_center", center_x,     center_y + 200)

        face_width    = max(right_ear_x - left_ear_x, 80)
        earring_size  = max(40, int(face_width * 0.20))
        necklace_size = max(120, int(face_width * 0.80))

        # Build response
        response_data = {
            "success":      True,
            "face_detected": True,
            "image_size": {          # ← REQUIRED by frontend
                "width":  w,
                "height": h
            }
        }

        # ── EARRINGS ──────────────────────────────
        if earring_id:
            response_data["earring_left"] = {
                "x":      left_ear_x  - earring_size // 2,
                "y":      left_ear_y  - earring_size // 4,
                "width":  earring_size,
                "height": int(earring_size * 1.5)
            }
            response_data["earring_right"] = {
                "x":      right_ear_x - earring_size // 2,
                "y":      right_ear_y - earring_size // 4,
                "width":  earring_size,
                "height": int(earring_size * 1.5)
            }

        # ── NECKLACE ──────────────────────────────
        if necklace_id:
            response_data["necklace"] = {
                "x":      neck_x - necklace_size // 2,
                "y":      neck_y - necklace_size // 6,
                "width":  necklace_size,
                "height": int(necklace_size * 0.75)
            }

        return JSONResponse(content=response_data)

    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"detail": f"Server error: {str(e)}"}
        )


@router.get("/catalogue")
async def catalogue():
    # Correct path — data/jewellery.json inside backend folder
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data", "jewellery.json"
    )

    try:
        with open(json_path, "r") as f:
            all_products = json.load(f)

        earrings  = [p for p in all_products if p.get("type") == "earring"]
        necklaces = [p for p in all_products if p.get("type") == "necklace"]

        return {"earrings": earrings, "necklaces": necklaces}

    except FileNotFoundError:
        print(f"File not found: {json_path}")
        return {"earrings": [], "necklaces": []}

    except Exception as e:
        print("Catalogue error:", e)
        return {"earrings": [], "necklaces": []}