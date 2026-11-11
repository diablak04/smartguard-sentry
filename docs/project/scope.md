# Zakres: co budujemy

Baza = przypadki użycia z zatwierdzonych **Scenariuszy** (UC-01–UC-04 + UC-07). Robimy działający przepływ,
nie wszystkie wymagania z karty. Sentry (wieżyczka) = rozszerzenie u PO.

Zasady:
- **Najpierw rdzeń, potem reszta.** Rdzeń = scenariusz główny każdego UC + wyjątki z tabel niżej.
- **Sentry nie psuje bazy:** baza działa bez ESP32 (wieżyczka w trybie SIM) i bez Dockera.
- **PDF-ów nie zmieniamy.** Odstępstwa → tabela na dole.
- Numery w nawiasach `[5]` = wymagania z karty projektu.

Stan: jest · częściowo · brak (sprawdzone w kodzie 11.11.2026).

## Rdzeń

### UC-01 Wykrywanie intruza w strefie — PO
| Co | Stan | Uwagi |
|---|---|---|
| Źródło obrazu z configu: kamera / plik / RTSP [1] | częściowo | config zna tylko numer kamery |
| Tryb demo: MP4 w pętli [1.1] | brak | po końcu pliku `smartguard/capture.py` nie przewija |
| YOLO, tylko ludzie, próg 0,5 [2] | jest | `smartguard/detector.py` |
| Punkt stóp w strefie, strefa ma nazwę [3] | częściowo | działa, brak nazwy strefy |
| Wejście po 3 klatkach [3.1] | jest | `FrameConfirmation` w `smartguard/rules.py` |
| Strefa pusta po 3 klatkach bez nikogo [3.1] | brak | potrzebne, żeby osoba stojąca w strefie dała jedno zdarzenie |

### UC-01 → zapis zdarzenia — SM
| Co | Stan | Uwagi |
|---|---|---|
| JPG z ramkami + wiersz w SQLite, status „niewysłany” [4] | brak | `smartguard/events.py` = zaślepka |
| Zapis **przed** wysyłką alertu [15] | brak | kolejność w `main.py` |

### UC-02 Wysłanie alertu ze zdjęciem — DEV (wysyłka), SM (warunki)
| Co | Stan | Uwagi |
|---|---|---|
| `sendPhoto` z podpisem: godzina, strefa [5] | brak | brak `smartguard/notifier.py` |
| Błąd sieci nie zatrzymuje programu [15] | brak | `notifier` zwraca False, nie rzuca wyjątku |
| Max 1 alert / 60 s na strefę [5.1] | brak | `cooldown_s` w configu dotyczy wieżyczki |
| Godziny czuwania [7] | częściowo | wartości w configu, brak sprawdzenia |

### UC-03 Zarządzanie zdarzeniami + UC-07 Logowanie — SM
| Co | Stan | Uwagi |
|---|---|---|
| Logowanie Basic Auth, login i hasło w `.env` [16] | brak | |
| Lista od najnowszego: miniatura, data, strefa, status [6] | brak | brak `smartguard/api.py` |
| Duże zdjęcie po kliknięciu [6] | brak | |
| Pusta lista z komunikatem (3a) | brak | |
| Czytelne na telefonie, ~360 px [18] | brak | |

### UC-04 Oznaczenie fałszywego alarmu — SM
| Co | Stan | Uwagi |
|---|---|---|
| Przycisk „Fałszywy alarm” + licznik [8] | brak | już oznaczone → bez zmian (1a) |

## Po rdzeniu (jeśli starczy czasu)
Ponawianie alertów i ponowne łączenie z kamerą [15.1] · wyciszenie UC-05 [9] · konfiguracja w panelu UC-06 [10] ·
przyciski w Telegramie [11] · n8n [12] · usuwanie po 30 dniach [17.1].
Na koniec: test README na czystym komputerze [19], log średniego czasu ze 100 klatek [13].

## Sentry Edition — PO
Wieżyczka Pan-Tilt, pompka, laser, buzzer, firmware ESP32, IFF po BLE, visual servoing. Zasady i protokół: [`docs/agents/hardware.md`](../agents/hardware.md).

## Odstępstwa od karty
Decyzje podjęte w ramach karty (bez odstępstwa), z uzasadnieniem: [`docs/project/decisions.md`](decisions.md).

| Karta | U nas | Dlaczego |
|---|---|---|
| Trello | GitHub Projects (Kanban) | jedno miejsce z kodem i PR-ami |
| YOLO26n na start | `yolo11n` | karta dopuszcza; ~40 ms/klatkę (pomiar 2026-11-09, detekcja na żywo z kamery) |
| Tylko `config.json` | + `config.local.json` per komputer | nikt nie nadpisuje ustawień innym |
| Telegram bezpośrednio z Pythona, n8n dodatkowo | tak samo (stary plan Sentry: przez n8n) | baza bez Dockera |
| Moduły z § 7 karty | + `smartguard/zone.py`, `smartguard/config.py` i pliki Sentry | podział zgodny z kartą |
| Brak wieżyczki | Sentry | rozszerzenie, karta go nie wyklucza |
