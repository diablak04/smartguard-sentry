"""Reguly decyzyjne SmartGuard: potwierdzanie detekcji + klasyfikacja swoj/wrog.

Oddziela 'surowe' wejscia (czy ktos jest w strefie, czy widac 'swojego' po BLE)
od decyzji maszyny stanow. Dzieki temu logike mozna testowac bez kamery i sprzetu.
"""
from dataclasses import dataclass


@dataclass
class FrameConfirmation:
    """Anty-falszywy-alarm: cel liczy sie dopiero po N kolejnych klatkach w strefie.

    Jedna zgubiona klatka (cel poza strefa / brak detekcji) zeruje licznik —
    chroni przed pojedynczymi bledami YOLO.
    """
    required: int = 3
    count: int = 0

    def update(self, target_in_zone: bool) -> bool:
        """Zwraca True, gdy cel potwierdzony (>= 'required' kolejnych klatek)."""
        self.count = self.count + 1 if target_in_zone else 0
        return self.count >= self.required

    def reset(self) -> None:
        self.count = 0


def classify_iff(iff_friend: bool) -> str:
    """'FRIENDLY' gdy w poblizu jest 'swoj' (brelok BLE), inaczej 'FOE'."""
    return "FRIENDLY" if iff_friend else "FOE"
