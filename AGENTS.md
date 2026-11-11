# AGENTS — SmartGuard: Sentry Edition

System ochrony posesji (projekt na Inżynierię Oprogramowania, Informatyka rok II): kamera → detekcja ludzi (YOLO) →
zdarzenie w SQLite + zdjęcie → alert na Telegram → panel WWW (FastAPI). Rozszerzenie Sentry: wieżyczka Pan-Tilt
strzelająca wodą + rozpoznawanie swój/wróg (IFF) po breloku BLE (ESP32). Python 3.13 (instalacja: `README.md` § Uruchomienie), Windows, SQLite.

**Jedno wejście dla asystentów AI.** Copilot, Cursor i Codex czytają ten plik same, Claude Code przez `CLAUDE.md`
(tam tylko import). Zasady obszarów są w jednej kopii w `docs/agents/`. Dla ludzi: `README.md`.

## Zanim zaczniesz (raz na wątek)

0. **Każde zadanie z kodem lub dokumentami:** przeczytaj `docs/agents/workflow.md`: rozumiesz to, co oddajesz; gotowe = dowód; instalacje i operacje niszczące za zgodą.
1. **Zanim edytujesz plik z kolumny Kod**, przeczytaj plik z kolumny Zasady (`docs/agents/`). Trzymają pułapki, których nie widać w kodzie.
2. Kolumna Dokumenty mówi, gdzie są wymagania, stan i decyzje obszaru. Czytaj wskazany §, nie cały plik.
3. Plik zasad albo § już jest w wątku → nie czytaj go ponownie.
4. Jeśli w korzeniu repo jest `AGENTS.local.md`, przeczytaj go (Claude Code ładuje go sam).

| Obszar | Kod | Zasady | Dokumenty |
|---|---|---|---|
| Każda zmiana w Pythonie | `*.py`, `config*.json`, `requirements.txt` | `docs/agents/code.md` | `docs/project/decisions.md` § D-02 (konwencja kodu) |
| Detekcja, strefa, potwierdzanie (UC-01) | `smartguard/capture.py`, `detector.py`, `zone.py`, `rules.py`, `calibrate.py`, `preview.py` | `docs/agents/code.md` | `docs/project/scope.md` § UC-01 Wykrywanie |
| Zapis zdarzeń: SQLite + zdjęcia | `smartguard/events.py` | `docs/agents/code.md` § Pliki generowane | `docs/project/scope.md` § UC-01 → zapis; `docs/project/team.md` § Co kto komu przekazuje |
| Alert na Telegram (UC-02) | `smartguard/notifier.py` (do napisania), `.env` | `docs/agents/code.md` § Konfiguracja | `docs/project/scope.md` § UC-02 |
| Panel WWW, logowanie, fałszywy alarm (UC-03, UC-04, UC-07) | `smartguard/api.py` (do napisania) | `docs/agents/code.md` | `docs/project/scope.md` § UC-03, § UC-04 |
| Maszyna stanów, spięcie modułów | `main.py` (wybór trybu), `smartguard/live.py`, `demo.py`, `state_machine.py` | `docs/agents/code.md` | `README.md` § Jak to działa |
| Wieżyczka, ESP32, IFF/BLE, okablowanie | `firmware/**`, `smartguard/turret.py`, `smartguard/ble_scanner.py` | `docs/agents/hardware.md` (+ `docs/agents/code.md` dla `*.py`) | `docs/project/decisions.md` § D-01 (skan BLE na ESP32); `docs/project/scope.md` § Sentry; `README.md` § ESP32 |
| Dokumentacja na oddanie: architektura, ERD, UML, testy | `docs/design/**` | `docs/agents/docs.md` | `docs/README.md` § Dokumentacja na oddanie; `docs/project/scope.md` |
| Instrukcje dla AI, dokumenty, notatki, zasady | `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/**` | `docs/agents/docs.md` | `docs/project/decisions.md` § D-03 (instrukcje dla AI) |
| Commit, push, PR (jeden PR = jedna zmiana), issue | `.github/` | `docs/agents/git.md` | `docs/project/team.md` § Jak pracujemy |
| Research, deep research, temat mógł być już rozważany | `docs/research/**` | `docs/agents/research.md` | `docs/research/README.md` (log) |
| „Czemu tak, a nie inaczej?”, wybór technologii | — | — | `docs/project/decisions.md` (sprawdź, czy już nie rozstrzygnięte) |
| Co dalej, stan prac, kto co robi | — | — | Kanban; `docs/project/scope.md`; `docs/project/team.md` |

`docs/project/scope.md`, `docs/project/decisions.md`, `docs/project/team.md` leżą w `docs/project/`; mapa całego `docs/`: `docs/README.md`.

## Repo jest publiczne

To, co wypychamy, widzi każdy: kod, dokumenty, instrukcje, commity, PR i issue. Wypychamy tylko rzeczy gotowe do
pokazania: działają, są sprawdzone, krótko opisane. Czego nie dodajemy (kopie, surowe zapisy AI, TODO, puste
szablony): `docs/agents/docs.md` § Czego nie dodajemy.

