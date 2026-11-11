"""Kalibrator strefy: klikaj punkty na obrazie z kamery i zapisz je do config.local.json.

Sterowanie (w oknie):
  LPM (lewy przycisk myszy) - dodaj punkt wielokata
  z - zapisz strefe (do config.local.json - tylko ten komputer, nie trafia do gita)
  r - wyczysc punkty i zacznij od nowa
  q - wyjscie (bez zapisu)

Zapisuje wspolrzedne znormalizowane (0-1), wiec strefa zadziala przy kazdej rozdzielczosci.
"""
import time
import cv2
from smartguard.capture import Camera
from smartguard.config import load_config, save_local

points = []  # punkty w pikselach


def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))


def main():
    config = load_config()
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

        for i, p in enumerate(points):
            cv2.circle(frame, p, 5, (0, 255, 0), -1)
            if i > 0:
                cv2.line(frame, points[i - 1], p, (0, 255, 0), 2)
        if len(points) > 2:
            cv2.line(frame, points[-1], points[0], (0, 255, 0), 1)  # domkniecie

        cv2.putText(frame, f"punkty: {len(points)} (min 3) | z=zapisz r=reset q=wyjscie",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow("Kalibracja strefy", frame)

        k = cv2.waitKey(1) & 0xFF
        if k == ord("q"):
            break
        elif k == ord("r"):
            points.clear()
        elif k == ord("z") and len(points) >= 3:
            zone_norm = [[round(x / w, 3), round(y / h, 3)] for (x, y) in points]
            save_local({"strefa": zone_norm})
            print("Zapisano strefe do config.local.json:", zone_norm)

    cam.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
