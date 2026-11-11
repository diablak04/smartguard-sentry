# SmartGuard: Sentry Edition

Projekt z **Inżynierii Oprogramowania** (Informatyka, rok II). Termin oddania: **24.01.2027**.

**Cel produktu** (z karty): właściciel posesji dostaje na telefon zdjęcie, gdy w chronionej strefie pojawi się
człowiek, bez fałszywych alarmów od zwierząt i wiatru.

**Sentry Edition** (rozszerzenie): wieżyczka Pan-Tilt strzela wodą we wroga, a swojego rozpoznaje po breloku BLE.

| GitHub | Rola | Obszar |
|---|---|---|
| `diablak04` | Product Owner | wykrywanie + wieżyczka (sprzęt, ESP32) |
| `AxmBro` | Scrum Master | zapis zdarzeń, panel WWW, spięcie |
| *(do dodania)* | Developer | alert na Telegram, testy |

## Zakres

Budujemy przypadki użycia ze **Scenariuszy** zatwierdzonych przez prowadzącą:

| UC | Co robi system |
|---|---|
| UC-01 | wykrywa człowieka w strefie (YOLO, punkt stóp, 3 klatki) i zapisuje zdarzenie ze zdjęciem |
| UC-02 | wysyła zdjęcie na Telegram (max 1 alert / 60 s na strefę) |
| UC-03 | panel WWW: lista zdarzeń, duże zdjęcie |
| UC-04 | oznaczenie fałszywego alarmu + licznik |
| UC-07 | logowanie do panelu |

Stan każdego punktu: `docs/zakres.md`. Kto co robi: `docs/podzial_pracy.md`.

## Jak to działa

```
kamera / MP4 → capture → detector (YOLO) → zona + rules (strefa, 3 klatki) → events (SQLite + JPG)
                                                                                 ├→ notifier → Telegram
                                                                                 └→ api → panel WWW
Sentry: rules (IFF) → main (maszyna stanów) → turret_controller → ESP32 (serwa, pompka, laser)
```

| Plik | Rola | Stan |
|---|---|---|
| `capture.py` | odczyt kamery w osobnym wątku | ✅ |
| `detector.py` | YOLO `yolo11n`, tylko ludzie | ✅ |
| `zona.py`, `kalibracja_strefy.py` | strefa chroniona + jej wyznaczanie | ✅ |
| `rules.py` | potwierdzanie na 3 klatkach, swój/wróg | ✅ |
| `events.py` | zapis zdarzeń + zdjęć | ❌ |
| `notifier.py` | alert na Telegram | ❌ |
| `api.py` | panel WWW | ❌ |
| `main.py` | maszyna stanów + spięcie | 🟡 |
| `config.py` | wczytuje `config.json` + `config.local.json` | ✅ |
| `turret_controller.py` | komendy do ESP32, tryb SIM, auto-port | ✅ |
| `integracja.py` | cały system na żywo (wieżyczka w trybie SIM) | ✅ |
| `firmware/` | ESP32: `smartguard_esp32` (główny), `ble_test`, `serwo_test` | 🟡 |

## Szybki start (Windows + VS Code)

Sprzęt niepotrzebny: wieżyczka działa w trybie SIM, wystarczy kamerka.

