import mediapipe as mp
import numpy as np
from PIL import Image
import io

mp_face_mesh = mp.solutions.face_mesh

# MediaPipe Face Mesh landmark indices
# These are fixed indices from Google's 468-point face mesh model
LEFT_EAR       = 127
RIGHT_EAR      = 356
NOSE_TIP       = 1
CHIN           = 152
LEFT_SHOULDER  = 234
RIGHT_SHOULDER = 454

def detect_landmarks(image_bytes: bytes):
    # Convert raw bytes to PIL Image then numpy array
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_array = np.array(image)
    h, w = img_array.shape[:2]

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,       # True for photos, False for video
        max_num_faces=1,              # Only detect 1 face
        refine_landmarks=True,        # More accurate landmarks around eyes/lips
        min_detection_confidence=0.5  # 50% confidence threshold
    ) as face_mesh:

        results = face_mesh.process(img_array)

        # No face found in image
        if not results.multi_face_landmarks:
            return None

        landmarks = results.multi_face_landmarks[0].landmark

        # MediaPipe returns normalized coordinates (0.0 to 1.0)
        # Multiply by width/height to get actual pixel positions
        def get_point(idx):
            lm = landmarks[idx]
            return {
                "x": int(lm.x * w),
                "y": int(lm.y * h)
            }

        # Neck center = midpoint between shoulder landmarks
        neck_x = int(((landmarks[LEFT_SHOULDER].x + landmarks[RIGHT_SHOULDER].x) / 2) * w)
        neck_y = int(((landmarks[LEFT_SHOULDER].y + landmarks[RIGHT_SHOULDER].y) / 2) * h)

        return {
            "left_ear":    get_point(LEFT_EAR),
            "right_ear":   get_point(RIGHT_EAR),
            "nose_tip":    get_point(NOSE_TIP),
            "chin":        get_point(CHIN),
            "neck_center": {
            "x": int(landmarks[CHIN].x * w),
            "y": int(landmarks[CHIN].y * h) + 80  # Drops 80 pixels directly below your chin!
                 },
            "image_size":  {"width": w, "height": h}
        }