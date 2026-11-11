# SmartGuard: Sentry Edition

Inteligentny system aktywnej ochrony perymetrycznej: detekcja ludzi (YOLO),
autonomiczna wieżyczka Pan-Tilt, identyfikacja IFF (BLE) i powiadomienia (n8n + Telegram).

Projekt z przedmiotu **Inżynieria Oprogramowania** (Informatyka, rok II).

## Zespół
- diablak04 (Product Owner) — architektura, wizja (YOLO), n8n, logika
- DEV (Lead Hardware) — elektronika, mechanika, firmware ESP32, zasilanie
- AxmBro (Scrum Master) — persystencja, Telegram, panel WWW, testy, dokumentacja

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

## Uruchomienie
```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
copy .env.example .env        # uzupełnij token Telegrama i URL webhooka n8n
```
Dema (model `yolo11n.pt` dociąga się sam przy pierwszym uruchomieniu):
```bash
.venv\Scripts\python.exe detekcja_test.py      # kamera + detekcja + strefa
.venv\Scripts\python.exe kalibracja_strefy.py  # klikasz strefę -> zapis do config.json
.venv\Scripts\python.exe integracja.py         # cały system na żywo (wieżyczka w SIM)
.venv\Scripts\python.exe main.py               # demo maszyny stanów (scenariusz)
```

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
- `config.json` — konfiguracja (strefa, kąty, progi, godziny czuwania, IFF)
- `firmware/` — kod ESP32: `smartguard_esp32` (główny), `ble_test`, `serwo_test`

## Zasady pracy (Git)
- **Obecnie praca solo** → ochrona `main` tymczasowo zdjęta, commity bezpośrednio na `main`.
- Gdy dołączy zespół: włączyć ochronę `main` (**PR + min. 1 approval**), pracować na `feature/<opis>`.

## Dokumentacja
Karta projektu i instrukcja wykonawcza — folder `docs/` (oraz repo dokumentów zespołu).
