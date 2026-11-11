"""Integracja na zywo (Faza 6) — caly system bez fizycznej wiezyczki.

Pelna petla: kamera -> YOLO -> strefa -> reguly -> maszyna stanow -> sterownik.
Sterownik w trybie SIM tylko loguje AIM/FIRE, wiec dziala bez sprzetu.
Celowanie: srodek korpusu celu mapowany na katy serw (visual servoing - podstawa).
IFF: przelacznik klawiszem 's' (docelowo z ESP32/BLE).

Okno — sterowanie:  's' = swoj/wrog   'm' = mute   'q' = wyjscie
Uruchom:  .venv\\Scripts\\python.exe integracja.py
"""
import json
import time
from pathlib import Path
import cv2

from capture import Camera
from detector import Detector
from turret_controller import TurretController
from main import SmartGuard, konfiguruj_logging
import zona

KROK_CO_S = 0.25  # maszyna stanow krokuje ~4x/s (nie co klatke) - czytelne tempo


def mapuj(v, a0, a1, b0, b1):
    return b0 + (v - a0) * (b1 - b0) / (a1 - a0)


def main():
    konfiguruj_logging()
    cfg = json.loads(Path("config.json").read_text(encoding="utf-8"))
    strefa, serw = cfg["strefa"], cfg["serwo"]

    cam = Camera(cfg.get("kamera_glowna", 0)).start()
    det = Detector(cfg["yolo_model"], cfg["yolo_prog_pewnosci"])
    turret = TurretController(port=cfg.get("esp32_port"), sim=True)  # SIM: bez sprzetu
    sg = SmartGuard(cfg, cooldown_ticks=8)

    iff_swoj = False
    ostatni_krok = 0.0
    time.sleep(1.0)
    print("'s'=swoj/wrog  'm'=mute  'q'=wyjscie")

    while True:
        frame = cam.read()
        if frame is None:
            continue
        h, w = frame.shape[:2]
        zona.rysuj_strefe(frame, strefa)

        cel_w_strefie, cel_box = False, None
        for box in det.wykryj_ludzi(frame):
            x1, y1, x2, y2, conf = box
            w_str = zona.punkt_w_strefie(zona.stopa_celu(box), strefa, w, h)
            kolor = (0, 0, 255) if w_str else (160, 160, 160)
            cv2.rectangle(frame, (x1, y1), (x2, y2), kolor, 2)
            if w_str:
                cel_w_strefie, cel_box = True, box

        # Maszyna stanow krokuje w stalym tempie (nie co klatke)
        if time.time() - ostatni_krok >= KROK_CO_S:
            akcja = sg.krok(cel_w_strefie, iff_swoj)
            ostatni_krok = time.time()
            if akcja and akcja[0] == "FIRE":
                turret.ogien(akcja[1])

        # Celowanie w srodek korpusu celu (gdy jest)
        if cel_box:
            cx = (cel_box[0] + cel_box[2]) // 2
            cy = (cel_box[1] + cel_box[3]) // 2
            pan = mapuj(cx, 0, w, serw["pan_min"], serw["pan_max"])
            tilt = mapuj(cy, 0, h, serw["tilt_max"], serw["tilt_min"])
            turret.celuj(pan, tilt)
            cv2.circle(frame, (cx, cy), 5, (0, 255, 255), -1)

        cv2.putText(frame, f"stan={sg.stan.name}  swoj={int(iff_swoj)}  mute={int(sg.muted)}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.imshow("SmartGuard - integracja (SIM)", frame)

        k = cv2.waitKey(1) & 0xFF
        if k == ord("q"):
            break
        elif k == ord("s"):
            iff_swoj = not iff_swoj
        elif k == ord("m"):
            sg.muted = not sg.muted

    cam.stop()
    cv2.destroyAllWindows()
    turret.zamknij()


if __name__ == "__main__":
    main()
