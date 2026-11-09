"""Odczyt obrazu z kamery w osobnym watku.

Watek ciagle czyta najnowsza klatke do bufora, a glowna petla pobiera ja
przez read() — dzieki temu detekcja nie blokuje odczytu i odwrotnie.
"""
import threading
import cv2


class Camera:
    def __init__(self, src=0):
        self.src = src                       # 0 = pierwsza kamera; moze byc tez plik/RTSP
        self.cap = cv2.VideoCapture(src)
        self.frame = None
        self.running = False
        self.lock = threading.Lock()
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._reader, daemon=True)
        self.thread.start()
        return self

    def _reader(self):
        while self.running:
            ok, frame = self.cap.read()
            if not ok:
                continue                     # zerwany strumien -> probuj dalej
            with self.lock:
                self.frame = frame

    def read(self):
        """Zwraca kopie najnowszej klatki (lub None, jesli jeszcze brak)."""
        with self.lock:
            return None if self.frame is None else self.frame.copy()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        self.cap.release()
