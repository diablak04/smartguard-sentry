# Konwencje kodu

> **Kiedy czytać:** przed każdą zmianą w `*.py`. Język nazw, struktura folderów, ścieżki i pliki generowane, konfiguracja, logi.
> Obowiązuje ludzi i asystentów AI.

## Język

| Co | Język | Przykład |
|---|---|---|
| pliki i foldery (kod i `docs/`), moduły | angielski | `zone.py`, `state_machine.py`, `docs/project/scope.md` |
| klasy, funkcje, zmienne, stałe | angielski | `point_in_zone()`, `FrameConfirmation`, `FIRE_MAX_MS` |
| klucze `config.json`, tabele i kolumny SQLite, endpointy API | angielski | `"fire_ms"`, `events.created_at`, `GET /api/events` |
| gałęzie, typ i zakres commita | angielski | `feat/telegram-alert`, `feat(events): …` |
| opis commita, PR, issue | polski | `feat(events): zapis zdarzenia do SQLite` |
| komentarze, docstringi, dokumentacja | polski, z polskimi znakami | `"""Zwraca punkt stóp celu."""` |
| teksty dla użytkownika: panel, Telegram, logi | polski | `log.info("Człowiek w strefie")` |

Nazwy według PEP 8: `snake_case` (moduły, funkcje, zmienne), `PascalCase` (klasy), `UPPER_CASE` (stałe).
Gdy liczba ma jednostkę, jednostka jest w nazwie: `fire_ms`, `cooldown_s`, `rssi_dbm`.

## Struktura

```
smartguard-sentry/
├─ main.py                 jedyne wejście: python main.py [live | demo | calibrate | preview]
├─ smartguard/             kod aplikacji (pakiet), w tym tryby live, demo, calibrate, preview
├─ tests/                  testy pytest
├─ firmware/               szkice ESP32 (nazwa folderu = nazwa pliku .ino)
├─ docs/                   dokumentacja (mapa: docs/README.md)
├─ models/  logs/  data/   pliki generowane, poza gitem
├─ notes/, AGENTS.local.md prywatne notatki każdej osoby, poza gitem (podział opisuje AGENTS.md)
└─ config.json, config.local.example.json, requirements.txt, .env.example, docker-compose.yml
```

- W korzeniu jest jeden skrypt, `main.py`, który tylko wybiera tryb; cała logika jest w `smartguard/`.
  Nowy tryb = moduł w `smartguard/` z funkcją `run()` + wpis w `MODES` w `main.py` (`docs/project/decisions.md` § D-04 (jedno wejście main.py)).
  Plików z `smartguard/` nie uruchamia się bezpośrednio. Nowych dokumentów nie kładziemy w korzeniu, tylko w `docs/`.
- Importy absolutne od nazwy pakietu: `from smartguard.config import load_config`.
- Nie używamy `src/`, `pyproject.toml` ani `pip install -e .`: uruchamiamy z folderu projektu, pakietu nie publikujemy.
  Skrypt uruchomiony z wnętrza pakietu albo z `scripts/` nie widzi pakietu (`ModuleNotFoundError`), stąd jedno wejście w korzeniu.
- Testy uruchamiasz z folderu projektu przez `python -m pytest`. Samo `pytest` nie znajdzie pakietu.

## Pliki generowane i ścieżki

| Folder | Co tam trafia | Kto tworzy |
|---|---|---|
| `models/` | `yolo11n.pt` | ultralytics, pobiera go przy pierwszym uruchomieniu |
| `logs/` | `smartguard.log` (z rotacją) | logging |
| `data/` | `smartguard.db`, `events/` (zdjęcia zdarzeń), `videos/` (nagrania testowe) | `smartguard/events.py` (do napisania), ty |

- Wszystkie trzy foldery są w `.gitignore`. W `data/` są zdjęcia ludzi (RODO), więc nigdy nie trafia do repo.
- Ścieżki są liczone od folderu projektu (stała `ROOT` w `smartguard/config.py`), nigdy od bieżącego katalogu
  i nigdy bezwzględnie (`C:\...`). Żaden kod nie zapisuje plików w korzeniu repo.
- Pliki tekstowe otwieraj zawsze z `encoding="utf-8"`, bo na Windows domyślne jest cp1250.

## Konfiguracja

- Wartości, które się stroi (progi, czasy, kąty, porty), trzymamy w `config.json`, nie w kodzie. Klucze są po angielsku
  i pogrupowane, np. `"camera": {"main": 0, "fpv": 1}`.
- `config.json` jest wspólny. `config.local.json` jest per komputer, poza gitem, i nadpisuje wspólny.
- Odczyt przez `load_config()`. Ustawienia konkretnego komputera zapisuje `save_local()` do `config.local.json`.
  Kod nigdy nie nadpisuje `config.json`.
- Port ESP32 = `"auto"` (wykrywanie po USB w module wieżyczki).
- Sekrety (token bota, hasło panelu) trzymamy tylko w `.env`.

## Logi i zależności

- Diagnostyka przez `logging.getLogger(__name__)`, nie przez `print`.
- Nowa biblioteka → `requirements.txt` z komentarzem, do czego służy.
