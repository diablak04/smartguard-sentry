"""Orkiestrator SmartGuard + maszyna stanow.

Faza 0: szkielet maszyny stanow + logging.
Faza 2: potwierdzanie detekcji na N klatkach (anty-falszywka) + klasyfikacja swoj/wrog.

Maszyna sterowana percepcja: krok(cel_w_strefie, iff_swoj) wykonuje JEDNO przejscie.
Realne wejscia (kamera -> YOLO -> strefa -> IFF BLE) podepniemy w integracji (Faza 6);
tu run() odgrywa scenariusz, zeby pokazac dzialanie bez sprzetu.
"""
import json
import logging
from enum import Enum, auto
from pathlib import Path

from rules import Potwierdzanie, klasyfikuj_iff

CONFIG_PATH = Path(__file__).parent / "config.json"


class Stan(Enum):
    IDLE = auto()        # czuwanie, strefa pusta
    PATROL = auto()      # ruch wahadlowy (F10)
    DETECTED = auto()    # YOLO wykrylo czlowieka w strefie
    CONFIRMING = auto()  # potwierdzanie na N klatkach
    FRIENDLY = auto()    # IFF: SWOJ -> blokada ognia
    FOE = auto()         # IFF: WROG -> eskalacja
    ENGAGE = auto()      # celowanie + strzal
    COOLDOWN = auto()    # przerwa po strzale


PRZEJSCIA = {
    Stan.IDLE:       [Stan.PATROL, Stan.DETECTED],
    Stan.PATROL:     [Stan.DETECTED, Stan.IDLE],
    Stan.DETECTED:   [Stan.CONFIRMING, Stan.IDLE],
    Stan.CONFIRMING: [Stan.FRIENDLY, Stan.FOE, Stan.IDLE],
    Stan.FRIENDLY:   [Stan.IDLE],
    Stan.FOE:        [Stan.ENGAGE],
    Stan.ENGAGE:     [Stan.COOLDOWN],
    Stan.COOLDOWN:   [Stan.IDLE, Stan.PATROL],
}


def wczytaj_config(path: Path = CONFIG_PATH) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def konfiguruj_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.StreamHandler(),
                  logging.FileHandler("smartguard.log", encoding="utf-8")],
    )


class SmartGuard:
    def __init__(self, config: dict, cooldown_ticks: int = 3):
        self.config = config
        self.stan = Stan.IDLE
        self.muted = False
        self.fire_ms = config.get("fire_ms", 200)
        self.potw = Potwierdzanie(wymagane=config.get("potwierdzenie_klatek", 3))
        # W realu cooldown to czas (config['cooldown_s']); w szkielecie liczymy w tickach.
        self.cooldown_ticks = cooldown_ticks
        self._cooldown = 0
        self.log = logging.getLogger("smartguard")

    def _przejdz(self, nowy: Stan) -> None:
        if nowy in PRZEJSCIA[self.stan]:
            self.log.info("Stan: %s -> %s", self.stan.name, nowy.name)
            self.stan = nowy
        else:
            self.log.warning("Niedozwolone przejscie: %s -> %s", self.stan.name, nowy.name)

    def krok(self, cel_w_strefie: bool, iff_swoj: bool):
        """Jedno przejscie maszyny na podstawie percepcji. Zwraca akcje albo None."""
        akcja = None
        st = self.stan

        if st == Stan.IDLE:
            if cel_w_strefie:
                self._przejdz(Stan.DETECTED)

        elif st == Stan.DETECTED:
            self.potw.reset()
            self._przejdz(Stan.CONFIRMING)

        elif st == Stan.CONFIRMING:
            if not cel_w_strefie:
                self._przejdz(Stan.IDLE)                      # cel zniknal = falszywy alarm
            elif self.potw.aktualizuj(True):
                docelowy = klasyfikuj_iff(iff_swoj)
                self.log.info("Potwierdzony po %d klatkach -> %s", self.potw.wymagane, docelowy)
                self._przejdz(Stan.FRIENDLY if docelowy == "FRIENDLY" else Stan.FOE)

        elif st == Stan.FRIENDLY:
            self.log.info("SWOJ w strefie -> BLOKADA OGNIA")
            self._przejdz(Stan.IDLE)

        elif st == Stan.FOE:
            self._przejdz(Stan.ENGAGE)

        elif st == Stan.ENGAGE:
            if self.muted:
                self.log.warning("ENGAGE, ale MUTED -> bez strzalu")
            else:
                self.log.warning("STRZAL %d ms (cel: korpus, nie glowa)", self.fire_ms)
                akcja = ("FIRE", self.fire_ms)
            self._cooldown = self.cooldown_ticks
            self._przejdz(Stan.COOLDOWN)

        elif st == Stan.COOLDOWN:
            self._cooldown -= 1
            if self._cooldown <= 0:
                self._przejdz(Stan.IDLE)

        return akcja

    def run_scenariusz(self, scenariusz) -> None:
        """Odgrywa liste (cel_w_strefie, iff_swoj) — demonstracja bez sprzetu."""
        self.log.info("SmartGuard start. Stan poczatkowy: %s", self.stan.name)
        for i, (cel, swoj) in enumerate(scenariusz, 1):
            akcja = self.krok(cel, swoj)
            self.log.info("  [t%02d] cel=%s swoj=%s | stan=%s%s",
                          i, int(cel), int(swoj), self.stan.name,
                          f" | AKCJA={akcja}" if akcja else "")
        self.log.info("Koniec scenariusza.")


def main() -> None:
    konfiguruj_logging()
    config = wczytaj_config()
    sg = SmartGuard(config)
    # Demo: intruz (WROG) wchodzi w strefe i zostaje w niej kilka klatek.
    scenariusz = [(False, False)] + [(True, False)] * 6 + [(False, False)] * 4
    sg.run_scenariusz(scenariusz)


if __name__ == "__main__":
    main()
