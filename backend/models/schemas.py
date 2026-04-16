from pydantic import BaseModel
from typing import Optional

class Point(BaseModel):
    x: int
    y: int

class ImageSize(BaseModel):
    width: int
    height: int

class LandmarkResponse(BaseModel):
    left_ear:    Point
    right_ear:   Point
    nose_tip:    Point
    chin:        Point
    neck_center: Point
    image_size:  ImageSize

class DetectResponse(BaseModel):
    success:   bool
    landmarks: LandmarkResponse

class TryOnRequest(BaseModel):
    earring_id:  Optional[str] = None   # e.g. "earring1"
    necklace_id: Optional[str] = None   # e.g. "necklace1"