"""Podglad detekcji: kamera + detekcja ludzi (YOLO) + strefa ochrony + FPS.

Czerwona ramka = osoba stoi W STREFIE (zagrozenie).
Szara ramka    = osoba poza strefa (ignorowana).

Uruchom:  python main.py preview
Wyjscie:  klawisz 'q' w oknie.
"""
import time
import cv2
from smartguard import zone
from smartguard.capture import Camera
from smartguard.config import load_config
from smartguard.detector import Detector


def run() -> None:
    config = load_config()
    zone_norm = config["zone"]

    cam = Camera(config["camera"]["main"]).start()
    det = Detector(config["yolo"]["model"], config["yolo"]["confidence"])
    time.sleep(1.0)
    print("Nacisnij 'q' w oknie, zeby zakonczyc.")

    while True:
        frame = cam.read()
        if frame is None:
            continue
        h, w = frame.shape[:2]
        zone.draw_zone(frame, zone_norm)

        for box in det.detect_people(frame):
            x1, y1, x2, y2, conf = box
            foot = zone.target_foot(box)
            inside = zone.point_in_zone(foot, zone_norm, w, h)
            color = (0, 0, 255) if inside else (160, 160, 160)
            label = "W STREFIE" if inside else "poza"
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.circle(frame, foot, 4, color, -1)
            cv2.putText(frame, f"person {conf:.2f} [{label}]", (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        fps = 1000.0 / det.last_ms if det.last_ms else 0.0
        cv2.putText(frame, f"{det.last_ms:.0f} ms  ({fps:.1f} FPS)", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.imshow("SmartGuard - podglad detekcji", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.stop()
    cv2.destroyAllWindows()

