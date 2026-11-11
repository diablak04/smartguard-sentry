"""Wczytywanie konfiguracji: wspolny config.json + osobisty config.local.json.

config.json        - w repo, wspolny dla zespolu (progi, katy, czasy...).
config.local.json  - NIE w repo (.gitignore), ustawienia TEGO komputera
                     (kamera, port ESP32, strefa z kalibracji). Nadpisuje config.json.

Dzieki temu 3 osoby nie nadpisuja sobie nawzajem ustawien przy git pull.
Sciezki liczone od folderu projektu, wiec skrypty dzialaja z dowolnego miejsca.
"""
import json
from pathlib import Path

KATALOG = Path(__file__).resolve().parent
WSPOLNY = KATALOG / "config.json"
LOKALNY = KATALOG / "config.local.json"


def _czytaj(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"Blad w pliku {path.name} (linia {e.lineno}): {e.msg}") from None


def _scal(baza: dict, nad: dict) -> dict:
    """Scala slowniki rekurencyjnie; listy i wartosci proste sa zastepowane."""
    wynik = dict(baza)
    for k, v in nad.items():
        if isinstance(v, dict) and isinstance(wynik.get(k), dict):
            wynik[k] = _scal(wynik[k], v)
        else:
            wynik[k] = v
    return wynik


def wczytaj_config(wspolny: Path = WSPOLNY, lokalny: Path = LOKALNY) -> dict:
    cfg = _czytaj(wspolny)
    if lokalny.exists():
        cfg = _scal(cfg, _czytaj(lokalny))
    return cfg


def zapisz_lokalnie(zmiany: dict, lokalny: Path = LOKALNY) -> None:
    """Dopisuje zmiany do config.local.json (zachowuje pozostale lokalne klucze)."""
    obecne = _czytaj(lokalny) if lokalny.exists() else {}
    lokalny.write_text(json.dumps(_scal(obecne, zmiany), indent=2, ensure_ascii=False),
                       encoding="utf-8")
