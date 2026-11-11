# Research: log przebiegów

> **Kiedy czytać:** zanim zaczniesz research albo zaproponujesz temat, który mógł być już rozważany, i gdy szukasz
> uzasadnienia decyzji. Jeden wiersz na przebieg, najnowsze na górze. Jak robić research: [`docs/agents/research.md`](../agents/research.md).

Aktualny stan żyje w kolumnie „Zastosowane w”; opracowanie to uzasadnienie na dzień jego daty.

| Data | Temat | Werdykt | Zastosowane w | Opracowanie |
|---|---|---|---|---|
| 2026-11-11 | Czy szablon PR ma sens w zespole 3 osób (Pirouzkhah i in., MSR '26: 80 tys. PR; Zhang i in., IST 2022, za MSR '26; dowód przeciw: lista kontrolna odhaczana bez czytania w zespole 3 osób) | Krótki szablon tak: co i po co, jak sprawdzone, na co spojrzeć przy przeglądzie (wskazanie oczekiwanego przeglądu: PR o 64–72% częściej scalane); długiej listy do odhaczania nie | `.github/pull_request_template.md` | wiersz logu; źródła w opisie commita |
| 2026-11-11 | Układ punktów wejścia małej aplikacji Python bez instalacji pakietu (dokumentacja Pythona `__main__` i `argparse`, The Hitchhiker's Guide to Python; Real Python niedostępny, 403) | Jeden skrypt w korzeniu z trybami jako podkomendy, logika trybów w pakiecie; wzorzec jak `manage.py` w Django | `main.py`, `docs/agents/code.md` § Struktura | [`docs/project/decisions.md` § D-04](../project/decisions.md#d-04) (jedno wejście main.py): źródła i odrzucone warianty |
| 2026-11-11 | Jak asystenci AI wczytują instrukcje projektu: [`AGENTS.md`](../../AGENTS.md), [`CLAUDE.md`](../../CLAUDE.md), `CLAUDE.local.md` (test w Claude Code 2.1.322 na plikach testowych) | Wejście w `AGENTS.md`, `CLAUDE.md` tylko z importami `@AGENTS.md` i `@AGENTS.local.md`; nie `CLAUDE.local.md`, bo jego obecność wyłącza `AGENTS.md` | `AGENTS.md`, `CLAUDE.md` | [`docs/project/decisions.md` § D-03](../project/decisions.md#d-03) (instrukcje dla AI): wynik testu |
| 2026-11-11 | Gdzie trzymać skrypty uruchomieniowe przy pakiecie `smartguard/` bez instalacji (test importu) | Skrypty w korzeniu repo; nie `scripts/`, bo uruchomiony tam skrypt nie widzi pakietu | [`docs/agents/code.md`](../agents/code.md) § Struktura | [`docs/project/decisions.md` § D-02](../project/decisions.md#d-02) (konwencja kodu): wynik testu |
