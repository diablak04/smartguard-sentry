"""Demo Fazy 1: kamera + detekcja ludzi (YOLO) + strefa ochrony + FPS.

Czerwona ramka = osoba stoi W STREFIE (zagrozenie).
Szara ramka    = osoba poza strefa (ignorowana).

Uruchom:  .venv\\Scripts\\python.exe detekcja_test.py
Wyjscie:  klawisz 'q' w oknie.
"""
import time
import cv2
from capture import Camera
from config import wczytaj_config
from detector import Detector
import zona


def main():
    config = wczytaj_config()
    strefa = config["strefa"]

    cam = Camera(config.get("kamera_glowna", 0)).start()
    det = Detector(config["yolo_model"], config["yolo_prog_pewnosci"])
    time.sleep(1.0)
    print("Nacisnij 'q' w oknie, zeby zakonczyc.")

    while True:
        frame = cam.read()
        if frame is None:
            continue
        h, w = frame.shape[:2]
        zona.rysuj_strefe(frame, strefa)

        for box in det.wykryj_ludzi(frame):
            x1, y1, x2, y2, conf = box
            stopa = zona.stopa_celu(box)
            w_strefie = zona.punkt_w_strefie(stopa, strefa, w, h)
            kolor = (0, 0, 255) if w_strefie else (160, 160, 160)
            etyk = "W STREFIE" if w_strefie else "poza"
            cv2.rectangle(frame, (x1, y1), (x2, y2), kolor, 2)
            cv2.circle(frame, stopa, 4, kolor, -1)
            cv2.putText(frame, f"person {conf:.2f} [{etyk}]", (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, kolor, 2)

        fps = 1000.0 / det.ostatni_ms if det.ostatni_ms else 0.0
        cv2.putText(frame, f"{det.ostatni_ms:.0f} ms  ({fps:.1f} FPS)", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.imshow("SmartGuard - F1 detekcja + strefa", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
