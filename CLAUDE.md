# SmartGuard: Sentry Edition — kontekst projektu (dla Claude Code)

> Ten plik jest automatycznie czytany przy starcie. Zawiera stan i decyzje projektu,
> żeby nowa sesja (np. uruchomiona z cmd) miała pełny kontekst bez historii czatu.

## Czym jest projekt
Inteligentny system ochrony posesji (projekt na Inżynierię Oprogramowania, Informatyka rok II):
detekcja ludzi (YOLO) → autonomiczna wieżyczka Pan-Tilt strzelająca wodą → identyfikacja
swój/wróg (IFF po BLE) → powiadomienia (n8n + Telegram) → panel WWW (FastAPI).

Zespół: diablak04 (PO), DEV (Hardware), AxmBro (SM).
Termin oddania: 24.01.2027.

## Gdzie co jest
- **To repo:** `D:\smartguard\smartguard-app` — kod aplikacji (Python) + firmware ESP32.
- **GitHub:** https://github.com/diablak04/smartguard-sentry (publiczne; ochrona main TYMCZASOWO ZDJĘTA na czas solo-pracy — włączyć „PR + 1 approval" gdy zespół dołączy).
- **Kanban:** https://github.com/users/diablak04/projects/1 (kolumny: Backlog / In Progress / Testing / Done; karty = Fazy+Sprinty z karty projektu).
- **Dokumenty** (Downloads): `SmartGuard_Karta_Projektu_Sentry_Edition_v2.pdf` (formalna karta),
  `SmartGuard_Instrukcja_wykonawcza.pdf` (plan dzień-po-dniu + kod startowy).
- **Symulacja CFD lufy:** `D:\smartguard\model\gotowe godot\simscale\` (OpenFOAM/SimScale).

## Stos technologiczny
- Python 3.11+: `ultralytics` (YOLO11n), `opencv-python`, `pyserial` (ESP32↔PC), `fastapi`+`uvicorn`, `requests`. (`bleak` tylko opcjonalny fallback — **IFF/BLE skanuje ESP32**, bo PC nie ma Bluetooth; patrz protokół.)
- Mikrokontroler: **ESP32** (NIE Arduino Nano — zmienione), Arduino C++ + `ESP32Servo`.
- n8n (lokalnie w Dockerze) + bot Telegram. Baza: SQLite.

## Model YOLO
Używać **`yolo11n.pt`** (Nano) — NIE trenować, model gotowy, filtrować klasę `person` (0).
Awaryjnie `yolo11s` jeśli Nano gubi cele. Cel wydajności: 3–5 FPS na CPU, <200 ms/klatkę.

## Finalny BOM (kluczowe, zweryfikowane)
- 2× serwo MG996R (metal, 180°) — **zasilanie MAX 6 V**.
- Uchwyt Pan-Tilt (z łożyskiem) — kupiony (albo druk 3D).
- Pompka spryskiwacza 12 V + wężyk silikonowy 4/6 mm + **lufa: rurka mosiężna Ø2,5/1,5 mm, wylot Ø1,5 mm**.
- ESP32 (z domu), moduł MOSFET D4184 (trigger 3,3 V), przetwornica **XL4015 5A** (12V→5–6V dla serw), kondensator 1000 µF, dioda 1N4007 (flyback na pompce).
- Laser 650nm 5V przez tranzystor 2N2222 (+ rez. 1kΩ baza, 10kΩ pull-down), buzzer aktywny 5V.
- Zasilacz 12V ≥3A (z domu), gniazdo DC 5.5/2.1, płytka 830 pól, przewody Dupont.
- IFF: brelok BLE (stały MAC) w kieszeni.

## Złote zasady (NIE łamać)
1. **Serwa max 6 V** — ustaw XL4015 miernikiem PRZED podłączeniem serw.
2. **Wylot lufy Ø1,5 mm** — nie szerszy (zweryfikowane CFD: strumień ~13,4 m/s, ~0,9 bar, ~1,4 l/min).
3. **Dioda flyback 1N4007** na pompce obowiązkowa (chroni MOSFET).
4. **ESP32 = logika 3,3 V** — laser przez tranzystor; MOSFET D4184 łapie 3,3 V.
5. **Prąd pompki/serw NIE przez płytkę stykową** — bezpośrednie przewody.
6. **Celować w korpus, nigdy w głowę** (BHP); impuls pompki max 200 ms.
7. Konfiguracja w `config.json` — zero sztywnych wartości w kodzie.

## Protokół PC ↔ ESP32 (UART 115200)
PC→ESP32: `AIM:<pan>,<tilt>` · `FIRE:<ms>` · `LASER:0/1` · `BUZZ` · `SCAN:ON/OFF`
ESP32→PC: `IFF:<0/1>,<rssi>` — swój widoczny (brelok BLE) + siła sygnału. **Skan BLE robi ESP32** (ma wbudowane BLE; PC bez BT).

## Plan realizacji (skrót — pełny w Instrukcji wykonawczej)
Dzień 1 detekcja YOLO · 2 strefa+3 klatki · 3 IFF BLE · 4 elektronika+firmware ·
5 wieżyczka+woda · 6 Visual Servoing (integracja, pierwszy strzał) · 7 SQLite+zdjęcia+n8n+Telegram ·
8 panel WWW · 9 tryby+BHP · 10 testy+oddanie. Dni 1–3 bez sprzętu (robić od razu).

## Stan na teraz
Zrobione: repo + struktura + firmware szkic + Kanban. Następne: Sprint 1 — detekcja YOLO
i skaner BLE (`detector.py`, `rules.py`), n8n lokalnie, bot Telegram.
