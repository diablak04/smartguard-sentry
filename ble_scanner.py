"""Skaner BLE (IFF) — identyfikacja 'swoj/wrog' po stalym MAC breloka + RSSI.

Brelok 'swoj' to urzadzenie BLE o znanym MAC (lista w config/.env: BLE_MAC_LIST).
Jesli jest widoczny i RSSI >= prog -> SWOJ (blokada ognia). W przeciwnym razie WROG.

Dziala z komputerowym Bluetoothem (bleak/WinRT). Brelok nie jest wymagany, zeby
przetestowac sam skaner — do testu wystarczy dowolne urzadzenie BLE w poblizu
(np. telefon z otwartym ekranem ustawien Bluetooth).
"""
import asyncio
from bleak import BleakScanner


async def skanuj(czas: float = 5.0) -> dict:
    """Zwraca {MAC: RSSI} wszystkich urzadzen BLE widocznych w ciagu 'czas' sekund."""
    znalezione: dict = {}

    def callback(device, adv):
        znalezione[device.address.upper()] = adv.rssi

    scanner = BleakScanner(detection_callback=callback)
    await scanner.start()
    await asyncio.sleep(czas)
    await scanner.stop()
    return znalezione


async def czy_swoj(mac_listy, rssi_prog: int = -75, czas: float = 3.0):
    """(True, mac, rssi) jesli ktorys brelok 'swoj' widoczny z RSSI >= prog; inaczej (False, None, None)."""
    urzadzenia = await skanuj(czas)
    for mac in mac_listy:
        rssi = urzadzenia.get(mac.upper())
        if rssi is not None and rssi >= rssi_prog:
            return True, mac.upper(), rssi
    return False, None, None


if __name__ == "__main__":
    print("Skanowanie BLE przez 5 s...")
    dev = asyncio.run(skanuj(5.0))
    if not dev:
        print("Brak urzadzen BLE (wlacz Bluetooth albo wlacz cos BLE w poblizu).")
    for mac, rssi in sorted(dev.items(), key=lambda x: x[1], reverse=True):
        print(f"  {mac}  RSSI={rssi} dBm")
    print(f"Razem widocznych: {len(dev)} urzadzen.")
