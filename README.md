# SmartGuard: Sentry Edition

Inteligentny system aktywnej ochrony perymetrycznej: detekcja ludzi (YOLO),
autonomiczna wieżyczka Pan-Tilt, identyfikacja IFF (BLE) i powiadomienia (n8n + Telegram).

Projekt z przedmiotu **Inżynieria Oprogramowania** (Informatyka, rok II).

## Zespół
- Wiktor Makowski (Product Owner) — architektura, wizja (YOLO), n8n, logika
- Jakub Marchewka (Lead Hardware) — elektronika, mechanika, firmware ESP32, zasilanie
- Bartłomiej Mucha (Scrum Master) — persystencja, Telegram, panel WWW, testy, dokumentacja

## Architektura (warstwy)
Kamera/BLE → `capture.py` → `detector.py` (YOLO) → `rules.py` (strefa + 3 klatki + IFF)
→ `turret_controller.py` (Visual Servoing) → ESP32 (serwa/pompka/laser)
oraz `events.py` (SQLite + JPG) → n8n → Telegram, panel WWW (FastAPI).

## Uruchomienie
```bash
pip install -r requirements.txt
cp .env.example .env        # uzupełnij token Telegrama i URL webhooka n8n
python main.py
```

## Struktura
- `capture.py` — odczyt obrazu z kamer (główna + FPV)
- `detector.py` — detekcja ludzi modelem YOLO (yolo11n)
- `rules.py` — strefa chroniona, potwierdzenie 3 klatek, fuzja IFF (BLE)
- `turret_controller.py` — przeliczanie pozycji na kąty serw, śledzenie celu
- `events.py` — zapis zdarzeń (SQLite) + zdjęcia, webhook do n8n
- `main.py` — orkiestrator głównej pętli (maszyna stanów)
- `config.json` — konfiguracja (strefa, kąty, progi, godziny czuwania)
- `firmware/` — kod ESP32 (Arduino C++)

## Zasady pracy (Git)
- Gałąź `main` chroniona: zmiany **tylko przez Pull Request** z min. **1 zatwierdzeniem**.
- Pracuj na gałęziach `feature/<opis>`, łącz przez PR.

## Dokumentacja
Karta projektu i instrukcja wykonawcza — folder `docs/` (lub repo dokumentów zespołu).
