"""SmartGuard: jedno wejście do programu, tryb wybierasz argumentem.

  python main.py              system na żywo (kamera, detekcja, strefa, wieżyczka w trybie SIM)
  python main.py demo         scenariusz bez kamery; „Koniec scenariusza.” = instalacja działa
  python main.py calibrate    wyznaczanie strefy chronionej
  python main.py preview      podgląd detekcji i strefy

Logika trybów jest w pakiecie smartguard/ (live, demo, calibrate, preview); sterowanie
każdego trybu opisuje nagłówek jego pliku.
"""
import argparse
import importlib

MODES = {
    "live": "system na zywo (domyslnie)",
    "demo": "scenariusz bez kamery",
    "calibrate": "wyznaczanie strefy chronionej",
    "preview": "podglad detekcji i strefy",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="SmartGuard: wybierz tryb uruchomienia.")
    modes = parser.add_subparsers(dest="mode", metavar="tryb")
    for name, help_text in MODES.items():
        modes.add_parser(name, help=help_text)
    mode = parser.parse_args().mode or "live"
    # Import dopiero po wyborze, żeby np. demo nie ładowało YOLO ani kamery.
    importlib.import_module(f"smartguard.{mode}").run()


if __name__ == "__main__":
    main()
