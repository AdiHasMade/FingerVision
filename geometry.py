import random
import cv2
import numpy as np
from hand_tracking import get_all_extended_finger_points

particles = []

def update_particles(frame, polygon_pts):
    global particles
    pts = polygon_pts.reshape(-1, 2)
    n = len(pts)

    for i in range(n):
        if random.random() < 0.4:
            p1, p2 = pts[i], pts[(i + 1) % n]
            a = random.random()
            x, y = int(p1[0] * a + p2[0] * (1 - a)), int(p1[1] * a + p2[1] * (1 - a))
            color = random.choice([
                (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 255, 255)
            ])
            particles.append([
                [x, y],
                [random.uniform(-2, 2), random.uniform(-3, -0.5)],
                random.randint(10, 20),
                color
            ])

    alive = []
    for pos, vel, life, color in particles:
        pos[0] += int(vel[0])
        pos[1] += int(vel[1])
        if life - 1 > 0:
            cv2.circle(frame, (pos[0], pos[1]), max(1, life // 5), color, -1)
            alive.append([pos, vel, life - 1, color])
    particles = alive

def get_dynamic_polygon_points(left_hand, right_hand, w, h):
    all_pts = get_all_extended_finger_points(left_hand, w, h) + \
              get_all_extended_finger_points(right_hand, w, h)
    if len(all_pts) >= 3:
        hull = cv2.convexHull(np.array(all_pts, dtype=np.int32))
        _, _, bw, _ = cv2.boundingRect(hull)
        return True, hull, float(bw)
    return False, None, 0.0

class ClosingGestureDetector:
    def __init__(self, close_ratio=0.16, open_ratio=0.30):
        self.c_ratio, self.o_ratio, self.is_closed = close_ratio, open_ratio, False

    def update(self, width, frame_w):
        triggered = False
        if not self.is_closed and width < self.c_ratio * frame_w:
            self.is_closed = True
            triggered = True
        elif self.is_closed and width > self.o_ratio * frame_w:
            self.is_closed = False
        return triggered

def render_portal(frame, polygon_pts, filtro_func, invert_world=True):
    """
    Renders Dual-World Portal:
    - invert_world=True  : Outer world is filtered, inside portal is normal.
    - invert_world=False : Inside portal is filtered, outer world is normal.
    """
    h, w = frame.shape[:2]

    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(mask, [polygon_pts], 255)
    mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR).astype(np.float32) / 255.0

    if invert_world:
        filtered_world = filtro_func(frame.copy())
        blended = (frame * mask_3ch + filtered_world * (1.0 - mask_3ch)).astype(np.uint8)
    else:
        x, y, bw, bh = cv2.boundingRect(polygon_pts)
        x, y, bw, bh = max(x, 0), max(y, 0), min(bw, w - x), min(bh, h - y)
        if bw <= 1 or bh <= 1:
            return frame
        
        roi = frame[y:y+bh, x:x+bw]
        filtered_roi = filtro_func(roi)
        mask_roi = mask_3ch[y:y+bh, x:x+bw]
        
        blended = frame.copy()
        blended[y:y+bh, x:x+bw] = (filtered_roi * mask_roi + roi * (1.0 - mask_roi)).astype(np.uint8)

    np.copyto(frame, blended)

    cv2.polylines(frame, [polygon_pts], isClosed=True, color=(255, 255, 255), thickness=2)
    update_particles(frame, polygon_pts)
    return frame