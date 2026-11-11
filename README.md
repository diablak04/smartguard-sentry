# SmartGuard: Sentry Edition

Inteligentny system aktywnej ochrony perymetrycznej: detekcja ludzi (YOLO),
autonomiczna wieżyczka Pan-Tilt, identyfikacja IFF (BLE) i powiadomienia (n8n + Telegram).

Projekt z przedmiotu **Inżynieria Oprogramowania** (Informatyka, rok II).

## Zespół
- Wiktor Makowski (Product Owner) — architektura, wizja (YOLO), n8n, logika
- Jakub Marchewka (Lead Hardware) — elektronika, mechanika, firmware ESP32, zasilanie
- Bartłomiej Mucha (Scrum Master) — persystencja, Telegram, panel WWW, testy, dokumentacja

## Stan projektu (listopad 2026)
Działa i przetestowane (software, bez fizycznej wieżyczki):
- ✅ **Detekcja** YOLO `yolo11n` — ~40 ms/klatkę, ~25 FPS na CPU
- ✅ **Strefa** chroniona (wielokąt) + **potwierdzanie na 3 klatkach**
- ✅ **Maszyna stanów** IDLE→DETECTED→CONFIRMING→FRIENDLY/FOE→ENGAGE→COOLDOWN (+ MUTED)
- ✅ **IFF/BLE** — skanowanie na **ESP32** (PC bez Bluetooth), decyzja swój/wróg po nazwie/MAC + RSSI; sprawdzone sprzętowo
- ✅ **Integracja na żywo** (`integracja.py`) — cały łańcuch na kamerze, wieżyczka w trybie SIM (loguje AIM/FIRE)

Czeka na sprzęt (serwa, zasilanie, pompka): realne serwa, pierwszy strzał, układ wodny.
W planie (bez sprzętu): n8n + Telegram, SQLite + zapis zdarzeń/zdjęć, panel WWW.

## Architektura (przepływ)
Kamera → `capture.py` → `detector.py` (YOLO) → `zona.py` (strefa) + `rules.py` (3 klatki + IFF)
→ maszyna stanów (`main.py`) → `turret_controller.py` → ESP32 (serwa/pompka/laser).
IFF: ESP32 skanuje BLE → `IFF:<0/1>,<rssi>` → PC. Oraz `events.py` (SQLite + JPG) → n8n → Telegram, panel WWW (FastAPI).

## Szybki start (Windows)

