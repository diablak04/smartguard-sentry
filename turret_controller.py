"""Sterownik wiezyczki — wysyla komendy do ESP32 po UART (protokol z CLAUDE.md).

Tryb SIM (bez sprzetu lub gdy brak portu): komendy sa tylko logowane — dzieki temu
caly system mozna uruchomic i przetestowac bez fizycznej wiezyczki.

Protokol PC->ESP32: AIM:<pan>,<tilt> | FIRE:<ms> | LASER:0/1 | BUZZ | SCAN:ON/OFF
"""
import logging

try:
    import serial  # pyserial
except ImportError:
    serial = None


class TurretController:
    def __init__(self, port: str | None = None, baud: int = 115200, sim: bool = False):
        self.log = logging.getLogger("turret")
        self.sim = sim or serial is None or not port
        self.ser = None
        if not self.sim:
            try:
                self.ser = serial.Serial(port, baud, timeout=0.2)
                self.log.info("Wiezyczka: polaczono z %s", port)
            except Exception as e:
                self.log.warning("Brak portu %s (%s) -> tryb SIM", port, e)
                self.sim = True
        if self.sim:
            self.log.info("Wiezyczka: tryb SIM (komendy tylko logowane)")

    def _wyslij(self, cmd: str) -> None:
        if self.sim:
            self.log.info("[SIM] -> %s", cmd)
        else:
            self.ser.write((cmd + "\n").encode())

    def celuj(self, pan: float, tilt: float) -> None:
        self._wyslij(f"AIM:{int(pan)},{int(tilt)}")

    def ogien(self, ms: int) -> None:
        self._wyslij(f"FIRE:{int(ms)}")

    def laser(self, wl: bool) -> None:
        self._wyslij(f"LASER:{1 if wl else 0}")

    def buzzer(self) -> None:
        self._wyslij("BUZZ")

    def zamknij(self) -> None:
        if self.ser:
            self.ser.close()
