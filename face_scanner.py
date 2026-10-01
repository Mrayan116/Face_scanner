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

   with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True,
                               min_detection_confidence=0.5,
                               min_tracking_confidence=0.5) as face_mesh:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            image = cv2.flip(frame, 1)
            h, w = image.shape[:2]
            theme = THEMES[theme_names[theme_i]]
            MESH, TXT, ACC = theme["mesh"], theme["text"], theme["accent"]

            results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # FPS (smoothed)
            now = time.time()
            fps = 0.9 * fps + 0.1 * (1 / max(now - t_prev, 1e-6))
            t_prev = now

def eye_ratio(pts, idx):
    hor = np.linalg.norm(pts[idx[0]] - pts[idx[1]])
    ver = np.linalg.norm(pts[idx[2]] - pts[idx[3]])
    return ver / hor if hor else 0

           status = "NO SUBJECT"

            if results.multi_face_landmarks:
                lm = results.multi_face_landmarks[0].landmark
                pts = np.array([[p.x * w, p.y * h] for p in lm])
                status = "LOCKED"

                if show_mesh:
                    image = glowing_mesh(image, pts, MESH)

                # Bounding box + brackets
                x1, y1 = pts[:, 0].min().astype(int), pts[:, 1].min().astype(int)
                x2, y2 = pts[:, 0].max().astype(int), pts[:, 1].max().astype(int)
                corner_brackets(image, x1 - 15, y1 - 15, x2 + 15, y2 + 15, ACC)
                put_text(image, f"SUBJECT: {YOUR_NAME}", (x1 - 15, y2 + 45), ACC)

                # ---- Blinks (both eyes together, counted once) ----
                ear_l = eye_ratio(pts, LEFT_EYE_IDX)
                ear_r = eye_ratio(pts, RIGHT_EYE_IDX)
                left_open = ear_l > EYE_OPEN_THRESHOLD
                right_open = ear_r > EYE_OPEN_THRESHOLD
                closed = (not left_open) and (not right_open)
                if closed and not eyes_closed_prev:
                    blinks += 1
                eyes_closed_prev = closed

                # ---- Eye tiles (top-right) ----
                tile, pad = EYE_TILE, 20
                sx = w - tile - pad
                for n, (idx, is_open, label) in enumerate([
                    (LEFT_EYE_IDX, left_open, "L-EYE"),
                    (RIGHT_EYE_IDX, right_open, "R-EYE"),
                ]):
                    c = pts[idx[:4]].mean(axis=0).astype(int)
                    sy = pad + n * (tile + 50)
                    image[sy:sy + tile, sx:sx + tile] = crop_square(image, tuple(c), tile)
                    corner_brackets(image, sx - 4, sy - 4, sx + tile + 4, sy + tile + 4, MESH, 18, 2)
                    put_text(image, f"{label}: {'OPEN' if is_open else 'CLOSED'}",
                             (sx, sy + tile + 28), TXT)


                # ---- Head roll (real angle in degrees) ----
                p_l, p_r = pts[LEFT_EYE_IDX[0]], pts[RIGHT_EYE_IDX[1]]
                angle = np.degrees(np.arctan2(p_r[1] - p_l[1], p_r[0] - p_l[0]))
                cx = int((x1 + x2) / 2)
                cy = int(y1 - ROLL_GAP)
                dy = int(np.tan(np.radians(angle)) * ROLL_LINE_HALF)
                cv2.line(image, (cx - ROLL_LINE_HALF, cy - dy), (cx + ROLL_LINE_HALF, cy + dy), MESH, 3, cv2.LINE_AA)
                cv2.circle(image, (cx, cy), 5, ACC, -1, cv2.LINE_AA)
                put_text(image, f"ROLL {angle:+.1f} deg", (cx - 65, cy - 25), TXT)

                # ---- Mouth ring (scales with face size, so distance doesn't matter) ----
                lip_gap = np.linalg.norm(pts[MOUTH_TOP] - pts[MOUTH_BOTTOM])
                face_h = np.linalg.norm(pts[FOREHEAD] - pts[CHIN])
                openness = min(1.0, (lip_gap / face_h) / MOUTH_OPEN_FULL)
                radius = int(MOUTH_RING_MIN + openness * (MOUTH_RING_MAX - MOUTH_RING_MIN))
                mx = int(x1 - MOUTH_RING_DIST)
                my = int((pts[MOUTH_TOP][1] + pts[MOUTH_BOTTOM][1]) / 2)
                # faint guide ring (max size) + live ring + filled core
                cv2.circle(image, (mx, my), MOUTH_RING_MAX, MESH, 1, cv2.LINE_AA)
                cv2.circle(image, (mx, my), radius, ACC, 2, cv2.LINE_AA)
                cv2.circle(image, (mx, my), max(2, radius // 3), MESH, -1, cv2.LINE_AA)
                put_text(image, f"MOUTH {int(openness * 100)}%", (mx - 50, my - MOUTH_RING_MAX - 12), TXT)

            # ---- HUD panel (top-left) ----
            elapsed = int(time.time() - t_start)
            put_text(image, f"// {theme_names[theme_i]} SCANNER", (20, 35), ACC, 0.8)
            put_text(image, f"STATUS : {status}", (20, 65), TXT)
            put_text(image, f"BLINKS : {blinks}", (20, 90), TXT)
            put_text(image, f"FPS    : {fps:4.1f}", (20, 115), TXT)

cv2.imshow("Face Scanner", image)

            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord('q')):
                break
            elif key == ord('t'):
                theme_i = (theme_i + 1) % len(theme_names)
            elif key == ord('w'):
                show_mesh = not show_mesh
            elif key == ord('r'):
                blinks = 0
                t_start = time.time()
            elif key == ord('s'):
                name = f"scan_{int(time.time())}.png"
                cv2.imwrite(name, image)
                print("Saved", name)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

            put_text(image, f"UPTIME : {elapsed // 60:02d}:{elapsed % 60:02d}", (20, 140), TXT)
            put_text(image, "[T] theme  [W] mesh  [R] reset  [S] snap  [Q] quit",
                     (20, h - 20), TXT, 0.5)

