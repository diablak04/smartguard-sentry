"""SmartGuard na zywo — caly system, wiezyczka w trybie SIM (bez fizycznego sprzetu).

Pelna petla: kamera -> YOLO -> strefa -> reguly -> maszyna stanow -> sterownik.
Sterownik w trybie SIM tylko loguje (AIM na DEBUG, wiec konsola jest cicha),
dzieki czemu dziala bez sprzetu. Celowanie: srodek korpusu GLOWNEGO celu
(najwiekszy w strefie), wygladzony (EMA), zeby celownik nie skakal.

UWAGA: strefa jest w widoku kamery. Najpierw skalibruj ja pod SWOJ widok
(calibrate_zone.py), potem uruchom ten plik.

Okno — sterowanie:  's' = swoj/wrog   'm' = mute   'q' = wyjscie
"""
import time
import cv2

from smartguard import zone
from smartguard.capture import Camera
from smartguard.config import load_config
from smartguard.detector import Detector
from smartguard.state_machine import SmartGuard, setup_logging
from smartguard.turret import TurretController

STEP_EVERY_S = 0.25  # maszyna stanow + celowanie krokuja ~4x/s
EMA = 0.4            # wygladzanie celownika (0=zamrozony, 1=bez wygladzania)


def map_range(v, a0, a1, b0, b1):
    return b0 + (v - a0) * (b1 - b0) / (a1 - a0)


def box_area(box):
    return (box[2] - box[0]) * (box[3] - box[1])


STATE_COLORS = {
    "IDLE": (180, 180, 180), "DETECTED": (0, 200, 255), "CONFIRMING": (0, 200, 255),
    "FRIENDLY": (0, 220, 0), "FOE": (0, 0, 255), "ENGAGE": (0, 0, 255), "COOLDOWN": (0, 140, 255),
}


def main():
    setup_logging()
    cfg = load_config()
    zone_norm, servo = cfg["strefa"], cfg["serwo"]

    cam = Camera(cfg.get("kamera_glowna", 0)).start()
    det = Detector(cfg["yolo_model"], cfg["yolo_prog_pewnosci"])
    turret = TurretController(port=cfg.get("esp32_port"), sim=True)  # SIM: bez sprzetu
    sg = SmartGuard(cfg, cooldown_ticks=8)

    iff_friend = False
    last_step = 0.0
    aim = (90, 40)
    sc = None          # wygladzony srodek celu (smoothed center)
    flash_until = 0.0
    time.sleep(1.0)
    print("Okno: 's'=swoj/wrog  'm'=mute  'q'=wyjscie  (konsola: stany + STRZAL)")

    while True:
        frame = cam.read()
        if frame is None:
            continue
        h, w = frame.shape[:2]
        zone.draw_zone(frame, zone_norm)

        detections = det.detect_people(frame)
        in_zone = [b for b in detections
                   if zone.point_in_zone(zone.target_foot(b), zone_norm, w, h)]
        main_target = max(in_zone, key=box_area) if in_zone else None
        target_in_zone = main_target is not None

        # Rysuj: pozostale cienko-szaro, glowny cel grubo-czerwono
        for b in detections:
            if b is main_target:
                continue
            cv2.rectangle(frame, (b[0], b[1]), (b[2], b[3]), (120, 120, 120), 1)
        if main_target:
            x1, y1, x2, y2, conf = main_target
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
        if time.time() - last_step >= STEP_EVERY_S:
            action = sg.step(target_in_zone, iff_friend)
            last_step = time.time()
            if sc is not None:
                aim = (int(map_range(sc[0], 0, w, servo["pan_min"], servo["pan_max"])),
                       int(map_range(sc[1], 0, h, servo["tilt_max"], servo["tilt_min"])))
                turret.aim(*aim)
            if action and action[0] == "FIRE":
                turret.fire(action[1])
                flash_until = time.time() + 0.8

        # --- HUD ---
        state_name = sg.state.name
        cv2.rectangle(frame, (0, 0), (w, 70), (0, 0, 0), -1)
        cv2.putText(frame, f"STAN: {state_name}", (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    STATE_COLORS.get(state_name, (255, 255, 255)), 2)
        cv2.putText(frame, f"IFF: {'SWOJ' if iff_friend else 'WROG'}   MUTE: {'TAK' if sg.muted else 'nie'}   AIM: {aim[0]},{aim[1]}",
                    (10, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
        cv2.putText(frame, "s=swoj/wrog  m=mute  q=wyjscie", (10, h - 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        if time.time() < flash_until:
            cv2.putText(frame, "STRZAL! 200ms", (w // 2 - 170, h // 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 4)

        cv2.imshow("SmartGuard - na zywo (SIM)", frame)
        k = cv2.waitKey(1) & 0xFF
        if k == ord("q"):
            break
        elif k == ord("s"):
            iff_friend = not iff_friend
        elif k == ord("m"):
            sg.muted = not sg.muted

    cam.stop()
    cv2.destroyAllWindows()
    turret.close()


if __name__ == "__main__":
    main()
