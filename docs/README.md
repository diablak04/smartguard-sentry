# Dokumentacja: co gdzie jest

Każdy dokument ma jedno miejsce, bez kopii. Nowy plik trafia do jednego z folderów niżej, nie luzem do `docs/`.
Nazwy folderów i plików są po angielsku, treść po polsku.

Dokumentacja projektu na zaliczenie obejmuje wszystko, od wymagań po wdrożenie: wymagania, przypadki
użycia, diagramy UML, model danych, testy. Składamy ją na bieżąco, po kawałku przy każdej zmianie, a nie w styczniu.

| Folder | Dla kogo | Co tam jest |
|---|---|---|
| [`project/`](./project/) | zespół, prowadząca | zakres i stan prac, decyzje, podział pracy |
| `design/` | zespół, prowadząca | dokumentacja techniczna zgodna z kodem: architektura, model danych, diagramy UML, testy (folder powstaje przy pierwszym pliku) |
| [`agents/`](./agents/) | zespół i asystenci AI | zasady pracy: proces, kod, sprzęt Sentry, Git, research, dokumenty |
| [`research/`](./research/) | zespół, prowadząca | log researchu i testów z werdyktami; opracowania `RRRR-MM-DD-<temat>.md` |
| `archive/` | nikt na co dzień | zamknięte dokumenty, tylko historia, nie edytujemy (folder powstaje przy pierwszym pliku) |

Zatwierdzone Karta Projektu i Scenariusze przypadków użycia to PDF-y poza repo (nie edytujemy). Ich streszczenie
dla zespołu jest w [`docs/project/scope.md`](project/scope.md). Wejście dla asystentów AI i tabela „przed zmianą w pliku X przeczytaj Y”: [`AGENTS.md`](../AGENTS.md).

## `project/`

| Plik | Kiedy otwierasz |
|---|---|
| [`scope.md`](./project/scope.md) | Co budujemy (UC-01–04, UC-07), stan każdego wymagania, pomiary, odstępstwa od karty. **Od tego zacznij** |
| [`decisions.md`](./project/decisions.md) | Czemu tak, a nie inaczej: decyzje techniczne z uzasadnieniem i odrzuconymi wariantami |
| [`team.md`](./project/team.md) | Role, kto robi który przypadek użycia, co kto komu przekazuje, Kanban, Definicja Ukończenia |

## Dokumentacja na oddanie (`design/`)

**Repo = treść, plik na Moodle = złożenie.** Teksty i diagramy powstają tutaj, razem z kodem, którego dotyczą,
bez imion i nazwisk. Plik oddawany na Moodle (jeden na zespół) zawiera skład zespołu, więc składamy go **poza repo**
z treści stąd i z zatwierdzonej karty. Do repo nie trafia ani ten plik, ani jego eksport.

Diagram = źródło `.drawio` + eksport `.png` obok, ta sama nazwa (np. `diagrams/use-case.drawio` + `use-case.png`).

| Element dokumentacji | Plik w `design/` | Powstaje razem z |
|---|---|---|
| Wymagania funkcjonalne i niefunkcjonalne | — (karta, PDF poza repo; stan w `project/scope.md`) | zatwierdzone |
| Diagram wymagań | `diagrams/requirements` | wymaganiami z karty |
| Diagram przypadków użycia + scenariusze | `diagrams/use-case` (scenariusze: PDF poza repo) | zatwierdzone |
| Diagram czynności | `diagrams/activity` | przepływem UC-01 → UC-02 (detekcja → zapis → alert) |
| Model danych (ERD) + opis tabel i statusów | `diagrams/erd`, `data-model.md` | `events.py` (SQLite) |
| Diagram klas | `diagrams/class` | modułami Pythona po refaktorze ([`docs/project/decisions.md` § D-02](project/decisions.md#d-02) (konwencja kodu)) |
| Diagram sekwencji | `diagrams/sequence` | spięciem modułów w `main.py` |
| Diagram stanów | `diagrams/state` | maszyną stanów (`State` / `Stan` w `main.py`) |
| Diagram wdrożenia | `diagrams/deployment` | uruchomieniem: PC, kamera, ESP32, Telegram, n8n w Dockerze |
| Architektura: moduły, przepływ, protokół PC ↔ ESP32 | `architecture.md` | spięciem modułów |
| Testy: przypadki testowe do wymagań, nagranie demo, wyniki | `testing.md` | testami (DEV) |

Lista elementów pochodzi z planu przedmiotu na Moodle (wymagania, UML, ERD, testowanie). Plik dodajesz wtedy,
gdy jego treść jest gotowa, a nie jako pusty szablon.

## `agents/`

| Plik | Kiedy |
|---|---|
| [`workflow.md`](./agents/workflow.md) | raz na wątek, przed każdym zadaniem: zrozumienie, gotowe = dowód, bezpieczeństwo, podsumowanie |
| [`code.md`](./agents/code.md) | przed zmianą w kodzie Python: nazwy, struktura, ścieżki, konfiguracja |
| [`hardware.md`](./agents/hardware.md) | przed pracą przy wieżyczce, ESP32, okablowaniu: złote zasady, protokół, BOM |
| [`git.md`](./agents/git.md) | przed commitem, PR, issue: zasady Git i danych osobowych |
| [`research.md`](./agents/research.md) | przed researchem i po sesji z AI: kiedy research, jak, co publiczne, co prywatne |
| [`docs.md`](./agents/docs.md) | przed dopisaniem do `AGENTS.md`, [`README.md`](../README.md), `docs/**`: gdzie co zapisać, czego nie dodajemy, nazwy plików |
