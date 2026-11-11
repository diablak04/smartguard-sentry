"""Strefa ochrony — wielokat w znormalizowanych wspolrzednych (0-1).

Czlowiek jest 'w strefie', gdy punkt jego stop (dol-srodek ramki detekcji)
lezy wewnatrz wielokata. Strefa trzymana w config.json jako [[x,y], ...] w
zakresie 0-1 — dzieki temu jest niezalezna od rozdzielczosci kamery.
"""
import numpy as np
import cv2


def target_foot(box):
    """Punkt stop celu = dol-srodek prostokata detekcji (x1, y1, x2, y2)."""
    x1, _, x2, y2 = box[:4]
    return ((x1 + x2) // 2, y2)


def _to_pixels(zone_norm, w, h):
    return np.array([[int(x * w), int(y * h)] for x, y in zone_norm], dtype=np.int32)


def point_in_zone(point, zone_norm, w, h) -> bool:
    """True, jesli punkt (px, py) lezy wewnatrz strefy (cv2 ray-casting)."""
    poly = _to_pixels(zone_norm, w, h)
    return cv2.pointPolygonTest(poly, (float(point[0]), float(point[1])), False) >= 0


def draw_zone(frame, zone_norm, color=(255, 180, 0)) -> None:
    """Rysuje obrys strefy na klatce (kolor BGR)."""
    h, w = frame.shape[:2]
    poly = _to_pixels(zone_norm, w, h)
    cv2.polylines(frame, [poly], isClosed=True, color=color, thickness=2)
