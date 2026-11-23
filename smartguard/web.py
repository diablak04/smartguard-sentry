"""SmartGuard — podglad na telefon/przegladarke (MJPEG przez HTTP).

Ta sama petla co `live` (kamera -> YOLO -> strefa -> maszyna stanow -> wiezyczka),
ale zamiast okna cv2 serwuje obraz na http://<IP-PC>:8000. Otworz ten adres na
telefonie (ten sam WiFi) — widzisz podglad i sterujesz (swoj/wrog, mute).
Celowanie i strzal dzialaja identycznie jak w `live`.
"""
import socket
import threading
import time

import cv2
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse

from smartguard import zone
from smartguard.capture import Camera
from smartguard.config import load_config
from smartguard.detector import Detector
from smartguard.state_machine import SmartGuard, setup_logging
from smartguard.turret import TurretController

PORT = 8000
HOME_DELAY = 1.5     # s bez celu zanim wiezyczka wroci na srodek (anty-oscylacja)
AIM_DEADZONE = 2     # stopnie - mniejsza zmiana nie rusza serwa (anty-drganie)
_latest = {"jpg": None}                       # najnowsza klatka JPEG (wspoldzielona)
_ctrl = {"iff_friend": False, "muted": False}  # sterowanie z przegladarki

STATE_COLORS = {
    "IDLE": (180, 180, 180), "DETECTED": (0, 200, 255), "CONFIRMING": (0, 200, 255),
    "FRIENDLY": (0, 220, 0), "FOE": (0, 0, 255), "ENGAGE": (0, 0, 255), "COOLDOWN": (0, 140, 255),
}

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SmartGuard</title>
<style>body{margin:0;background:#111;color:#eee;font-family:sans-serif;text-align:center}
img{width:100%;max-width:960px}button{font-size:1.2em;padding:14px 22px;margin:10px;border:0;border-radius:10px}
.a{background:#2d6cdf;color:#fff}.b{background:#d9534f;color:#fff}</style></head>
<body><h3>SmartGuard - podglad na zywo</h3>
<img src="/stream"><br>
<button class="a" onclick="fetch('/iff')">SWOJ / WROG</button>
<button class="b" onclick="fetch('/mute')">MUTE on/off</button>
</body></html>"""


def map_range(v, a0, a1, b0, b1):
    return b0 + (v - a0) * (b1 - b0) / (a1 - a0)


def box_area(box):
    return (box[2] - box[0]) * (box[3] - box[1])


def lan_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


def _loop(cfg) -> None:
    zone_norm, servo = cfg["zone"], cfg["servo"]
    step_every_s = cfg["aim"]["step_every_s"]
    ema = cfg["aim"]["smoothing"]

    cam = Camera(cfg["camera"]["main"]).start()
    det = Detector(cfg["yolo"]["model"], cfg["yolo"]["confidence"])
    turret = TurretController(port=cfg["esp32"]["port"], baud=cfg["esp32"]["baud"],
                              sim=cfg["esp32"].get("sim", False))
    sg = SmartGuard(cfg, cooldown_ticks=8)

    home = ((servo["pan_min"] + servo["pan_max"]) // 2, (servo["tilt_min"] + servo["tilt_max"]) // 2)
    aim = home
    sc = None
    last_step = 0.0
    last_seen = 0.0
    flash_until = 0.0
    time.sleep(1.0)

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
            sc = (cx, cy) if sc is None else (int((1 - ema) * sc[0] + ema * cx),
                                              int((1 - ema) * sc[1] + ema * cy))
            cv2.drawMarker(frame, sc, (0, 255, 255), cv2.MARKER_CROSS, 26, 2)
        else:
            sc = None

        if time.time() - last_step >= step_every_s:
            sg.muted = _ctrl["muted"]
            action = sg.step(target_in_zone, _ctrl["iff_friend"])
            last_step = time.time()
            if sc is not None:
                new_aim = (int(map_range(sc[0], 0, w, servo["pan_min"], servo["pan_max"])),
                           int(map_range(sc[1], 0, h, servo["tilt_max"], servo["tilt_min"])))
                if abs(new_aim[0] - aim[0]) > AIM_DEADZONE or abs(new_aim[1] - aim[1]) > AIM_DEADZONE:
                    aim = new_aim          # ruszaj tylko przy wyrazniejszej zmianie (martwa strefa)
                    turret.aim(*aim)
                last_seen = time.time()
            elif time.time() - last_seen > HOME_DELAY and aim != home:
                aim = home                 # brak celu dluzej niz HOME_DELAY -> powrot na srodek
                turret.aim(*aim)
            if action and action[0] == "FIRE":
                turret.fire(action[1])
                flash_until = time.time() + 0.8

        state_name = sg.state.name
        cv2.rectangle(frame, (0, 0), (w, 70), (0, 0, 0), -1)
        cv2.putText(frame, f"STAN: {state_name}", (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    STATE_COLORS.get(state_name, (255, 255, 255)), 2)
        cv2.putText(frame, f"IFF: {'SWOJ' if _ctrl['iff_friend'] else 'WROG'}   "
                           f"MUTE: {'TAK' if _ctrl['muted'] else 'nie'}   AIM: {aim[0]},{aim[1]}",
                    (10, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
        if time.time() < flash_until:
            cv2.putText(frame, f"STRZAL! {sg.fire_ms}ms", (w // 2 - 170, h // 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 4)

        ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        if ok:
            _latest["jpg"] = buf.tobytes()


def _mjpeg():
    while True:
        jpg = _latest["jpg"]
        if jpg is not None:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpg + b"\r\n"
        time.sleep(0.05)


def run() -> None:
    setup_logging()
    cfg = load_config()
    threading.Thread(target=_loop, args=(cfg,), daemon=True).start()

    app = FastAPI()

    @app.get("/")
    def index():
        return HTMLResponse(PAGE)

    @app.get("/stream")
    def stream():
        return StreamingResponse(_mjpeg(), media_type="multipart/x-mixed-replace; boundary=frame")

    @app.get("/iff")
    def iff():
        _ctrl["iff_friend"] = not _ctrl["iff_friend"]
        return {"iff_friend": _ctrl["iff_friend"]}

    @app.get("/mute")
    def mute():
        _ctrl["muted"] = not _ctrl["muted"]
        return {"muted": _ctrl["muted"]}

    ip = lan_ip()
    print(f"\n>>> Otworz na telefonie (ten sam WiFi):  http://{ip}:{PORT}\n")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")
