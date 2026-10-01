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
