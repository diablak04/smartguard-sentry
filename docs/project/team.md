# Zespół i sposób pracy

Zakres = przypadki użycia ze Scenariuszy (UC-01–04 + UC-07). Każdy UC ma jednego właściciela.
Stan prac: [`docs/project/scope.md`](scope.md). Bieżące zadania: Kanban.

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

## Jak pracujemy

Narzędzia (karta § 6.1, z jedną zmianą: zamiast Trello GitHub Projects, bo zadania są w jednym miejscu z kodem i PR):

| Do czego | Narzędzie |
|---|---|
| kod, przegląd zmian | GitHub, to repo; przepływ: `docs/agents/git.md` § Gałęzie i commity |
| zadania | [Kanban na GitHub Projects](https://github.com/users/diablak04/projects/1) |
| bieżąca komunikacja, Daily | Discord |
| diagramy UML i ERD | draw.io, DataModeler |

**Kanban:** kolumny Backlog → In Progress → Testing → Done.
- Jedna karta = jedno wymaganie z [`docs/project/scope.md`](scope.md), w tytule numer z karty, np. `[5] Alert na Telegram`.
- Kartę zakładasz jako issue w repo i dodajesz do projektu.
- PR z `Closes #<nr issue>` zamyka issue po merge; karta sama przechodzi do Done, jeśli w projekcie jest włączony
  workflow „Item closed”.

## Definicja Ukończenia

Karta projektu § 12.1. Karta na Kanbanie idzie do Done, gdy:
- kod jest w `main` przez PR zatwierdzony przez drugą osobę,
- działa w trybie demo na nagraniu testowym,
- wynik sprawdzenia jest w komentarzu karty,
- druga osoba uruchomiła zmianę u siebie,
- odstępstwo od karty jest wpisane w `docs/project/scope.md` § Odstępstwa od karty.
