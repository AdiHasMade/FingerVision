import cv2
import numpy as np

def named(name):
    """Decorator to assign a HUD display name to a filter function."""

    def func_decorator(func):
        func.name = name
        return func

    return func_decorator

@named("Thermal Vision")
def filter_thermal(roi):
    return cv2.applyColorMap(
        cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY), cv2.COLORMAP_JET
    )

@named("Cyberpunk Synth")
def filter_cyberpunk(roi):
    img = roi.copy()
    img[:, :, 0] = cv2.add(img[:, :, 0], 50)
    img[:, :, 2] = cv2.add(img[:, :, 2], 60)
    return img

@named("Pop Art Comic")
def filter_comic(roi):
    gray = cv2.medianBlur(cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY), 5)
    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
    )
    return cv2.bitwise_and(
        cv2.bilateralFilter(roi, 9, 250, 250), roi, mask=edges
    )

@named("8-Bit Retro")
def filter_pixelate(roi, px=12):
    h, w = roi.shape[:2]
    small = cv2.resize(
        roi, (max(1, w // px), max(1, h // px)), interpolation=cv2.INTER_LINEAR
    )
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

@named("Inverted X-Ray")
def filter_xray(roi):
    return cv2.cvtColor(
        cv2.bitwise_not(cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)),
        cv2.COLOR_GRAY2BGR,
    )

@named("Night Vision")
def filter_night_vision(roi):
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    tint = np.zeros_like(roi)
    tint[:, :, 1] = cv2.add(
        gray, np.random.randint(0, 30, gray.shape, dtype=np.uint8)
    )
    return tint

@named("RGB Glitch")
def filter_glitch(roi):
    glitch = roi.copy()
    h, w = glitch.shape[:2]
    shift = max(2, w // 30)

    b, g, r = cv2.split(glitch)
    glitch = cv2.merge(
        [np.roll(b, -shift, axis=1), g, np.roll(r, shift, axis=1)]
    )

    for _ in range(max(1, h // 20)):
        y, slice_h = np.random.randint(0, max(1, h - 10)), np.random.randint(
            2, 8
        )
        glitch[y : y + slice_h, :] = np.roll(
            glitch[y : y + slice_h, :], np.random.randint(-15, 15), axis=1
        )
    return glitch

@named("Sci-Fi Hologram")
def filter_hologram(roi):
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    hologram = np.stack(
        [cv2.add(gray, 80), cv2.add(gray, 40), gray // 3], axis=-1
    )

    scanlines = np.ones(roi.shape[:2], dtype=np.uint8) * 255
    scanlines[::4, :] = 120
    scanlines = cv2.cvtColor(scanlines, cv2.COLOR_GRAY2BGR)

    return cv2.addWeighted(
        cv2.multiply(hologram, scanlines // 255), 0.85, roi, 0.15, 0
    )

@named("Neon Bloom")
def filter_neon_glow(roi):
    edges = cv2.dilate(
        cv2.Canny(cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY), 50, 150),
        np.ones((3, 3), np.uint8),
    )
    glow_mask = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    glow = np.zeros_like(roi)
    glow[:, :, 0], glow[:, :, 1], glow[:, :, 2] = 255, 220, 50
    colored = cv2.bitwise_and(glow, glow_mask)

    return cv2.add(cv2.add(roi, colored), cv2.GaussianBlur(colored, (21, 21), 0))

FILTROS = [
    filter_thermal,
    filter_cyberpunk,
    filter_comic,
    filter_pixelate,
    filter_xray,
    filter_night_vision,
    filter_glitch,
    filter_hologram,
    filter_neon_glow,
]