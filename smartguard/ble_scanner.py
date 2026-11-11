"""Skaner BLE (IFF) — identyfikacja 'swoj/wrog' po stalym MAC breloka + RSSI.

Brelok 'swoj' to urzadzenie BLE o znanym MAC (lista w config/.env: BLE_MAC_LIST).
Jesli jest widoczny i RSSI >= prog -> SWOJ (blokada ognia). W przeciwnym razie WROG.

Dziala z komputerowym Bluetoothem (bleak/WinRT). Brelok nie jest wymagany, zeby
przetestowac sam skaner — do testu wystarczy dowolne urzadzenie BLE w poblizu
(np. telefon z otwartym ekranem ustawien Bluetooth).
"""
import asyncio
from bleak import BleakScanner


async def scan(duration: float = 5.0) -> dict:
    """Zwraca {MAC: RSSI} wszystkich urzadzen BLE widocznych w ciagu 'duration' sekund."""
    found: dict = {}

    def callback(device, adv):
        found[device.address.upper()] = adv.rssi

    scanner = BleakScanner(detection_callback=callback)
    await scanner.start()
    await asyncio.sleep(duration)
    await scanner.stop()
    return found


async def is_friend_visible(macs, rssi_threshold: int = -75, duration: float = 3.0):
    """(True, mac, rssi) jesli ktorys brelok 'swoj' widoczny z RSSI >= prog; inaczej (False, None, None)."""
    devices = await scan(duration)
    for mac in macs:
        rssi = devices.get(mac.upper())
        if rssi is not None and rssi >= rssi_threshold:
            return True, mac.upper(), rssi
    return False, None, None


if __name__ == "__main__":
    print("Skanowanie BLE przez 5 s...")
    dev = asyncio.run(scan(5.0))
    if not dev:
        print("Brak urzadzen BLE (wlacz Bluetooth albo wlacz cos BLE w poblizu).")
    for mac, rssi in sorted(dev.items(), key=lambda x: x[1], reverse=True):
        print(f"  {mac}  RSSI={rssi} dBm")
    print(f"Razem widocznych: {len(dev)} urzadzen.")
