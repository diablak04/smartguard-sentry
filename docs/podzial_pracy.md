# Podział pracy

Zakres = przypadki użycia ze Scenariuszy (UC-01–04 + UC-07). Każdy UC ma jednego właściciela.
Stan prac: `docs/zakres.md`. Bieżące zadania: Kanban.

## Role

| Rola | GitHub | Odpowiada za |
|---|---|---|
| **PO** | `diablak04` | kolejność zadań, odbiór UC; **wykrywanie (UC-01)** i **wieżyczka (Sentry)** |
| **SM** | `AxmBro` | Kanban, Daily, dokumentacja z zajęć, Moodle; **zapis zdarzeń, panel, spięcie** |
| **DEV** | *(do dodania)* | **alert na Telegram (UC-02)**, nagrania testowe |

## Kto robi który UC

| UC | Kto | Co ma działać |
|---|---|---|
| UC-01 Wykrywanie intruza | PO | kamera lub MP4 w pętli → YOLO → punkt stóp w strefie → potwierdzenie na 3 klatkach (wejście i wyjście) |
| UC-01 krok 6: zapis zdarzenia | SM | zdjęcie JPG z ramkami + wiersz w SQLite, przed wysyłką alertu |
| UC-02 Wysłanie alertu | DEV | zdjęcie z podpisem (godzina, strefa) na czat Telegram; brak internetu nie wywala programu |
| UC-02 krok 1: warunki wysyłki | SM | max 1 alert / 60 s na strefę, godziny czuwania |
| UC-07 Logowanie | SM | panel tylko po zalogowaniu, hasło w `.env` |
| UC-03 Zarządzanie zdarzeniami | SM | lista od najnowszego, duże zdjęcie, działa na telefonie |
| UC-04 Fałszywy alarm | SM | przycisk + licznik |
| Sentry | PO | wieżyczka, ESP32, IFF; u reszty działa w trybie SIM |

## Co kto komu przekazuje

```
PO  ──(wejście do strefy: strefa, pewność, klatka, ramki)──▶  SM
SM  ──(zdjęcie + podpis)──▶  DEV  ──(wysłane: tak / nie)──▶  SM
SM  ──(baza zdarzeń)──▶  panel
```

Zmiana tego, co się przekazuje = PR oglądany przez obie strony.

## Kolejność

1. UC-01 + zapis zdarzenia (PO, SM) — bez tego reszta nie ma danych.
2. UC-02 (DEV, SM) — pierwszy pełny alert na telefonie.
3. UC-07 + UC-03 (SM) — panel z logowaniem.
4. UC-04 (SM).

Sentry PO robi równolegle, gdy przyjdzie sprzęt. DEV od początku nagrywa nagrania testowe (karta § 9.1)
i wpisuje wyniki w karty na Kanbanie.
