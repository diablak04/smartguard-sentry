"""Kalibrator strefy: klikaj punkty na obrazie z kamery i zapisz je do config.json.

Sterowanie (w oknie):
  LPM (lewy przycisk myszy) - dodaj punkt wielokata
  z - zapisz strefe do config.json
  r - wyczysc punkty i zacznij od nowa
  q - wyjscie (bez zapisu)

Zapisuje wspolrzedne znormalizowane (0-1), wiec strefa zadziala przy kazdej rozdzielczosci.
"""
import json
import time
from pathlib import Path
import cv2
from capture import Camera

CONFIG = Path("config.json")
punkty = []  # punkty w pikselach


def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        punkty.append((x, y))


def main():
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    cam = Camera(config.get("kamera_glowna", 0)).start()
    time.sleep(1.0)
    cv2.namedWindow("Kalibracja strefy")
    cv2.setMouseCallback("Kalibracja strefy", on_mouse)
    print("LPM=dodaj punkt | z=zapisz | r=reset | q=wyjscie")

    while True:
        frame = cam.read()
        if frame is None:
            continue
        h, w = frame.shape[:2]

        for i, p in enumerate(punkty):
            cv2.circle(frame, p, 5, (0, 255, 0), -1)
            if i > 0:
                cv2.line(frame, punkty[i - 1], p, (0, 255, 0), 2)
        if len(punkty) > 2:
            cv2.line(frame, punkty[-1], punkty[0], (0, 255, 0), 1)  # domkniecie

        cv2.putText(frame, f"punkty: {len(punkty)} (min 3) | z=zapisz r=reset q=wyjscie",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow("Kalibracja strefy", frame)

        k = cv2.waitKey(1) & 0xFF
        if k == ord("q"):
            break
        elif k == ord("r"):
            punkty.clear()
        elif k == ord("z") and len(punkty) >= 3:
            strefa = [[round(x / w, 3), round(y / h, 3)] for (x, y) in punkty]
            config["strefa"] = strefa
            CONFIG.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
            print("Zapisano strefe do config.json:", strefa)

    cam.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
