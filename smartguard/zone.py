"""Strefa ochrony — wielokat w znormalizowanych wspolrzednych (0-1).

Czlowiek jest 'w strefie', gdy punkt jego stop (dol-srodek ramki detekcji)
lezy wewnatrz wielokata. Strefa trzymana w config.json jako [[x,y], ...] w
zakresie 0-1 — dzieki temu jest niezalezna od rozdzielczosci kamery.
"""
import numpy as np
import cv2


def stopa_celu(box):
    """Punkt stop celu = dol-srodek prostokata detekcji (x1, y1, x2, y2)."""
    x1, _, x2, y2 = box[:4]
    return ((x1 + x2) // 2, y2)


def _na_piksele(strefa_norm, w, h):
    return np.array([[int(x * w), int(y * h)] for x, y in strefa_norm], dtype=np.int32)


def punkt_w_strefie(punkt, strefa_norm, w, h) -> bool:
    """True, jesli punkt (px, py) lezy wewnatrz strefy (cv2 ray-casting)."""
    poly = _na_piksele(strefa_norm, w, h)
    return cv2.pointPolygonTest(poly, (float(punkt[0]), float(punkt[1])), False) >= 0


def rysuj_strefe(frame, strefa_norm, kolor=(255, 180, 0)) -> None:
    """Rysuje obrys strefy na klatce (kolor BGR)."""
    h, w = frame.shape[:2]
    poly = _na_piksele(strefa_norm, w, h)
    cv2.polylines(frame, [poly], isClosed=True, color=kolor, thickness=2)
