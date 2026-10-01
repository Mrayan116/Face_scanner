# Face Scanner

A real-time computer vision project that uses Python, OpenCV, and MediaPipe to track facial features through a webcam and display a futuristic HUD.

The scanner detects a face and provides live information about eye state, blinks, mouth movement, head roll, FPS, and system uptime.

## Features

- Real-time face tracking using MediaPipe
- 3D-style facial mesh overlay
- Eye tracking
  - Left eye open/closed status
  - Right eye open/closed status
- Blink counter
- Mouth openness percentage
- Head roll angle in degrees
- Face detection bounding brackets
- FPS counter
- Scanner uptime
- Multiple visual themes
- Toggleable face mesh
- Screenshot capture
- Keyboard controls

## Preview

The application opens a webcam window with a live scanner-style HUD around the detected face.

## Technologies

- Python 3.12
- OpenCV
- MediaPipe
- NumPy

## Project Structure

```text
face_scanner/
│
├── face_scanner.py
├── README.md
└── .venv/
```

`.venv` is the local Python virtual environment and should not be uploaded to GitHub.

## Requirements

- Windows
- Python 3.12
- Webcam
- OpenCV
- MediaPipe
- NumPy

Python 3.12 is recommended because this project uses the MediaPipe `mp.solutions.face_mesh` API.

## Setup

### 1. Clone the repository

```powershell
git clone YOUR_REPOSITORY_URL
cd face_scanner
```

### 2. Create a virtual environment

```powershell
py -3.12 -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see:

```text
(.venv)
```

at the beginning of your terminal.

### 4. Install dependencies

```powershell
python -m pip install mediapipe==0.10.14 opencv-python numpy
```

### 5. Run the program

```powershell
python face_scanner.py
```

Your webcam should open automatically.

## Configuration

The project has a section near the top of `face_scanner.py` called:

```python
# MAKE IT YOURS - edit this section
```

You can change the name displayed on the scanner:

```python
YOUR_NAME = "Muhammad Rayan"
```

You can also change the scanner themes, mesh appearance, text size, eye detection threshold, mouth ring size, camera resolution, and other settings.

## Controls

| Key | Action |
|---|---|
| `T` | Change scanner theme |
| `W` | Show/hide face mesh |
| `R` | Reset blink counter and uptime |
| `S` | Save a screenshot |
| `Q` | Quit |
| `ESC` | Quit |

## Scanner Information

### Face Mesh

MediaPipe Face Mesh detects facial landmarks and connects them to create the live facial mesh.

### Blink Detection

The program calculates an eye aspect ratio using selected eye landmarks.

When both eyes are detected as closed, the blink counter increases.

### Mouth Detection

The distance between the upper and lower lip landmarks is compared with the detected face height.

This produces a percentage representing mouth openness.

### Head Roll

The program calculates the angle between the left and right eye landmarks to estimate how much the head is tilted sideways.

### FPS

The scanner calculates and smooths the current frame rate so the HUD can display a more stable FPS value.

## Themes

The scanner includes four built-in themes:

- SYNTHWAVE
- TOXIC
- ICE
- BLOOD

Press `T` while the scanner is running to switch between them.

## Screenshots

Screenshots can be saved while the program is running by pressing:

```text
S
```

The image will be saved in the current project directory with a filename similar to:

```text
scan_1727812345.png
```

## Troubleshooting

### MediaPipe does not have `solutions`

If you see:

```text
AttributeError: module 'mediapipe' has no attribute 'solutions'
```

check your MediaPipe version:

```powershell
python -c "import mediapipe as mp; print(mp.__version__)"
```

This project uses the older MediaPipe API, so MediaPipe `0.10.14` is recommended.

### Make sure the correct Python version is active

Run:

```powershell
python --version
```

You should see:

```text
Python 3.12.x
```

If you see Python 3.13, activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Webcam does not open

Make sure:

- Your webcam is connected
- No other application is using the camera
- Windows has given VS Code/Python permission to access the camera
- `CAM_INDEX` is set correctly

The default camera index is:

```python
CAM_INDEX = 0
```

If you have multiple cameras, you can try:

```python
CAM_INDEX = 1
```

## Future Improvements

Possible improvements include:

- Hand tracking
- Face recognition
- Multiple face tracking
- Facial expression detection
- Eye gaze tracking
- Face distance estimation
- Recording scanner sessions
- More HUD animations
- Custom user themes
- Web-based version
- Performance improvements

## Author

**Muhammad Rayan**

Software Engineering student at the University of Guelph.

GitHub: `https://github.com/Mrayan116`

LinkedIn: `www.linkedin.com/in/muhammad-rayan26`
