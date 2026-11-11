# SmartGuard: Sentry Edition

System ochrony posesji: kamera wykrywa człowieka w chronionej strefie, zapisuje zdarzenie ze zdjęciem i wysyła
je na telefon przez Telegram, bez fałszywych alarmów od zwierząt i wiatru. Zdarzenia przegląda się w panelu WWW.

Rozszerzenie **Sentry**: wieżyczka Pan-Tilt na ESP32 celuje w intruza i strzela wodą, a domownika rozpoznaje po
breloku BLE w kieszeni.

Projekt zespołowy na przedmiot Inżynieria Oprogramowania (Informatyka, rok II). Python, YOLO, OpenCV, FastAPI, SQLite.

## Co robi system

| Przypadek użycia | Co się dzieje |
|---|---|
| UC-01 Wykrywanie intruza | człowiek w strefie → zdarzenie w bazie + zdjęcie z ramkami |
| UC-02 Alert | zdjęcie z godziną i strefą trafia na Telegram |
| UC-03 Przegląd zdarzeń | panel WWW: lista od najnowszego, duże zdjęcie |
| UC-04 Fałszywy alarm | oznaczenie zdarzenia + licznik |
| UC-07 Logowanie | panel tylko po zalogowaniu |

Co już działa, a czego jeszcze nie ma: [`docs/project/scope.md`](docs/project/scope.md).

## Jak to działa

```
kamera / MP4 → capture → detector (YOLO) → zone + rules (strefa, 3 klatki) → events (SQLite + JPG)
                                                                                 ├→ notifier → Telegram
                                                                                 └→ api → panel WWW
Sentry: rules (IFF) → state_machine → turret → ESP32 (serwa, pompka, laser)
```

Moduły są w pakiecie `smartguard/`; opis każdego jest w nagłówku jego pliku.

Dlaczego tak, a nie inaczej: [`docs/project/decisions.md`](docs/project/decisions.md).

## Uruchomienie

Wymagany Python 3.13. Sprzęt niepotrzebny: wieżyczka działa w trybie symulacji (SIM), wystarczy kamera.

Instalacja (raz):

```bat
py -3.13 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Uruchamianie (z aktywnym `.venv`, w folderze projektu):

```
python main.py              system na żywo (to samo daje przycisk ▶ w VS Code)
python main.py demo         bez kamery; „Koniec scenariusza.” = instalacja działa
python main.py calibrate    wyznaczanie strefy chronionej
python main.py preview      podgląd detekcji i strefy
python main.py --help       lista trybów
```

Sterowanie w oknie (klawisze) opisuje nagłówek pliku danego trybu w `smartguard/`.

## Konfiguracja

- `config.json`: wspólne ustawienia (progi, czasy, kąty).
- `config.local.json`: ustawienia twojego komputera, nadpisują wspólne (wzór: `config.local.example.json`).
- `.env`: sekrety, np. token bota Telegram (wzór: `.env.example`).

Dwa ostatnie są poza gitem.

## ESP32 i sprzęt Sentry

Firmware jest w `firmware/` (Arduino C++). Wgrywanie, połączenia i protokół:
[`docs/agents/hardware.md`](docs/agents/hardware.md).

⚠️ **Uwaga:** przed podłączeniem serw i pompki przeczytaj `docs/agents/hardware.md` § Złote zasady.

## Zespół i współpraca

| GitHub | Rola |
|---|---|
| `diablak04` | Product Owner (PO) |
| `AxmBro` | Scrum Master (SM) |
| *(do dodania)* | Developer (DEV) |

- Kto co robi, Kanban, Definicja Ukończenia: [`docs/project/team.md`](docs/project/team.md).
- Zmiany przez gałąź i Pull Request z 1 approval: [`docs/agents/git.md`](docs/agents/git.md).
- Konwencje kodu: [`docs/agents/code.md`](docs/agents/code.md). Jak pracujemy z asystentami AI: [`AGENTS.md`](AGENTS.md).
- Repo jest publiczne: bez danych osobowych i sekretów (`AGENTS.md` § Repo jest publiczne).

## Dokumentacja

Mapa wszystkich dokumentów: [`docs/README.md`](docs/README.md). Karta projektu i Scenariusze przypadków użycia
(zatwierdzone przez prowadzącą) są poza repo; ich streszczenie jest w `docs/project/scope.md`.
