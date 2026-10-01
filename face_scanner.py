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


def put_text(img, text, pos, color, scale=TEXT_SCALE):
    """Text with a dark outline so it stays readable on any background."""
    cv2.putText(img, text, pos, TEXT_FONT, scale, (0, 0, 0), TEXT_THICK + 3, cv2.LINE_AA)
    cv2.putText(img, text, pos, TEXT_FONT, scale, color, TEXT_THICK, cv2.LINE_AA)


def corner_brackets(img, x1, y1, x2, y2, color, length=30, thick=3):
    for (x, y, dx, dy) in [(x1, y1, 1, 1), (x2, y1, -1, 1), (x1, y2, 1, -1), (x2, y2, -1, -1)]:
        cv2.line(img, (x, y), (x + dx * length, y), color, thick, cv2.LINE_AA)
        cv2.line(img, (x, y), (x, y + dy * length), color, thick, cv2.LINE_AA)


def glowing_mesh(image, pts, color):
    layer = np.zeros_like(image)
    for i, j in mp_face_mesh.FACEMESH_TESSELATION:
        cv2.line(layer, tuple(pts[i].astype(int)), tuple(pts[j].astype(int)), color, 1, cv2.LINE_AA)
    glow = cv2.GaussianBlur(layer, (0, 0), GLOW_BLUR)
    out = cv2.addWeighted(image, 1.0, glow, GLOW_STRENGTH, 0)
    return cv2.addWeighted(out, 1.0, layer, MESH_OPACITY, 0)


def crop_square(image, center, size):
    x, y = center
    half = size // 2
    h, w = image.shape[:2]
    crop = image[max(0, y - half):min(h, y + half), max(0, x - half):min(w, x + half)]
    if crop.size == 0:
        return np.zeros((size, size, 3), np.uint8)
    return cv2.resize(crop, (size, size))

# =====================================================================
#  Main
# =====================================================================
def main():
    cap = cv2.VideoCapture(CAM_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)

    theme_names = list(THEMES)
    theme_i = theme_names.index(START_THEME)
    show_mesh = True
    blinks = 0
    eyes_closed_prev = False
    t_prev, fps = time.time(), 0.0
    t_start = time.time()
def eye_ratio(pts, idx):
    hor = np.linalg.norm(pts[idx[0]] - pts[idx[1]])
    ver = np.linalg.norm(pts[idx[2]] - pts[idx[3]])
    return ver / hor if hor else 0
