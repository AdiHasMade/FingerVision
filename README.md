# FingerVision

FingerVision is an augmented reality application that generates an interactive, real-time spatial portal in live webcam footage using advanced hand-tracking algorithms. By analyzing multi-hand gesture coordinates, FingerVision dynamically constructs $N$-sided geometric viewports that apply real-time image processing filters, particle effects, and dual-world frame blending.

---

## Features

- **Real-Time Hand Tracking:** Powered by MediaPipe Vision Tasks for multi-hand landmark extraction.
- **Dynamic $N$-Sided Geometry:** Generates custom convex hulls ($3 \to 10+$ vertices) based on extended fingertip coordinates across both hands.
- **Live Visual Pipeline:** Applies 9 high-performance OpenCV/NumPy filters directly within the portal or across the outer background.
- **Gesture-Based Filter Switching:** Integrated hysteresis and proximity detection to cycle filters seamlessly when hands close together.
- **Dual-World Rendering:** Toggle active processing between the portal interior and the exterior environment.
- **Perimeter Spark Engine:** Real-time physics-driven particle sparks rendered along geometry borders.
- **Frameless Telemetry HUD:** Displays active shape mode, selected filter title, and live FPS in Cascadia Mono font.

---

## Filters Included

| Filter | Description |
| :--- | :--- |
| `filtro_thermal` | Simulation of thermal camera using OpenCV `COLORMAP_JET` |
| `filtro_cyberpunk` | Vibrant neon blue and red channel amplification |
| `filtro_popart` | Adaptive edge thresholding with bilateral color filtering |
| `filtro_8bit` | Downscaled linear pixelation re-upscaled with nearest-neighbor |
| `filtro_xray` | Bitwise color inversion over single-channel grayscale |
| `filtro_nightvision` | High-gain green channel projection with noise matrix |
| `filtro_glitch` | Chromatic aberration with RGB channel separation |
| `filtro_hologram` | Cyan scanline multiplication with frame opacity blending |
| `filtro_neon` | Glowing Canny edge outlines with soft Gaussian bloom |

---

## Installation

### Prerequisites
- **Python 3.10+**
- A connected USB or integrated webcam

### Setup
1. **Clone the repository:**
```bash
   git clone https://github.com/AdiHasMade/FingerVision.git
   cd FingerVision

```


2. **Create a virtual environment:**
```bash
python -m venv venv

```


3. **Activate the environment:**
* **Windows:**
```bash
venv\Scripts\activate

```


* **macOS / Linux:**
```bash
source venv/bin/activate

```




4. **Install required dependencies:**
```bash
pip install opencv-python numpy mediapipe pillow

```



---

## Usage

Start the main pipeline:

```bash
python main.py

```

* **Generate Portal:** Raise one or both hands with 3 or more total fingers extended to build the viewport.
* **Cycle Filters:** Bring your hands close together to trigger the gesture transition.
* **Exit Application:** Press `q` with the video window in focus to exit.

> **Note:** On first launch, the required MediaPipe landmarker task model (`hand_landmarker.task`) will automatically download to your project directory.

---

## Project Structure

```text
FingerVision/
├── main.py              # Application entry point: video capture loop & telemetry HUD
├── hand_tracking.py     # Multi-finger extension detection & landmark processing
├── geometry.py          # Portal convex hull generation, particle engine & dual-world blending
├── filters.py           # Decorator-based registry & 9 custom image filters
├── hand_landmarker.task # MediaPipe gesture model
└── README.md

```

---

## Extend the Project

To add a custom filter, define a function in `filters.py` with the `@named` decorator that accepts a BGR image ROI (`numpy.ndarray`) and returns a processed array of the same dimensions:

```python
@named("My Custom Filter")
def filtro_nuevo(roi: np.ndarray) -> np.ndarray:
    return roi

```

Then append the new function to the `FILTERS` list at the bottom of `filters.py`. The filter switching sequence automatically accommodates any added functions.

---

## Technical Stack

* **Python 3.10**
* **OpenCV** (Image processing & spatial window management)
* **MediaPipe Tasks API** (Real-time hand landmarker tracking)
* **NumPy** (Array math & frame matrix operations)
* **Pillow** (Truetype font rendering for telemetry display)

---

## Acknowledgement

* Developed as an independent project by **([AdiHasMade](https://github.com/AdiHasMade))**.
* Hand tracking powered by **([Google MediaPipe](https://github.com/google-ai-edge/mediapipe))**.
* Computer vision processing powered by **([OpenCV](https://github.com/opencv/opencv))**.

---

## License

This project is a creation solely owned and developed by **[AdiHasMade](https://github.com/AdiHasMade)**. It is not affiliated with any university, academic institution, or corporate entity.

Distributed under the **Apache License 2.0**. You are free to use, modify, and distribute this software for personal or commercial purposes, provided that full copyright attribution is given to **[AdiHasMade](https://github.com/AdiHasMade)** and all modified files carry prominent notices stating that you changed the files.

```text
                                 Apache License
                           Version 2.0, January 2004
                        [http://www.apache.org/licenses/](http://www.apache.org/licenses/)

   Copyright 2026 AdiHasMade

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,Capacity or conditions of ANY KIND,
   either express or implied. See the License for the specific language
   governing permissions and limitations under the License.
