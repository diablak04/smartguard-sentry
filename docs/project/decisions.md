# Decyzje techniczne

SmartGuard to projekt zespołowy na Inżynierię Oprogramowania. Zakres wyznaczają zatwierdzona Karta Projektu
i Scenariusze przypadków użycia; ich streszczenie i stan prac są w [`docs/project/scope.md`](scope.md). Tu zapisujemy decyzje podjęte
**w ramach** karty: co wybraliśmy, dlaczego i co odrzuciliśmy. Dzięki temu każdy, także osoba spoza zespołu,
zrozumie, skąd wziął się dany układ, bez czytania historii rozmów.

- Odstępstwa **od** karty: `docs/project/scope.md` § Odstępstwa od karty. Bieżące zadania: Kanban.
- Fakty w uzasadnieniach są sprawdzone (pomiar, test, kod); stan opisany w „Skutkach” ma datę wpisu.

**Jak dopisać:** nowy numer na końcu, najnowsza decyzja na dole, nad nagłówkiem stała kotwica `<a id="d-xx"></a>`
(do linków `decisions.md#d-xx`). Starej decyzji nie kasujemy: gdy ją zmieniamy,
dopisujemy nową, a w starej ustawiamy status „zastąpiona przez D-xx”. Bez imion i nazwisk: role (PO / SM / DEV).

```
## D-xx: <co postanowiliśmy> (RRRR-MM-DD, rola)
- **Status:** przyjęta | proponowana | zastąpiona przez D-yy
- **Dotyczy:** przypadek użycia / wymaganie karty / obszar
- **Problem:** co trzeba było rozstrzygnąć
- **Decyzja:** co wybraliśmy
- **Odrzucone:** inne warianty i dlaczego nie
- **Skutki:** co to zmienia w kodzie i pracy
```

<a id="d-01"></a>
## D-01: Skan BLE dla IFF robi ESP32, nie PC (2026-11-09, PO)
- **Status:** przyjęta
- **Dotyczy:** Sentry Edition (rozszerzenie poza rdzeniem karty): rozpoznawanie swój/wróg (IFF).
- **Problem:** IFF wymaga wykrycia breloka BLE „swojego”. Komputer deweloperski nie ma Bluetooth:
  `Get-PnpDevice -Class Bluetooth` zwraca pustą listę, a `bleak` zgłasza „No Bluetooth adapter found”.
- **Decyzja:** skanuje ESP32, który ma wbudowane BLE, i wysyła do PC `IFF:<0/1>,<rssi>` po UART.
- **Odrzucone:** dongiel USB Bluetooth do PC: dodatkowy zakup, a skan i tak lepiej robić przy wieżyczce,
  bo RSSI mierzony przy niej lepiej oddaje odległość od celu.
- **Skutki** (stan na 2026-11-11): skan BLE działa w szkicu testowym `firmware/ble_test`. W głównym firmware i po stronie PC
  odczytu `IFF:` jeszcze nie ma; na razie `integracja.py` przełącza swój/wróg klawiszem `s`. `ble_scanner.py` (`bleak`)
  zostaje tylko jako zapas dla komputera z Bluetooth. Na liście zakupów jest brelok BLE ze stałym MAC.

<a id="d-02"></a>
## D-02: Konwencja kodu i struktura folderów (2026-11-11, SM)
- **Status:** przyjęta dla nowego kodu, gdy PO zatwierdzi PR z tą konwencją; przeniesienie istniejącego kodu
  to osobny PR refaktoru.
- **Dotyczy:** cały kod Python i konfiguracja (`config.json`); działanie programu się nie zmienia.
- **Problem:** pliki generowane (`yolo11n.pt`, `smartguard.log`) trafiały do korzenia repo albo do folderu, z którego
  ktoś uruchomił program, bo ścieżki liczyły się od bieżącego katalogu. Nazwy w kodzie były mieszane PL/EN
  (`Camera`, `Detector` obok `wczytaj_config`, `Stan`).
- **Decyzja:** nazwy w kodzie po angielsku, komentarze i teksty po polsku. Logika w pakiecie `smartguard/`,
  w korzeniu tylko skrypty do uruchomienia. Pliki generowane w `models/`, `logs/`, `data/`, ścieżki od folderu projektu.
  Szczegóły: [`docs/agents/code.md`](../agents/code.md).
- **Odrzucone:**
  - układ `src/` + `pyproject.toml`: wymaga `pip install -e .` na każdym komputerze, a pakietu nie publikujemy;
  - folder `scripts/` na skrypty: uruchomiony w nim skrypt nie widzi pakietu (sprawdzone: `python scripts/x.py` →
    `ModuleNotFoundError: No module named 'smartguard'`; ten sam skrypt w korzeniu importuje pakiet, także uruchomiony z innego folderu);
  - samo ukrycie plików w edytorze: nie naprawia ścieżek.
- **Skutki:** zmiana nazw plików, funkcji i kluczy `config.json`; każdy poprawia po niej swój `config.local.json`.
  Główne moduły z [`README.md`](../../README.md) § Jak to działa mają angielskie nazwy (`capture`, `detector`, `rules`, `events`; `notifier` i `api` powstaną pod tymi
  nazwami) i je zachowują; zmieniają się `zona`, `turret_controller`, skrypty i nazwy funkcji.

<a id="d-03"></a>
## D-03: Instrukcje dla asystentów AI i podział publiczne/prywatne (2026-11-11, SM)
- **Status:** przyjęta
- **Dotyczy:** organizacja pracy zespołu i dokumentacji (repo jest publiczne).
- **Problem:** zespół może używać różnych asystentów AI (Claude Code, Copilot, Cursor, Codex). Instrukcje były tylko
  w [`CLAUDE.md`](../../CLAUDE.md), a notatki robocze z sesji AI lądowały w publicznym `docs/`.
- **Decyzja:** wejście dla wszystkich narzędzi to [`AGENTS.md`](../../AGENTS.md) z tabelą „obszar → kod → zasady → dokumenty”; zasady
  obszarów są w `docs/agents/`, a `CLAUDE.md` tylko importuje `AGENTS.md` i `AGENTS.local.md`. Prywatne: `AGENTS.local.md`
  i `notes/` (poza gitem). To, co warte pokazania, trafia do publicznego `docs/` według [`docs/agents/docs.md`](../agents/docs.md) § Gdzie co zapisać.
- **Odrzucone:** sam `AGENTS.md` bez `CLAUDE.md`. Sprawdzone w Claude Code 2.1.322: gdy w folderze leży `CLAUDE.local.md`,
  Claude Code pomija `AGENTS.md`; import w `CLAUDE.md` wczytuje oba pliki i nie zgłasza błędu, gdy `AGENTS.local.md` nie istnieje.
- **Skutki:** kto miał `CLAUDE.local.md`, przemianowuje go na `AGENTS.local.md`. Surowy zapis sesji z 2026-11-09
  wyszedł z repo; jego trwała treść jest w § D-01, `docs/project/scope.md` (pomiar ~40 ms/klatkę) i `README.md` (uruchamianie).
