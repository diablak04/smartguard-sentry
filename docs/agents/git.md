# Git i publiczne repo

> **Kiedy czytać:** przed każdym `git add` / commit / push / PR / issue. Kanban i Definicja Ukończenia:
> `docs/project/team.md` § Jak pracujemy.

## Gałęzie i commity
1. `git checkout main` → `git pull`
2. `git checkout -b feat/krotki-opis` (albo `fix/`, `docs/`, `chore/`; kebab-case, po angielsku)
3. commity `typ(zakres): opis po polsku`, np. `feat(events): zapis zdarzenia do SQLite` (Conventional Commits)
4. `git push -u origin feat/krotki-opis` → Pull Request → 1 approval drugiej osoby → merge

## Zasady
- Do `main` tylko przez PR. Ochrona `main` na GitHubie w 11.2026 jest jeszcze wyłączona, do włączenia przez właściciela repo.
- Asystent AI robi commit, push, PR i issue tylko na wyraźne polecenie użytkownika w bieżącej wiadomości
  („zakomituj”, „wypchnij”). Pytanie („zakomitować?”), „ogarnij”, zatwierdzony plan ani zgoda z wcześniejszej
  wiadomości nie są poleceniem: asystent kończy pracę na niezacommitowanych zmianach, mówi, co jest gotowe, i czeka.
  Kiedy powstaje commit, decyduje człowiek.
- Issue i PR są publiczne: obowiązują te same zasady danych osobowych co w kodzie (`AGENTS.md` § Repo jest publiczne).

## Pull request
- **Jeden PR = jedna zmiana logiczna:** funkcja, poprawka, refaktor albo dokumenty. Mieszanka → podziel, bo recenzent
  nie odróżni zmiany zachowania od przeniesienia kodu, a cofnięcie jednej rzeczy cofa wszystko.
- Sygnały do podziału: zmiana dotyka kilku obszarów z tabeli `AGENTS.md`, refaktor razem z nową funkcją, kilkaset linii
  kodu do przejrzenia. Asystent AI proponuje podział sam, zanim zacznie commitować.
- Przeniesienie plików (`git mv`) to osobny commit bez zmian treści: wtedy `git log --follow` zachowuje historię pliku.
- Dokumenty idą w tym samym PR co kod, którego dotyczą (stan w `docs/project/scope.md`, decyzja w `docs/project/decisions.md`). Zmiana bez nich
  jest niedokończona.
- Opis według szablonu `.github/pull_request_template.md` (GitHub wstawia go sam): co i po co, jak sprawdzone, czego
  nie sprawdzono, `Closes #<nr issue>`.

## Czujnik danych osobowych (raz na komputer)
W `.git/info/zakazane.txt` wpisz nazwiska do blokowania (jedno w linii, bez pustych linii; plik nie trafia do repo).
Przed każdym commitem i PR:
```
git diff --cached | grep '^+' | grep -i -F -f .git/info/zakazane.txt
```
Ma nic nie zwrócić.

## Przepisana historia
W 11.2026 historia `main` na GitHubie została przepisana (te same pliki, nowe hashe, autorzy commitów bez imion i nazwisk).
- Gdy lokalny `main` „diverged” od `origin/main`, a treść jest ta sama: **nie** `git pull` (wmerge'owałby starą historię),
  tylko przy czystym drzewie `git fetch` → `git checkout main` → `git reset --hard origin/main`.
- Stare lokalne gałęzie sprzed przepisania usuń; nie wypychaj ich.
