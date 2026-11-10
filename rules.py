"""Reguly decyzyjne SmartGuard: potwierdzanie detekcji + klasyfikacja swoj/wrog.

Oddziela 'surowe' wejscia (czy ktos jest w strefie, czy widac 'swojego' po BLE)
od decyzji maszyny stanow. Dzieki temu logike mozna testowac bez kamery i sprzetu.
"""
from dataclasses import dataclass


@dataclass
class Potwierdzanie:
    """Anty-falszywy-alarm: cel liczy sie dopiero po N kolejnych klatkach w strefie.

    Jedna zgubiona klatka (cel poza strefa / brak detekcji) zeruje licznik —
    chroni przed pojedynczymi bledami YOLO.
    """
    wymagane: int = 3
    licznik: int = 0

    def aktualizuj(self, cel_w_strefie: bool) -> bool:
        """Zwraca True, gdy cel potwierdzony (>= 'wymagane' kolejnych klatek)."""
        self.licznik = self.licznik + 1 if cel_w_strefie else 0
        return self.licznik >= self.wymagane

    def reset(self) -> None:
        self.licznik = 0


def klasyfikuj_iff(iff_swoj: bool) -> str:
    """'FRIENDLY' gdy w poblizu jest 'swoj' (brelok BLE), inaczej 'FOE'."""
    return "FRIENDLY" if iff_swoj else "FOE"
