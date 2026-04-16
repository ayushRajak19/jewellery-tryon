from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.landmark import detect_landmarks
from models.schemas import DetectResponse

router = APIRouter()

ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg", "image/webp"]

@router.post("/detect", response_model=DetectResponse)
async def detect(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Only JPG/PNG allowed."
        )

    image_bytes = await file.read()

    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum 10MB."
        )

    landmarks = detect_landmarks(image_bytes)

    if not landmarks:
        raise HTTPException(
            status_code=422,
            detail="No face detected. Use a clear front-facing photo."
        )

    return DetectResponse(success=True, landmarks=landmarks)