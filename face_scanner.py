import time
import cv2
import mediapipe as mp
import numpy as np

YOUR_NAME = "Muhammad Rayan"     # can be changed to whoevers 

# Themes are (B, G, R). Press T while running to cycle through them.
THEMES = {
    "SYNTHWAVE": {"mesh": (200, 0, 255),   "text": (255, 255, 0),   "accent": (0, 140, 255)},
    "TOXIC":     {"mesh": (80, 255, 0),    "text": (200, 255, 200), "accent": (0, 255, 255)},
    "ICE":       {"mesh": (255, 200, 60),  "text": (255, 255, 255), "accent": (255, 120, 0)},
    "BLOOD":     {"mesh": (40, 40, 255),   "text": (200, 200, 255), "accent": (0, 200, 255)},
}
START_THEME = "SYNTHWAVE"

# Mesh look
GLOW_STRENGTH = 0.9        # 0 = no glow, 1+ = very glowy
GLOW_BLUR = 7              # bigger = softer glow
MESH_OPACITY = 0.55

# Text
TEXT_FONT = cv2.FONT_HERSHEY_DUPLEX
TEXT_SCALE = 0.6
TEXT_THICK = 1


# Mouth ring (placed to the left of the face)
MOUTH_RING_DIST = 110      # how far left of the face the ring sits
MOUTH_RING_MIN = 8
MOUTH_RING_MAX = 55
MOUTH_OPEN_FULL = 0.16     # lip gap / face height that counts as 100% open

# Head roll gauge (above the head)
ROLL_GAP = 70              # distance above the head
ROLL_LINE_HALF = 80

# Eye tiles (top-right)
EYE_TILE = 140
EYE_OPEN_THRESHOLD = 0.22  # lower = harder to count as closed

# Camera
CAM_INDEX = 0
FRAME_W, FRAME_H = 1280, 720

# =====================================================================
#  Landmarks
# =====================================================================
mp_face_mesh = mp.solutions.face_mesh
LEFT_EYE_IDX = [33, 133, 159, 145]
RIGHT_EYE_IDX = [362, 263, 386, 374]
MOUTH_TOP, MOUTH_BOTTOM = 13, 14
FOREHEAD, CHIN = 10, 152


# =====================================================================
#  Helpers
# =====================================================================
def eye_ratio(pts, idx):
    hor = np.linalg.norm(pts[idx[0]] - pts[idx[1]])
    ver = np.linalg.norm(pts[idx[2]] - pts[idx[3]])
    return ver / hor if hor else 0
