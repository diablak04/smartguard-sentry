# Dokumenty i notatki: co, gdzie, jak pisać

> **Kiedy czytać:** zanim dopiszesz albo zmienisz coś w `AGENTS.md`, `README.md`, `docs/**`, i zanim przeniesiesz
> coś z prywatnych `notes/` do repo. Cel: mało plików, każdy potrzebny, bez powtórzeń i bez slopu.

## Gdzie co zapisać

Jedyna tabela tego typu w repo. Jedna rzecz = jedno miejsce; gdzie indziej tylko odnośnik.

| Co | Gdzie |
|---|---|
| Decyzja techniczna w ramach karty (wybór technologii, podejścia, układu) | `docs/project/decisions.md`, nowy wpis D-xx |
| Odstępstwo od karty, stan wymagania, pomiar (np. czas detekcji) | `docs/project/scope.md` |
| Kto robi który przypadek użycia, interfejs między modułami | `docs/project/team.md` |
| Zasada: sposób pracy, weryfikacja, praca z asystentem AI | `docs/agents/workflow.md` |
| Zasada: nazwy, struktura, ścieżki, konfiguracja, styl kodu Python | `docs/agents/code.md` |
| Zasada: sprzęt, okablowanie, firmware, protokół PC ↔ ESP32 | `docs/agents/hardware.md` |
| Zasada: Git, PR, issue, dane osobowe w historii | `docs/agents/git.md` |
| Zasada: dokumenty, notatki, nazwy plików `.md` | ten plik |
| Zasady nowego obszaru (panel WWW, Telegram, testy), gdy jest ich więcej niż kilka linii | nowy `docs/agents/<obszar>.md` + wiersz w tabeli `AGENTS.md` § Zanim zaczniesz + wiersz w `docs/README.md` |
| Architektura, model danych (ERD), diagram UML, plan i wyniki testów | `docs/design/` według `docs/README.md` § Dokumentacja na oddanie |
| Research ze źródłami i werdyktem | wiersz w `docs/research/README.md` (+ opracowanie, decyzja), według `docs/agents/research.md` |
| Zamknięty dokument wart zachowania (stary plan, usunięty mechanizm) | `docs/archive/<temat>.md` z nagłówkiem „Archiwum, nie edytować” |
| Bieżące zadanie, plan na najbliższe dni, pomysł na później | Kanban |
| Zapis sesji z AI, surowy raport, szkic | `notes/` (prywatne); to, co trwałe, przepisz krótko wyżej |

## Czego nie dodajemy do repo
- Surowych zapisów rozmów z AI, raportów przeklejonych 1:1, wklejek. Do repo idzie krótki wniosek, surowiec do `notes/`.
- Opisu tego, co widać w kodzie (funkcja po funkcji prozą). Kod czyta się szybciej niż jego streszczenie.
- List zadań, harmonogramów z datami, „TODO na później”: to jest Kanban.
- Drugiej kopii tej samej wiedzy: zamiast kopii odwołanie według § Odwołania.
- Pustych szablonów i plików „na przyszłość”: plik powstaje, gdy ma gotową treść.
- Liczb wpisanych ręcznie, które się zdezaktualizują (liczba plików, linii, testów). Pomiar tylko z datą i sposobem pomiaru.
- Historii „jak było wcześniej” w zasadach: zasada opisuje stan obecny i powód; historia jest w gicie i w statusach `docs/project/decisions.md`.
- Kopii zapasowych (`*_old.py`, `kopia`, `v2`, `final`): od tego jest git.
- Danych osobowych, sekretów, zdjęć i nagrań z ludźmi, dużych plików binarnych (modele, nagrania): `AGENTS.md` § Repo jest publiczne.

