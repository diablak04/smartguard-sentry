"""Wczytywanie konfiguracji: wspolny config.json + osobisty config.local.json.

config.json        - w repo, wspolny dla zespolu (progi, katy, czasy...).
config.local.json  - NIE w repo (.gitignore), ustawienia TEGO komputera
                     (kamera, port ESP32, strefa z kalibracji). Nadpisuje config.json.

Dzieki temu 3 osoby nie nadpisuja sobie nawzajem ustawien przy git pull.
Sciezki liczone od folderu projektu (ROOT), wiec skrypty dzialaja z dowolnego miejsca.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED_CONFIG = ROOT / "config.json"
LOCAL_CONFIG = ROOT / "config.local.json"
LOGS_DIR = ROOT / "logs"


def project_path(path: str) -> Path:
    """Sciezka z configu (np. "models/yolo11n.pt") liczona od folderu projektu, nie od biezacego katalogu."""
    p = Path(path)
    return p if p.is_absolute() else ROOT / p


def _read(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"Blad w pliku {path.name} (linia {e.lineno}): {e.msg}") from None


def _merge(base: dict, override: dict) -> dict:
    """Scala slowniki rekurencyjnie; listy i wartosci proste sa zastepowane."""
    result = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(result.get(k), dict):
            result[k] = _merge(result[k], v)
        else:
            result[k] = v
    return result


def load_config(shared: Path = SHARED_CONFIG, local: Path = LOCAL_CONFIG) -> dict:
    cfg = _read(shared)
    if local.exists():
        cfg = _merge(cfg, _read(local))
    return cfg


def save_local(changes: dict, local: Path = LOCAL_CONFIG) -> None:
    """Dopisuje zmiany do config.local.json (zachowuje pozostale lokalne klucze)."""
    current = _read(local) if local.exists() else {}
    local.write_text(json.dumps(_merge(current, changes), indent=2, ensure_ascii=False),
                     encoding="utf-8")
