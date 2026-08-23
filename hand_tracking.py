import numpy as np

TIPS = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

def _to_pt(lm, w, h):
    return np.array([lm.x * w, lm.y * h])

def get_all_extended_finger_points(hand, w, h):
    if not hand:
        return []
    lm = hand.landmark if hasattr(hand, "landmark") else hand
    wrist = _to_pt(lm[0], w, h)

    open_pts = []
    
    for tip, pip, mcp in [(8, 6, 5), (12, 10, 9), (16, 14, 13), (20, 18, 17)]:
        p_tip, p_pip, p_mcp = (
            _to_pt(lm[tip], w, h),
            _to_pt(lm[pip], w, h),
            _to_pt(lm[mcp], w, h),
        )
        v_base, v_finger = p_mcp - wrist, p_tip - p_mcp
        align = np.dot(v_base, v_finger) / (
            np.linalg.norm(v_base) * np.linalg.norm(v_finger) + 1e-6
        )
        if align > 0.4 and np.linalg.norm(p_tip - wrist) > np.linalg.norm(
            p_pip - wrist
        ):
            open_pts.append((int(p_tip[0]), int(p_tip[1])))

    p_thumb, p_pinky_mcp = _to_pt(lm[4], w, h), _to_pt(lm[17], w, h)
    if (
        np.linalg.norm(p_thumb - p_pinky_mcp)
        > np.linalg.norm(_to_pt(lm[2], w, h) - p_pinky_mcp) * 1.2
    ):
        open_pts.append((int(p_thumb[0]), int(p_thumb[1])))

    return open_pts