1. Zainstaluj [Python 3.13](https://www.python.org/downloads/windows/) (zaznacz **„Add python.exe to PATH”**)
   i [VS Code](https://code.visualstudio.com/) z rozszerzeniem **Python**.
2. `git clone https://github.com/diablak04/smartguard-sentry` → VS Code: *File → Open Folder*.
3. W terminalu VS Code (~1,2 GB, ok. 5 min):
   ```bat
   py -3.13 -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
4. `Ctrl+Shift+P` → *Python: Select Interpreter* → **`.venv`**.
5. Uruchamiaj przyciskiem **▶ Run Python File**:

| Plik | Co robi | Klawisze |
|---|---|---|
| `main.py` | demo bez kamery; `Koniec scenariusza.` = instalacja OK | — |
| `detekcja_test.py` | wykrywanie ludzi + strefa | `q` wyjście |
| `kalibracja_strefy.py` | wyznaczanie strefy | klik = punkt, `z` zapisz, `r` reset, `q` wyjście |
| `integracja.py` | cały system na żywo | `s` swój/wróg, `m` wycisz, `q` wyjście |

**Gdy nie działa:**
- `No module named 'cv2'` → zrób krok 4. Nie używaj „Run Code” (Code Runner), tylko **Run Python File**.
- `'py' is not recognized` → zainstaluj Pythona ponownie z „Add python.exe to PATH”.
- Czarne okno / zła kamera → `"kamera_glowna": 1` w `config.local.json`.
- Kamera zajęta → zamknij Teams / Zoom / Discord.

## Konfiguracja

| Plik | W gicie | Do czego |
|---|---|---|
| `config.json` | tak | wspólne ustawienia (progi, czasy, kąty) |
| `config.local.json` | nie | ustawienia Twojego komputera; nadpisuje `config.json` |
| `.env` | nie | sekrety: token bota, id czatu, login panelu |

`config.local.json` tworzysz tylko, gdy coś nie działa: `copy config.local.example.json config.local.json`.
Najczęściej: `"kamera_glowna"` (0 = wbudowana, 1 = USB), `"esp32_port"` (zostaw `"auto"`).
Strefę dopisuje tam `kalibracja_strefy.py`. `.env`: `copy .env.example .env` i uzupełnij.

## Praca w zespole

**Narzędzia** (karta § 6.1, z jedną zmianą):

| Do czego | Narzędzie |
|---|---|
| kod, przegląd zmian | GitHub — to repo |
| zadania (w karcie: Trello) | [Kanban na GitHub Projects](https://github.com/users/diablak04/projects/1) |
| bieżąca komunikacja, Daily | Discord |
| diagramy UML i ERD | draw.io, DataModeler |

**Kanban:** kolumny Backlog → In Progress → Testing → Done.
- Jedna karta = jedna rzecz z `docs/zakres.md`, w tytule numer wymagania, np. `[5] Alert na Telegram`.
- Kartę zakładaj jako **issue** w repo i dodaj do projektu.
- PR z `Closes #<nr issue>` zamyka issue po merge; karta sama przechodzi do Done, jeśli w projekcie jest włączony workflow „Item closed”.

**Git:**
1. `git checkout main` → `git pull`
2. `git checkout -b feat/krotki-opis` (albo `fix/`, `docs/`, `chore/`)
3. commity `typ(zakres): opis po polsku`, np. `feat(events): zapis zdarzenia do SQLite`
4. `git push -u origin feat/krotki-opis` → Pull Request → **1 approval** drugiej osoby → merge

**Definicja Ukończenia** (karta § 12.1). Karta idzie do Done, gdy:
- [ ] kod jest w `main` przez PR zatwierdzony przez drugą osobę,
- [ ] działa w trybie demo na nagraniu testowym,
- [ ] wynik sprawdzenia jest w komentarzu karty,
- [ ] druga osoba uruchomiła zmianę u siebie,
- [ ] odstępstwo od karty jest wpisane w `docs/zakres.md`.

## ESP32 (tylko PO)

1. [Arduino IDE 2](https://www.arduino.cc/en/software) → *Boards Manager*: **esp32** (Espressif) → *Library Manager*: **ESP32Servo**.
2. Kabel USB **z danymi**. Brak portu COM → sterownik: **CP2102** → Silicon Labs CP210x, **CH340** → WCH CH340.
3. Szkic z `firmware/`, *Board: ESP32 Dev Module*, **Upload** (wisi na `Connecting....` → przytrzymaj **BOOT**). Serial: 115200.

⚠️ Przed podłączeniem serw i pompki przeczytaj „Złote zasady” w `CLAUDE.md` (serwa max 6 V, dioda flyback, BHP).

## Dokumenty

| Co | Gdzie |
|---|---|
| Zakres i stan prac | `docs/zakres.md` |
| Podział pracy, kontrakty między modułami | `docs/podzial_pracy.md` |
| Karta projektu i Scenariusze (zatwierdzone, nie edytujemy) | PDF poza repo (wersja oddana prowadzącej) |
| Sprzęt, protokół ESP32, złote zasady | `CLAUDE.md` |
