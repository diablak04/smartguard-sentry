"""Sterownik wiezyczki — wysyla komendy do ESP32 po UART (protokół: docs/agents/hardware.md § Protokół PC).

Tryb SIM (bez sprzetu lub gdy brak portu): komendy sa tylko logowane — dzieki temu
caly system mozna uruchomic i przetestowac bez fizycznej wiezyczki.

Protokol PC->ESP32: AIM:<pan>,<tilt> | FIRE:<ms> | LASER:0/1 | BUZZ | SCAN:ON/OFF

Port: "auto" (domyslnie) = sam znajdz ESP32 po ukladzie USB-UART; albo konkretny, np. "COM5".
"""
import logging

try:
    import serial  # pyserial
    from serial.tools import list_ports
except ImportError:
    serial = list_ports = None

# Uklady USB<->UART spotykane na plytkach ESP32 (USB Vendor ID)
ESP32_USB_VIDS = {
    0x10C4: "CP210x",
    0x1A86: "CH340/CH9102",
    0x0403: "FTDI",
    0x303A: "Espressif (natywne USB)",
}


def find_esp32_port(ports=None) -> str | None:
    """Zwraca nazwe portu pierwszego urzadzenia wygladajacego na ESP32 albo None."""
    if ports is None:
        if list_ports is None:
            return None
        ports = list_ports.comports()
    candidates = sorted(p.device for p in ports if p.vid in ESP32_USB_VIDS)
    return candidates[0] if candidates else None


class TurretController:
    def __init__(self, port: str | None = "auto", baud: int = 115200, sim: bool = False):
        self.log = logging.getLogger("turret")
        if not sim and port == "auto":
            port = find_esp32_port()
            if port:
                self.log.info("Wiezyczka: wykryto ESP32 na %s", port)
            else:
                self.log.warning("Wiezyczka: nie znaleziono ESP32 na USB")
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

    def _send(self, cmd: str) -> None:
        if self.sim:
            # AIM leci bardzo czesto -> DEBUG (nie zasmieca konsoli); reszta INFO
            (self.log.debug if cmd.startswith("AIM") else self.log.info)("[SIM] -> %s", cmd)
        else:
            self.ser.write((cmd + "\n").encode())

    def aim(self, pan: float, tilt: float) -> None:
        self._send(f"AIM:{int(pan)},{int(tilt)}")

    def fire(self, ms: int) -> None:
        self._send(f"FIRE:{int(ms)}")

    def laser(self, on: bool) -> None:
        self._send(f"LASER:{1 if on else 0}")

    def buzz(self) -> None:
        self._send("BUZZ")

    def close(self) -> None:
        if self.ser:
            self.ser.close()
