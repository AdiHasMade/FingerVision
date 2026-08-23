import os
import time
import urllib.request
import cv2
import numpy as np
import mediapipe as mp
from PIL import Image, ImageDraw, ImageFont

from filters import FILTROS
from geometry import (
    ClosingGestureDetector,
    get_dynamic_polygon_points,
    render_portal,
)

MODEL_PATH = "hand_landmarker.task"
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
SHAPES = {
    3: "TRIANGLE",
    4: "QUADRILATERAL",
    5: "PENTAGON",
    6: "HEXAGON",
    7: "HEPTAGON",
    8: "OCTAGON",
}

FONT_PATH = next(
    (
        p
        for p in [
            "C:\\Windows\\Fonts\\CascadiaMono-SemiLight.ttf",
            "C:\\Windows\\Fonts\\CascadiaMono.ttf",
            "CascadiaMono.ttf",
        ]
        if os.path.exists(p)
    ),
    None,
)
hud_font = (
    ImageFont.truetype(FONT_PATH, 22) if FONT_PATH else ImageFont.load_default()
)
GREY = (224, 224, 224)

def draw_hud(frame, polygon_pts, filtro, fps):
    h, w = frame.shape[:2]
    pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    m = 25

    n = len(polygon_pts) if polygon_pts is not None else 0
    shape_str = f"PORTAL: {SHAPES.get(n, f'{n}-GON' if n else 'NONE (3+ FINGERS)')}"
    draw.text((m, m), shape_str, font=hud_font, fill=GREY)

    filt_str = f"FILTER: {getattr(filtro, 'name', 'CUSTOM').upper()}"
    fw = draw.textbbox((0, 0), filt_str, font=hud_font)[2]
    draw.text((w - fw - m, m), filt_str, font=hud_font, fill=GREY)

    fps_str = f"FPS: {int(fps)}"
    fps_w, fps_h = draw.textbbox((0, 0), fps_str, font=hud_font)[2:]
    draw.text((w - fps_w - m, h - fps_h - m - 10), fps_str, font=hud_font, fill=GREY)

    np.copyto(frame, cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR))


def main():
    if not os.path.exists(MODEL_PATH):
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

    options = mp.tasks.vision.HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_hands=2,
    )

    cap = cv2.VideoCapture(0)
    filtro_idx, detector, p_time = 0, ClosingGestureDetector(), 0

    with mp.tasks.vision.HandLandmarker.create_from_options(options) as marker:
        start_t = time.time()
        while cap.isOpened():
            ok, frame = cap.read()
            if not ok:
                break

            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]
            ts = int((time.time() - start_t) * 1000)
            res = marker.detect_for_video(
                mp.Image(
                    image_format=mp.ImageFormat.SRGB,
                    data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                ),
                ts,
            )

            left, right = None, None
            if res.hand_landmarks and res.handedness:
                for lm, hd in zip(res.hand_landmarks, res.handedness):
                    label = (
                        "Right"
                        if hd[0].category_name == "Left"
                        else "Left"
                    )
                    if label == "Left" and not left:
                        left = lm
                    elif label == "Right" and not right:
                        right = lm
                if len(res.hand_landmarks) == 2 and not (left and right):
                    left, right = res.hand_landmarks[:2]

            valid, pts, width = get_dynamic_polygon_points(left, right, w, h)
            if valid:
                if detector.update(width, w):
                    filtro_idx = (filtro_idx + 1) % len(FILTROS)
                frame = render_portal(frame, pts, FILTROS[filtro_idx], invert_world=True) #To get to CLASSIC WORLD(..., invert_world=False)

            c_time = time.time()
            fps = 1 / (c_time - p_time) if p_time else 0
            p_time = c_time

            draw_hud(frame, pts if valid else None, FILTROS[filtro_idx], fps)
            cv2.imshow("Portal Filter App", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()