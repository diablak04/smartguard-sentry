# Research i zapisy sesji

> **Kiedy czytać:** zanim zaczniesz research (także „deep research” w asystencie AI), zanim zaproponujesz temat,
> który mógł być już rozważany, i gdy kończysz sesję z wnioskami wartymi zachowania. Log przebiegów: `docs/research/README.md`.

## Kiedy research, a kiedy pomiar
- **Research** tylko wtedy, gdy błąd jest drogi albo trudny do cofnięcia: zakup sprzętu, bezpieczeństwo (BHP wieżyczki,
  zasilanie), dane osobowe i RODO (zdjęcia ludzi), prawo, wybór, którego zmiana przepisuje dużo kodu.
- **Pomiar albo test** zamiast researchu, gdy decyzję łatwo zmienić: taniej sprawdzić na kodzie i poprawić
  (np. czas detekcji, układ folderów; zob. `docs/project/decisions.md` § D-02 (konwencja kodu) i § D-03 (instrukcje dla AI)).
- Najpierw przejrzyj `docs/research/README.md` i `docs/project/decisions.md`: rozszerz istniejący przebieg, nie rób go od nowa.

## Jak robić
1. Zacznij od decyzji: wypisz 2–5 decyzji, które wynik może zmienić, i co zrobisz przy każdej odpowiedzi.
   Pytanie, przy którym każda odpowiedź prowadzi do tego samego działania, skreśl.
2. Źródła pierwotne (dokumentacja producenta, karta katalogowa, przepis, pomiar), z datą i krótkim dosłownym cytatem.
   Liczba bez źródła się nie liczy. Przy każdym fakcie tag: `[zweryfikowane]`, `[prawdopodobne]` albo `[do weryfikacji]`.
3. Dla każdego mocnego wniosku jedno konkretne wyszukanie dowodu przeciwnego; zapisz wynik albo „nie znaleziono”.
4. Werdykt w formie „rób Y, bo Z; nie X”.

## Gdzie co trafia
Miejsca: `docs/agents/docs.md` § Gdzie co zapisać. Tu tylko to, co dotyczy samego researchu:
- Surowy materiał (raport, zrzut rozmowy z AI) → `notes/research/`, prywatnie.
- Każdy przebieg = jeden wiersz w `docs/research/README.md`, najnowszy na górze.
- Opracowanie `docs/research/RRRR-MM-DD-<temat>.md` tylko wtedy, gdy werdykt potrzebuje uzasadnienia dłuższego niż
  wiersz logu: pytanie, tabela źródeł (fakt + tag), werdykt, odrzucone warianty, pytania otwarte.
- Decyzja z researchu → wpis w `docs/project/decisions.md`, który odwołuje się do wiersza logu.

Repo jest publiczne: w opracowaniu nie ma imion, nazwisk, ścieżek z nazwą użytkownika ani danych z prywatnych źródeł.
Fakty zmienne (ceny, dostępność, wersje, przepisy) mają datę; przed użyciem sprawdź, czy są aktualne.

## Zapis sesji z asystentem AI
- Sesja, z której nic trwałego nie wynika, nie zostawia śladu w repo.
- Surowy zapis (jeśli chcesz go mieć) → `notes/sesje/` (prywatne).
- Co trwałe, przepisz krótko według `docs/agents/docs.md` § Gdzie co zapisać. Kontekst na następną sesję daje repo,
  nie stary zapis rozmowy.