## Zanim dopiszesz
1. Grep w `docs/` i `AGENTS.md`: już jest → popraw w miejscu, bez „v2” i bez drugiej sekcji obok.
2. Najpierw skreśl albo scal, potem dopisz. Usuwasz tylko kopie, nigdy jedynej wersji wiedzy.
3. Zmiana faktu, nazwy albo układu = poprawka we wszystkich miejscach w tym samym commicie. Grep nie tylko po starej
   nazwie, ale też po zdaniach opisujących stary układ („zasady są w …”, „plik X robi …”): po przeniesieniu
   to one zostają i przeczą nowemu stanowi.

## Jak pisać
- Zapisuj tylko to, czego nie widać w kodzie: decyzje, pułapki, sprzęt, proces, niestandardowe praktyki. Opisy repo
  i oczywistości nie poprawiają pracy asystenta, a kosztują go czytanie każdej sesji `[prawdopodobne]`.
- Wpis = co robić + dlaczego (jedno zdanie) + gdzie (plik, symbol, §). Fakt przed uzasadnieniem, jedna myśl na akapit
  albo wiersz tabeli. Stan obecny i powód, nie przebieg rozmowy.
- Normalnym tonem, bez wielkich liter i wykrzykników: nadmiar nacisku sprawia, że model stosuje zasadę za szeroko.
- Emoji oszczędnie, tylko gdy niesie znaczenie, np. jedno ⚠️ przy ostrzeżeniu BHP. Nie jako ozdobnik nagłówków
  ani zamiast słów w tabelach: stan piszemy słowami (jest / częściowo / brak), bo słowo znajdzie Grep.
- Zmiana zdania = zastąpienie, nie dopisek obok: popraw wszystkie miejsca, a w `docs/project/decisions.md` dopisz nowy wpis
  i ustaw staremu status „zastąpiona przez D-xx”. Przy sprzecznych instrukcjach model wybiera jedną losowo.

## Plik dla dwóch czytelników (człowiek i asystent AI)
- Pierwsze linie mówią, czym plik jest i kiedy go otworzyć, słowami zrozumiałymi bez innego pliku.
- Odwołanie według § Odwołania: zawsze ścieżka i początek nagłówka, przy decyzji także krótka nazwa.
- Skrót rozwinięty przy pierwszym użyciu w pliku: przypadek użycia (UC), swój/wróg (IFF), Product Owner (PO).
- Pliki w `docs/project/` mówią prostym językiem o stanie i decyzjach; pliki w `docs/agents/` używają nazw z kodu.

## Odwołania (jeden format wszędzie)
Kilka formatów naraz (linki, kotwice `#`, gołe kody, „sekcja »X«”) sprawia, że odwołań nie znajdziesz jednym Grepem,
a część psuje się po cichu przy zmianie nagłówka. Dlatego jeden zapis, także w `README.md`, szablonie PR i komentarzach w kodzie:
- Do innego pliku: `ścieżka/od/korzenia.md` § Początek nagłówka, np. `docs/project/scope.md` § UC-02.
  Pełna ścieżka zawsze, nawet gdy nazwa pliku jest unikalna.
- W obrębie tego samego pliku: samo § Początek nagłówka.
- Do decyzji: `docs/project/decisions.md` § D-02 (konwencja kodu): numer i krótka nazwa w nawiasie, nigdy sam „D-02”.
- Do dokumentu spoza repo: nazwa słowami i jego numer sekcji, np. karta § 12.1.
- § = dosłowny początek nagłówka z pliku. Zmieniasz nagłówek → Grep po starym i popraw odwołania w tym samym commicie.
- Odwołanie możesz owinąć w link, żeby dało się kliknąć na GitHubie; widoczny tekst zostaje ten sam:
  [`docs/project/scope.md`](../project/scope.md) § UC-02. Ścieżka linku względna od pliku, w którym stoi.
  Linkuj tam, gdzie czyta człowiek (`README.md`, `docs/README.md`, `docs/project/`, `docs/research/`); w plikach dla
  asystentów (`AGENTS.md`, `docs/agents/`) wystarczy tekst.
