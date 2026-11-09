"""Detekcja ludzi modelem YOLO (yolo11n).

Model jest GOTOWY — nie trenujemy. Filtrujemy tylko klase 'person' (0).
Mierzymy czas inferencji (wymog: < 200 ms/klatke, cel 3-5 FPS na CPU).
"""
import time
from ultralytics import YOLO


class Detector:
    def __init__(self, model_path: str = "yolo11n.pt", prog: float = 0.5, imgsz: int = 640):
        self.model = YOLO(model_path)
        self.prog = prog            # prog pewnosci
        self.imgsz = imgsz          # rozdzielczosc wejscia (zmniejsz dla wiekszego FPS)
        self.ostatni_ms = 0.0       # czas ostatniej inferencji [ms]

    def wykryj_ludzi(self, frame):
        """Zwraca liste wykryc [(x1, y1, x2, y2, conf), ...] tylko dla ludzi."""
        t0 = time.perf_counter()
        wynik = self.model(frame, classes=[0], conf=self.prog,
                           imgsz=self.imgsz, verbose=False)[0]
        self.ostatni_ms = (time.perf_counter() - t0) * 1000.0

        wykrycia = []
        for box in wynik.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            wykrycia.append((x1, y1, x2, y2, conf))
        return wykrycia
