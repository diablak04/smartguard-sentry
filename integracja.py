"""Integracja na zywo (Faza 6) — caly system bez fizycznej wiezyczki.

Pelna petla: kamera -> YOLO -> strefa -> reguly -> maszyna stanow -> sterownik.
Sterownik w trybie SIM tylko loguje (AIM na DEBUG, wiec konsola jest cicha),
dzieki czemu dziala bez sprzetu. Celowanie: srodek korpusu GLOWNEGO celu
(najwiekszy w strefie), wygladzony (EMA), zeby celownik nie skakal.

UWAGA: strefa jest w widoku kamery. Najpierw skalibruj ja pod SWOJ widok
(kalibracja_strefy.py), potem uruchom ten plik.

Okno — sterowanie:  's' = swoj/wrog   'm' = mute   'q' = wyjscie
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

KROK_CO_S = 0.25  # maszyna stanow + celowanie krokuja ~4x/s
EMA = 0.4         # wygladzanie celownika (0=zamrozony, 1=bez wygladzania)


def mapuj(v, a0, a1, b0, b1):
    return b0 + (v - a0) * (b1 - b0) / (a1 - a0)


def pole(box):
    return (box[2] - box[0]) * (box[3] - box[1])


KOLOR_STANU = {
    "IDLE": (180, 180, 180), "DETECTED": (0, 200, 255), "CONFIRMING": (0, 200, 255),
    "FRIENDLY": (0, 220, 0), "FOE": (0, 0, 255), "ENGAGE": (0, 0, 255), "COOLDOWN": (0, 140, 255),
}


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
    aim = (90, 40)
    sc = None          # wygladzony srodek celu (smoothed center)
    flash_do = 0.0
    time.sleep(1.0)
    print("Okno: 's'=swoj/wrog  'm'=mute  'q'=wyjscie  (konsola: stany + STRZAL)")

    while True:
        frame = cam.read()
        if frame is None:
            continue
        h, w = frame.shape[:2]
        zona.rysuj_strefe(frame, strefa)

        detekcje = det.wykryj_ludzi(frame)
        w_strefie = [b for b in detekcje
                     if zona.punkt_w_strefie(zona.stopa_celu(b), strefa, w, h)]
        glowny = max(w_strefie, key=pole) if w_strefie else None
        cel_w_strefie = glowny is not None

        # Rysuj: pozostale cienko-szaro, glowny cel grubo-czerwono
        for b in detekcje:
            if b is glowny:
                continue
            cv2.rectangle(frame, (b[0], b[1]), (b[2], b[3]), (120, 120, 120), 1)
        if glowny:
            x1, y1, x2, y2, conf = glowny
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, f"CEL {conf:.2f}", (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            sc = (cx, cy) if sc is None else (int((1 - EMA) * sc[0] + EMA * cx),
                                              int((1 - EMA) * sc[1] + EMA * cy))
            cv2.drawMarker(frame, sc, (0, 255, 255), cv2.MARKER_CROSS, 26, 2)
        else:
            sc = None

        # Maszyna stanow + celowanie w stalym tempie
        if time.time() - ostatni_krok >= KROK_CO_S:
            akcja = sg.krok(cel_w_strefie, iff_swoj)
            ostatni_krok = time.time()
            if sc is not None:
                aim = (int(mapuj(sc[0], 0, w, serw["pan_min"], serw["pan_max"])),
                       int(mapuj(sc[1], 0, h, serw["tilt_max"], serw["tilt_min"])))
                turret.celuj(*aim)
            if akcja and akcja[0] == "FIRE":
                turret.ogien(akcja[1])
                flash_do = time.time() + 0.8

        # --- HUD ---
        st = sg.stan.name
        cv2.rectangle(frame, (0, 0), (w, 70), (0, 0, 0), -1)
        cv2.putText(frame, f"STAN: {st}", (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    KOLOR_STANU.get(st, (255, 255, 255)), 2)
        cv2.putText(frame, f"IFF: {'SWOJ' if iff_swoj else 'WROG'}   MUTE: {'TAK' if sg.muted else 'nie'}   AIM: {aim[0]},{aim[1]}",
                    (10, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
        cv2.putText(frame, "s=swoj/wrog  m=mute  q=wyjscie", (10, h - 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        if time.time() < flash_do:
            cv2.putText(frame, "STRZAL! 200ms", (w // 2 - 170, h // 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 4)

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