- Kierunek: plik prywatny (`AGENTS.local.md`, `notes/`) może wskazywać publiczny, odwrotnie nie. Publiczny plik
  nie linkuje prywatnego, bo na GitHubie tego pliku nie ma; może go tylko nazwać jako pojęcie („twój `AGENTS.local.md`”).
- Bez łańcuchów: odwołanie prowadzi tam, gdzie wiedza jest, nie do pliku, który tylko odsyła dalej. Same odnośniki
  mają tylko mapy (`AGENTS.md`, `docs/README.md`, `CLAUDE.md` z importami). Przenosisz wiedzę → popraw odwołania
  na nowe miejsce, zamiast zostawiać w starym „patrz tam”.
- Kotwica `#` tylko do decyzji (`decisions.md#d-02`), bo mają stałe `<a id="d-02"></a>`. Kotwice wyliczane przez
  GitHub z treści nagłówka pękają przy każdej zmianie tytułu, więc do innych sekcji linkuj sam plik, a sekcję podaj po §.

## Nazwy plików `.md`
- Angielski kebab-case, krótki rzeczownik mówiący, czego plik dotyczy: `code.md`, `hardware.md`, `scope.md`,
  nie `sentry-hardware-rules-v2.md`. Treść po polsku.
- `README.md` tylko jako mapa folderu (GitHub wyświetla go sam przy wejściu do folderu).
- Data w nazwie tylko w researchu i notatkach sesji: `RRRR-MM-DD-<temat>.md`.
- Nowy plik tylko dla odrębnego tematu; dziel plik, gdy czytelnik obszaru nie potrzebuje reszty, scalaj, gdy pliki
  tylko się powtarzają.

## Rozmiar: budżet, nie zapadka
Dokumenty same z siebie tylko rosną, a jednorazowe sprzątanie nie trzyma. Pomaga rozsądny budżet, nie sztywne liczniki:
- `AGENTS.md` ładuje się w każdej sesji, więc zostaje mały (ok. 10 KB): tylko to, co potrzebne zawsze, i mapa.
- Pozostałe pliki nie mają limitu linii. Sygnał do zagęszczenia: plik nie da się przeczytać za jednym razem, powtarza
  inny plik albo opisuje to, co widać w kodzie. Wtedy najpierw skreślasz i scalasz, dopiero potem dopisujesz.
- Nowy plik, gdy temat jest odrębny i czytelnik obszaru nie potrzebuje reszty; inaczej sekcja w istniejącym pliku.
- Nie robimy zapadki „plik może tylko maleć” ani liczników: karałyby dopisanie prawdziwej pułapki. Automat
  (test, skrypt, punkt w szablonie PR) dodajemy dopiero wtedy, gdy ten sam błąd wróci, nie na zapas.

## Gdy zasada nie działa
- Zasada dla zespołu żyje w repo (`AGENTS.md`, `docs/`), nie w `AGENTS.local.md` ani w pamięci asystenta: inne osoby
  i inne narzędzia jej nie zobaczą.
- Prośba „zapisz / zawsze / na przyszłość”: najpierw Grep. Wpis jest → popraw go; nowy tylko przy zerze trafień.
  Skala wpisu = skala uwagi: uwaga o jednym module to linia w jego pliku zasad, nie nowa zasada ogólna.
- Ten sam temat wraca w kolejnej sesji = błąd procesu, nie powód do drugiego wpisu. Nazwij przyczynę (brak wpisu,
  plik nieczytany, zasada za ogólna albo sprzeczna) i popraw ją.
- Zasada łamana drugi raz mimo zapisu → nie pogrubienie, tylko automat: punkt w szablonie PR
  (`.github/pull_request_template.md`), test albo sprawdzenie skryptem. Wcześniej nie: automat na zapas to też rozrost.
- Słowa typu „z głową”, „bez slopu” opisują styl pracy z `docs/agents/workflow.md` § Z głową; nie robi się z nich nowych zasad.
