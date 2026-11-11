# SmartGuard: Sentry Edition — kontekst projektu (dla Claude Code)

> Ten plik jest automatycznie czytany przy starcie. Zawiera stan i decyzje projektu,
> żeby nowa sesja (np. uruchomiona z cmd) miała pełny kontekst bez historii czatu.

## Czym jest projekt
Inteligentny system ochrony posesji (projekt na Inżynierię Oprogramowania, Informatyka rok II):
detekcja ludzi (YOLO) → autonomiczna wieżyczka Pan-Tilt strzelająca wodą → identyfikacja
swój/wróg (IFF po BLE) → powiadomienia (Telegram, dodatkowo n8n) → panel WWW (FastAPI).

**Dwie warstwy:** baza = przypadki użycia UC-01–04 + UC-07 z zatwierdzonych Scenariuszy (wykrycie w strefie →
zdarzenie SQLite + zdjęcie → alert Telegram → panel; **to jest oceniane**), Sentry (wieżyczka, IFF, ESP32) = rozszerzenie.
Najpierw baza, bez overengineeringu; Sentry nie może jej psuć. Szczegóły + odstępstwa od karty: `docs/zakres.md`.

Zespół: `diablak04` (PO, hardware + rdzeń wizji + Sentry), `AxmBro` (SM, panel WWW + integracja),
DEV (Telegram + testy). Szczegóły: `docs/podzial_pracy.md`.
Termin oddania: 24.01.2027.

## Repo jest PUBLICZNE (NIE łamać)
Projekt na studia (IO), ale to, co wypychamy, widzi każdy: kod, docs, instrukcje, commity, PR, issue.
**Wypychamy tylko rzeczy gotowe do pokazania, jak w pracy:** działa, sprawdzone, krótko opisane, bez śmieci
(pliki tymczasowe, zakomentowany kod, debugowe printy, TODO bez karty na Kanbanie). Lepiej mniej, ale porządnie.

Dane osobowe:
1. **Bez imion i nazwisk** (zespół, prowadząca, osoby trzecie). Tylko role (PO / SM / DEV) i loginy GitHub.
2. **Bez kontaktów i sekretów:** e-maile, telefony, tokeny, zawartość `.env`, prawdziwe MAC breloków, adresy kamer z hasłem.
3. **Bez ścieżek z nazwą użytkownika** (`C:\Users\<ktoś>\...`).
4. **Bez zdjęć zdarzeń, nagrań testowych i bazy** — widać na nich ludzi (RODO). Leżą w `events/`, `videos/`, `*.db`, poza gitem.
5. **Przed każdym commitem i PR:** przejrzyj `git diff --cached`. Czujnik u siebie (raz na komputer):
   w `.git/info/zakazane.txt` wpisz nazwiska do blokowania (jedno w linii, bez pustych linii — plik nie trafia do repo),
   sprawdzenie: `git diff --cached | grep '^+' | grep -i -F -f .git/info/zakazane.txt` → ma nic nie zwrócić.
6. Wyciek już w historii → zgłoś PO; nie „poprawiaj” go nowym commitem (historia zostaje).

## Twoje prywatne notatki dla Claude Code — `CLAUDE.local.md`
Każdy może mieć w korzeniu repo własny `CLAUDE.local.md`. Claude Code czyta go automatycznie obok tego pliku,
a git go ignoruje (`.gitignore`), więc nie trafia na GitHuba. Wpisz tam to, co tylko twoje: rolę, ścieżki do własnych
notatek i materiałów, preferencje pracy. Tam wolno ścieżki bezwzględne i nazwiska. Tutaj nie.

## Gdzie co jest
- **To repo:** kod aplikacji (Python) + firmware ESP32. Każdy klonuje gdzie chce — **nie wpisuj nigdzie ścieżek bezwzględnych** (np. `C:\...`); ścieżki w kodzie liczone od folderu projektu.
- **GitHub:** https://github.com/diablak04/smartguard-sentry (publiczne; zasady Git — „Praca zespołowa” niżej).
- **Kanban:** https://github.com/users/diablak04/projects/1 (kolumny: Backlog / In Progress / Testing / Done; jedna karta = jedno wymaganie z karty projektu, np. `[5] Alert na Telegram`).
- **Dokumenty formalne (zatwierdzone przez prowadzącą, nie edytujemy):** Karta Projektu IO i Scenariusze
  przypadków użycia (PDF, poza repo). Odstępstwa od nich → `docs/zakres.md`.
- **Dokumenty robocze Sentry** (poza repo): `SmartGuard_Karta_Projektu_Sentry_Edition_v2.pdf`,
  `SmartGuard_Instrukcja_wykonawcza.pdf` (plan dzień-po-dniu, BOM).
- **Symulacja CFD lufy:** poza repo, lokalnie u lidera (OpenFOAM/SimScale).

## Praca zespołowa
- **Git (zespół 3 osób):** każdy na swojej gałęzi `<type>/<short-description>` (Conventional Branch:
  `feat`/`fix`/`docs`/`chore`, kebab-case, np. `feat/web-panel`), do `main` tylko przez PR z 1 approval.
  Commity: Conventional Commits `<type>(<scope>): <opis>` — opis po polsku.
  (Ochrona `main` na GitHubie w 11.2026 jeszcze wyłączona — do włączenia przez właściciela repo.)
- **Kto co robi + interfejsy między modułami:** `docs/podzial_pracy.md`.
- **Konfiguracja:** `config.json` wspólny, `config.local.json` per komputer (poza gitem). Czytać przez
  `config.wczytaj_config()`, zapisywać przez `config.zapisz_lokalnie()` — nigdy nie nadpisywać `config.json` z kodu.
  Port ESP32 = `"auto"` (wykrywanie po USB w `turret_controller.py`).
- **Nowa biblioteka** → `requirements.txt` z komentarzem, do czego jest.

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
7. Konfiguracja w `config.json` (+ `config.local.json` per komputer) — zero sztywnych wartości w kodzie.

## Protokół PC ↔ ESP32 (UART 115200)
PC→ESP32: `AIM:<pan>,<tilt>` · `FIRE:<ms>` · `LASER:0/1` · `BUZZ` · `SCAN:ON/OFF`
ESP32→PC: `IFF:<0/1>,<rssi>` — swój widoczny (brelok BLE) + siła sygnału. **Skan BLE robi ESP32** (ma wbudowane BLE; PC bez BT).

## Stan i plan
Stan i kolejność prac: `docs/zakres.md` (najpierw rdzeń UC-01–04 + UC-07, potem reszta, Sentry równolegle u PO).
Bieżące zadania: Kanban. Harmonogramów z datami nie trzymamy w repo — szybko się dezaktualizują.