**Raz na komputerze:** zainstaluj [Python 3.13](https://www.python.org/downloads/windows/)
(w instalatorze **zaznacz „Add python.exe to PATH”**). Pobierz projekt: zielone **Code → Download ZIP**
i rozpakuj (albo `git clone`). Sprzęt niepotrzebny — wieżyczka jest symulowana, wystarczy kamerka.

**W folderze projektu** kliknij pasek adresu w Eksploratorze, wpisz `cmd`, Enter, i wklej:
```bat
py -3.13 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```
1. tworzy prywatne środowisko `.venv` w folderze projektu (reszta systemu nietknięta),
2. instaluje biblioteki z `requirements.txt` — **~1,2 GB, ok. 5 min**,
3. demo bez kamery: w konsoli przewijają się stany aż do `Koniec scenariusza.` = instalacja OK.

**Programy z kamerą** (klawisze działają po kliknięciu w okno):

| Uruchom: `.venv\Scripts\python.exe …` | Co robi | Klawisze |
|---|---|---|
| `detekcja_test.py` | wykrywanie ludzi + strefa | `q` wyjście |
| `kalibracja_strefy.py` | klikasz rogi strefy chronionej | LPM punkt, `z` zapisz, `r` reset, `q` |
| `integracja.py` | cały system na żywo | `s` swój/wróg, `m` wycisz, `q` |

Model YOLO (5 MB) pobiera się sam przy pierwszym uruchomieniu.

**Twoje ustawienia — `config.local.json`** (opcjonalny, nie trafia do gita)

Program czyta najpierw wspólny `config.json`, a potem nadpisuje go tym, co jest w `config.local.json`.
Dopóki wszystko działa, ten plik nie jest potrzebny. Gdy chcesz coś zmienić tylko u siebie,
wpisz w oknie `cmd` otwartym w folderze projektu (jak przy instalacji):
```bat
copy config.local.example.json config.local.json
```
i w Notatniku zmień wartość:
- `"kamera_glowna"` — numer kamery: `0` = wbudowana, `1` = druga (np. na USB),
- `"esp32_port"` — zostaw `"auto"`; konkretny port (np. `"COM5"`) tylko gdy auto nie znajdzie płytki.

`config.local.example.json` to tylko wzór do skopiowania — program go nie czyta, nie edytuj go i nie usuwaj
(jest w repo dla następnych osób). Liczy się wyłącznie `config.local.json`.
Linijki, których nie zmieniasz, możesz usunąć. Strefę dopisuje tam sam `kalibracja_strefy.py`.
Każdy inny klucz z `config.json` też można tu nadpisać.

**Problemy:** `'py' is not recognized` → zainstaluj Pythona ponownie z „Add to PATH” ·
czarne okno / zła kamera → w `config.local.json` ustaw `"kamera_glowna": 1` · kamera zajęta → zamknij Teams/Zoom/Discord.

## ESP32 (tylko osoba od firmware)
1. [Arduino IDE 2](https://www.arduino.cc/en/software) → *Boards Manager*: **esp32** (Espressif) → *Library Manager*: **ESP32Servo**.
2. Podłącz ESP32 kablem USB **z danymi** (nie „tylko ładowanie”). Nie widać nowego portu COM w Menedżerze urządzeń →
   sterownik wg kostki przy USB: **CP2102** → Silicon Labs CP210x, **CH340** → WCH CH340.
3. Otwórz szkic z `firmware/` (na start `ble_test`), *Board: ESP32 Dev Module*, *Port: COMx*, Upload
   (wisi na `Connecting....` → przytrzymaj **BOOT**). *Serial Monitor*: 115200.

Portu nie trzeba wpisywać do konfiguracji — `"esp32_port": "auto"` sam znajduje ESP32 po USB.
⚠️ Przed serwami/pompką: „Złote zasady” w `CLAUDE.md` (serwa max 6 V, dioda flyback, BHP).

**n8n + Telegram** (Faza 7) — jeszcze nie instaluj; będzie potrzebny Docker Desktop i plik `.env` (z `.env.example`).

## Struktura
- `capture.py` — odczyt obrazu z kamery (wątek, bufor najnowszej klatki)
- `detector.py` — detekcja ludzi modelem YOLO (yolo11n), pomiar FPS
- `zona.py` + `kalibracja_strefy.py` — strefa chroniona (wielokąt 0–1) + kalibrator
- `rules.py` — potwierdzanie na N klatkach + klasyfikacja swój/wróg
- `main.py` — maszyna stanów + logging
- `turret_controller.py` — komendy do ESP32 (AIM/FIRE/LASER/BUZZ), tryb SIM
- `integracja.py` — pełna pętla na żywo (Visual Servoing, bez sprzętu w SIM)
- `ble_scanner.py` — skaner BLE po stronie PC (opcjonalny fallback; IFF robi ESP32)
- `events.py` — zapis zdarzeń (SQLite) + zdjęcia, webhook do n8n (TODO)
- `config.py` — wczytuje `config.json` (wspólny) + `config.local.json` (Twój komputer)
- `config.json` — konfiguracja (strefa, kąty, progi, godziny czuwania, IFF)
- `firmware/` — kod ESP32: `smartguard_esp32` (główny), `ble_test`, `serwo_test`

## Zasady pracy (Git)
- **Teraz (solo):** ochrona `main` wyłączona, commity na `main` albo na gałęzi `<type>/<short-description>`.
- **Zespół:** ochrona `main` (**PR + min. 1 approval lidera**), każdy na gałęzi `<type>/<short-description>` (np. `feat/web-panel`).
- Kto co robi: `docs/podzial_pracy.md`.

## Dokumentacja
Karta projektu i instrukcja wykonawcza — folder `docs/` (oraz repo dokumentów zespołu).