Dane osobowe (RODO i zwykła przyzwoitość, bo repo czytają obcy):
1. Bez imion i nazwisk (zespół, prowadząca, osoby trzecie): tylko role (PO / SM / DEV) i loginy GitHub.
2. Bez kontaktów i sekretów: e-maile, telefony, tokeny, zawartość `.env`, prawdziwe MAC breloków, adresy kamer z hasłem.
3. Bez ścieżek z nazwą użytkownika (`C:\Users\<ktoś>\...`).
4. Bez zdjęć zdarzeń, nagrań testowych i bazy, bo widać na nich ludzi. Są poza gitem; gdzie leżą: `docs/agents/code.md` § Pliki generowane.
5. Przed każdym commitem i PR: przejrzyj `git diff --cached` i puść czujnik nazwisk (`docs/agents/git.md` § Czujnik).
6. Wyciek już w historii → zgłoś PO; nie poprawiaj go nowym commitem, bo historia i tak zostaje.

## Co publiczne, co prywatne

| Gdzie | W gicie | Co tam jest |
|---|---|---|
| `README.md`, `AGENTS.md`, `docs/**` | tak | wejście dla ludzi, zasady, zakres, decyzje, research, dokumentacja (mapa: `docs/README.md`) |
| `AGENTS.local.md` | nie | twoje instrukcje dla asystenta: rola, prywatne źródła (PDF-y karty), preferencje |
| `notes/` | nie | twój brudnopis: `sesje/`, `research/` (surowe raporty), `archiwum/` |
| `config.local.json`, `.env` | nie | ustawienia twojego komputera, sekrety |
| `models/`, `logs/`, `data/` | nie | pliki generowane (`docs/agents/code.md`) |

`notes/` to brudnopis, nie śmietnik: co warte pokazania, przepisz krótko według `docs/agents/docs.md` § Gdzie co zapisać.
W plikach prywatnych wolno ścieżki bezwzględne i nazwiska, w publicznych nie. `notes/` czytasz tylko wtedy, gdy
użytkownik go wskaże. Nie twórz `CLAUDE.local.md`: to dawna nazwa `AGENTS.local.md`, a jej obecność wyłącza
w Claude Code ten plik (`docs/project/decisions.md` § D-03).

## Zawsze

- Najpierw rdzeń oceniany na zajęciach (UC-01–04 + UC-07), potem reszta; Sentry nie może go psuć. Bez overengineeringu.
- Nazwy w kodzie po angielsku, komentarze i teksty po polsku (`docs/project/decisions.md` § D-02 (konwencja kodu)).
- Nowe progi, czasy, kąty i porty dodajesz do `config.json`, nie do kodu; kod nigdy nie nadpisuje `config.json`
  (`docs/agents/code.md` § Konfiguracja).
- Ścieżki od folderu projektu (`project_path()` w `smartguard/config.py`), nie od bieżącego katalogu. Pliki
  generowane tylko w `models/`, `logs/`, `data/`.
- Wieżyczka: impuls pompki max 200 ms, cel w korpus, nigdy w głowę (pozostałe złote zasady: `docs/agents/hardware.md`).
- Wiedzę zapisujesz według `docs/agents/docs.md` § Gdzie co zapisać: jedna rzecz = jedno miejsce, nowe dokumenty w `docs/`.
- Commit, push, PR i issue tylko na prośbę użytkownika (`docs/agents/git.md` § Zasady); instalacje i operacje
  niszczące tylko za zgodą (`docs/agents/workflow.md` § Bezpiecznie).

## Stos
- Python: `ultralytics` (YOLO), `opencv-python`, `pyserial` (ESP32 ↔ PC), `fastapi` + `uvicorn`, `requests`.
- Model `yolo11n.pt` (Nano), gotowy, nie trenujemy; tylko klasa `person` (0). Awaryjnie `yolo11s`, jeśli Nano gubi cele.
  Cel: 3–5 FPS na CPU, < 200 ms na klatkę.
- ESP32 (Arduino C++ + `ESP32Servo`); skan BLE robi ESP32, nie PC (`docs/project/decisions.md` § D-01).
- n8n (lokalnie w Dockerze) + bot Telegram. Baza: SQLite.

## Gdzie co jest
- GitHub: https://github.com/diablak04/smartguard-sentry. Każdy klonuje, gdzie chce.
- Kanban: https://github.com/users/diablak04/projects/1; zasady kart: `docs/project/team.md` § Jak pracujemy.
- Karta Projektu IO i Scenariusze (zatwierdzone przez prowadzącą) to PDF-y poza repo, nie edytujemy ich; streszczenie:
  `docs/project/scope.md`. Zespół i role (Product Owner PO, Scrum Master SM, DEV):
  `docs/project/team.md`.
