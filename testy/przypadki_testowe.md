# Przypadki testowe – SmartGuard

Przypadki do sprawdzenia bez sprzętu: wystarczy instalacja z [`README.md`](../README.md) § Uruchomienie.
Testy 2–4 podają wejścia wprost do funkcji z `smartguard/`, bez kamery.

Wyniki z 2026-11-24 dotyczą tej logiki. Kamery, modelu YOLO i wieżyczki te testy nie obejmują.

## Test 1 – potwierdzenie intruza
Cel: sprawdzenie, czy obcy w strefie jest potwierdzany po 3 klatkach i czy system reaguje raz.
Dane wejściowe: `python main.py demo` (scenariusz: pusta strefa, 6 kroków z obcym w strefie, pusta strefa).
Oczekiwany wynik: linia „Potwierdzony po 3 klatkach -> FOE”, jeden strzał 200 ms, powrót do stanu IDLE, na końcu „Koniec scenariusza.”.
Wynik: zgodny.

## Test 2 – chwilowe wykrycie
Cel: sprawdzenie, czy wykrycie krótsze niż 3 klatki nie wywołuje reakcji (fałszywy alarm).
Dane wejściowe: `SmartGuard.step()`: 3 kroki z obcym w strefie (wykrycie, start potwierdzania, 1 klatka potwierdzenia), potem pusta strefa.
Oczekiwany wynik: przejście CONFIRMING -> IDLE, brak strzału.
Wynik: zgodny.

## Test 3 – domownik w strefie
Cel: sprawdzenie, czy osoba rozpoznana jako „swój” nie jest celem.
Dane wejściowe: `SmartGuard.step()`: 6 kroków z osobą w strefie i znacznikiem „swój”.
Oczekiwany wynik: stan FRIENDLY, log „SWOJ w strefie -> BLOKADA OGNIA”, brak strzału.
Wynik: zgodny.

## Test 4 – osoba poza strefą
Cel: sprawdzenie, czy o wejściu do strefy decyduje punkt stóp, a nie cała ramka.
Dane wejściowe: `point_in_zone()`, obraz 640×480, strefa = prawa połowa; ramka A od x=300 do x=330 (nachodzi na strefę, środek dołu przed nią), ramka B od x=400 do x=500.
Oczekiwany wynik: A poza strefą, B w strefie.
Wynik: zgodny.

## Test 5 – sytuacja błędna: uszkodzona konfiguracja
Cel: sprawdzenie reakcji aplikacji na niepoprawne dane.
Dane wejściowe: `config.local.json` z brakującą wartością, np. `"confirm_frames":` bez liczby.
Oczekiwany wynik: program nie startuje i podaje nazwę pliku oraz linię, np. „Blad w pliku config.local.json (linia 3)”.
Wynik: zgodny.
