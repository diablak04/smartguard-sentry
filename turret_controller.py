"""Sterowanie wieżyczką: przeliczanie pozycji celu na kąty serw (Visual Servoing).

Komunikacja z ESP32 przez UART (pyserial): AIM, FIRE, LASER, SCAN.

TODO (Dzień 6): piksel_na_katy(cx, cy, w, h) wg kalibracji z config.json.
TODO (Dzień 6): śledzenie ruchomego celu (korekta min. 5 Hz).
"""
