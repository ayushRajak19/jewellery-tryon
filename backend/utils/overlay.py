import cv2
import numpy as np
from PIL import Image
import io
import os

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "jewellery")

def load_jewellery_png(filename: str):
    """
    Load a PNG jewellery image with transparency (RGBA).
    Returns None if file not found.
    """
    path = os.path.join(STATIC_DIR, filename)
    if not os.path.exists(path):
        return None
    # Read with alpha channel (transparency)
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        return None
    # If image has no alpha channel, add one
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    return img

def overlay_png(background, overlay, x, y, size):
    """
    Place overlay PNG on background image at position (x, y).
    x, y = CENTER point where jewellery should be placed.
    size = width in pixels (height scales proportionally).
    """
    if overlay is None:
        return background

    # Resize overlay maintaining aspect ratio
    h_orig, w_orig = overlay.shape[:2]
    aspect = h_orig / w_orig
    new_w = size
    new_h = int(size * aspect)
    overlay_resized = cv2.resize(overlay, (new_w, new_h))

    # Calculate top-left corner from center point
    x1 = x - new_w // 2
    y1 = y - new_h // 2
    x2 = x1 + new_w
    y2 = y1 + new_h

    # Make sure overlay fits within image bounds
    bg_h, bg_w = background.shape[:2]

    # Clip to image boundaries
    if x1 < 0: x1 = 0
    if y1 < 0: y1 = 0
    if x2 > bg_w: x2 = bg_w
    if y2 > bg_h: y2 = bg_h

    # Recalculate overlay crop if clipped
    ov_x1 = max(0, -(x - new_w // 2))
    ov_y1 = max(0, -(y - new_h // 2))
    ov_x2 = ov_x1 + (x2 - x1)
    ov_y2 = ov_y1 + (y2 - y1)

    if x2 <= x1 or y2 <= y1:
        return background

    overlay_crop = overlay_resized[ov_y1:ov_y2, ov_x1:ov_x2]

    if overlay_crop.shape[0] == 0 or overlay_crop.shape[1] == 0:
        return background

    # Alpha blending — merge jewellery with photo using transparency
    alpha = overlay_crop[:, :, 3] / 255.0  # transparency mask (0.0 to 1.0)

    for c in range(3):  # blend R, G, B channels
        background[y1:y2, x1:x2, c] = (
            alpha * overlay_crop[:, :, c] +
            (1 - alpha) * background[y1:y2, x1:x2, c]
        )

    return background


def apply_tryon(image_bytes: bytes, landmarks: dict,
                earring_id: str = None, necklace_id: str = None,
                ear_dx: int = 0, ear_dy: int = 0,
                neck_dx: int = 0, neck_dy: int = 0) -> bytes:
    """
    Main function — takes photo + landmarks + jewellery IDs + Manual Adjustments
    Returns final image bytes with jewellery overlaid
    """
    # Load original photo
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_array = np.array(image)
    # Convert RGB to BGR for OpenCV
    bg = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    face_width = landmarks["right_ear"]["x"] - landmarks["left_ear"]["x"]

    # ── EARRINGS ──────────────────────────────────────────────
    if earring_id:
        earring = load_jewellery_png(f"{earring_id}.png")

        if earring is not None:
            # Earring size = 18% of face width
            earring_size = max(30, int(face_width * 0.18))

            # Place on LEFT ear (Subtracting ear_dx pushes it further LEFT/Outward)
            bg = overlay_png(
                bg, earring,
                x=landmarks["left_ear"]["x"] - ear_dx,
                y=landmarks["left_ear"]["y"] + ear_dy,
                size=earring_size
            )

            # Flip earring horizontally for RIGHT ear
            earring_flipped = cv2.flip(earring, 1)

            # Place on RIGHT ear (Adding ear_dx pushes it further RIGHT/Outward)
            bg = overlay_png(
                bg, earring_flipped,
                x=landmarks["right_ear"]["x"] + ear_dx,
                y=landmarks["right_ear"]["y"] + ear_dy,
                size=earring_size
            )

    # ── NECKLACE ──────────────────────────────────────────────
    if necklace_id:
        necklace = load_jewellery_png(f"{necklace_id}.png")

        if necklace is not None:
            # Necklace width = 60% of face width
            necklace_size = max(80, int(face_width * 0.70))

            # Place centered on neck (Add manual adjustments directly)
            bg = overlay_png(
                bg, necklace,
                x=landmarks["neck_center"]["x"] + neck_dx,
                y=landmarks["neck_center"]["y"] + neck_dy,
                size=necklace_size
            )

    # Convert back to RGB and return as bytes
    result_rgb = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)
    result_image = Image.fromarray(result_rgb)
    output = io.BytesIO()
    result_image.save(output, format="JPEG", quality=95)
    return output.getvalue()