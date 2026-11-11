# Jak pracujemy (ludzie i asystenci AI)

> **Kiedy czytać:** raz na wątek, przed każdym zadaniem z kodem albo dokumentami. Krótki proces dla projektu
> studenckiego: ma pomagać zrobić rzecz dobrze i ją zrozumieć, a nie dokładać biurokracji.

## Rozumiesz to, co oddajesz
Projekt jest na zaliczenie i do obrony, więc liczy się zrozumienie, nie tylko działający kod.
- **Asystent tłumaczy, nie tylko pisze:** przy każdej zmianie krótko, prostym językiem, co zrobił i dlaczego tak,
  a nie inaczej. Autor PR umie wyjaśnić swoją zmianę bez asystenta.
- **Najpierw własna próba, potem AI** jako wyjaśnienie, podpowiedź i przegląd. Badania na studentach: AI, które daje
  gotowe rozwiązania do ćwiczeń, obniżało rozumienie i oceny, a podpowiedzi po własnej próbie pomagały
  (Lehmann 2025, Bassner 2025, Kestin 2025; za opracowaniem researchu metod uczenia się z 2026-10-21) `[prawdopodobne]`.
- **Proste i standardowe zamiast sprytnego:** biblioteka standardowa i biblioteki z `requirements.txt`, zwykłe funkcje
  i klasy, czytelne nazwy. Bez własnych frameworków, warstw „na zapas”, metaklas i sztuczek, których nie omawialiśmy
  na zajęciach. Kod ma czytać student II roku.
- **Architektura jest wasza:** podział na moduły, przepływ danych, schemat bazy i protokół z ESP32 projektuje zespół.
  Asystent proponuje 2–3 warianty z kosztem i rekomendacją, tłumaczy kompromisy i pokazuje, gdzie zmiana siedzi
  w przepływie (`README.md` § Jak to działa). Wybieracie wy, asystent wdraża dopiero po wyborze, a wybór
  z uzasadnieniem trafia do `docs/project/decisions.md`. Rutynę (nazwa zmiennej, kolejność kroków) rozstrzyga sam.
- Rozmowa z asystentem po polsku.

## Z głową
- **Skala do zadania:** rozwiązanie, proces i dokumentacja proporcjonalne do zakresu. To projekt studencki trzech osób,
  nie produkt firmy: brak procedury jest lepszy niż procedura, której nikt nie potrzebuje.
- **Obiektywnie:** wniosek wynika z dowodu (kod, pomiar, źródło), nie z tego, co ktoś chce usłyszeć. Gdy propozycja
  użytkownika albo własna jest słabsza od innej, powiedz to i podaj powód.
- **Bez skrajności:** korekta kierunku jest tak duża, jak problem. Za dużo plików → scal, nie zakazuj nowych;
  za długi plik → zagęść, nie wprowadzaj licznika.
- **Nie na siłę:** nowy plik, zasada, automat albo warstwa w kodzie tylko wtedy, gdy rozwiązuje problem, który już
  wystąpił albo na pewno wystąpi; na zapas nie.

## Zanim zaczniesz
- **Drobna zmiana** (1–2 pliki, bez nowego modułu i bez zmiany kontraktu między modułami): rób od razu.
- **Duża zmiana** (nowy moduł, zmiana bazy, protokołu ESP32 albo interfejsu z `docs/project/team.md`): najpierw
  krótki plan: problem, 2–3 warianty z kosztem, polecany wariant, czego nie robimy. Po akceptacji bez kolejnych planów.
- **Pytaj, gdy różne odczytania dają istotnie inną pracę** (zakres, dane, wygląd); rutynę rozstrzygaj sam.
- Fakty bierz z kodu, dokumentów i pomiarów, nie z pamięci. Wniosek oznacz: `[zweryfikowane]`, `[prawdopodobne]`
  albo `[do weryfikacji]`.

## Gotowe = dowód
Samo „zrobione” nie wystarcza; gotowe jest to, co zostało sprawdzone.
1. Przed kodem ustal, czym sprawdzisz wynik: uruchomienie (`main.py` w trybie SIM, `demo.py` bez
   kamery), nagranie demo, test albo liczba.
2. Spisz skrajne przypadki w skali zadania (np. pusta strefa, brak kamery, brak sieci przy alercie).
3. Sprawdź na prawdziwych danych i pokaż komendę z wynikiem, nie samo „działa”.
4. Rozwiązanie ogólne, nie pod test: bez wartości wpisanych pod konkretny przypadek i bez luzowania testów.
   Test wygląda na błędny → zgłoś.
5. Czego nie sprawdzono, napisz wprost.
6. Poprawka błędu: najpierw odtwórz błąd (komenda, nagranie, test, który pada), potem napraw i pokaż, że już nie występuje.
7. Test sprawdza zachowanie widoczne dla użytkownika (zdarzenie w bazie, wysłany alert, stan maszyny), nie to, że
   funkcja została wywołana ani jak wygląda kod: test „po kodzie” przepuszcza powrót tego samego błędu.

## Bezpiecznie
- **Instalacje tylko za zgodą użytkownika:** przed `pip install`, pobraniem modelu albo Dockera napisz co, gdzie i ile
  zajmie. Nowa biblioteka: `docs/agents/code.md` § Logi i zależności.
- **Operacje niszczące tylko za zgodą:** `git reset --hard`, usuwanie plików, nadpisywanie cudzej pracy. Przed
  nadpisaniem albo usunięciem obejrzyj, co tam jest.
- Pliki robocze (zrzuty, `debug_*.py`, printy) sprzątasz przed commitem.
- Windows: PowerShell 5.1 nie zna `&&` (łącz przez `;`), a `Set-Content` bez `-Encoding utf8` psuje polskie znaki.

## Podsumowanie na koniec pracy
Krótko, w tej kolejności: **Zrobione** (co i gdzie) · **Sprawdzone** (komenda + wynik) · **Niesprawdzone** ·
**Dalej** (co zostało, co czeka na decyzję). Wniosek wart zachowania zapisz według `docs/agents/docs.md` § Gdzie co zapisać;
gdy użytkownik prosił o zapisanie czegoś, dopisz: „prośba → `plik` § sekcja” albo dlaczego nie zapisano.
