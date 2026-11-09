"""Orkiestrator SmartGuard + maszyna stanow (szkielet Fazy 0).

Na tym etapie main.py:
  - wczytuje config.json,
  - uruchamia logging (konsola + plik),
  - trzyma maszyne stanow i stoi w IDLE,
  - loguje kilka tickow i konczy (moduly F1+ jeszcze niepodpiete).

Realne moduly (kamera, YOLO, strefa, IFF, wiezyczka) dochodza w kolejnych fazach.
"""
import json
import logging
import time
from enum import Enum, auto
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"


class Stan(Enum):
    """Stany maszyny (zgodne z karta projektu)."""
    IDLE = auto()        # czuwanie, strefa pusta
    PATROL = auto()      # ruch wahadlowy w poszukiwaniu celow (F10)
    DETECTED = auto()    # YOLO wykrylo czlowieka (F1)
    CONFIRMING = auto()  # potwierdzanie na 3 klatkach (F2)
    FRIENDLY = auto()    # IFF: SWOJ -> blokada ognia (F2)
    FOE = auto()         # IFF: WROG -> eskalacja (F2)
    ENGAGE = auto()      # celowanie + strzal (F5)
    COOLDOWN = auto()    # przerwa po strzale (max 1 alert / 60 s)


# Dozwolone przejscia: z_stanu -> [mozliwe_nastepne]
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
    """Logi jednoczesnie na konsole i do pliku smartguard.log."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("smartguard.log", encoding="utf-8"),
        ],
    )


class SmartGuard:
    def __init__(self, config: dict):
        self.config = config
        self.stan = Stan.IDLE
        self.muted = False  # nakladka MUTED (wyciszenie z Telegrama, F8)
        self.log = logging.getLogger("smartguard")

    def przejdz(self, nowy: Stan) -> bool:
        """Zmiana stanu zgodnie z tabela przejsc (chroni przed bledna logika)."""
        if nowy in PRZEJSCIA[self.stan]:
            self.log.info("Stan: %s -> %s", self.stan.name, nowy.name)
            self.stan = nowy
            return True
        self.log.warning("Niedozwolone przejscie: %s -> %s", self.stan.name, nowy.name)
        return False

    def w_godzinach_czuwania(self) -> bool:
        """Nakladka ARMED_HOURS. Szkielet: zawsze True.

        TODO (F10): porownaj biezaca godzine z config['godziny_czuwania'].
        """
        return True

    def tick(self) -> None:
        """Jeden obieg glownej petli. W szkielecie F0 tylko loguje.

        TODO F1: capture.py -> detector.py (YOLO)
        TODO F2: rules.py (strefa + 3 klatki + IFF) -> wyznacz nastepny stan
        TODO F5: turret_controller.py (celowanie + strzal)
        """
        self.log.info(
            "tick | stan=%s | muted=%s | czuwanie=%s",
            self.stan.name, self.muted, self.w_godzinach_czuwania(),
        )

    def run(self, max_tick: int = 3, interwal: float = 1.0) -> None:
        self.log.info("SmartGuard start. Wczytano config: %s", list(self.config.keys()))
        self.log.info("Maszyna stanow w stanie poczatkowym: %s", self.stan.name)
        for _ in range(max_tick):
            self.tick()
            time.sleep(interwal)
        self.log.info("Szkielet F0 OK — moduly (F1+) jeszcze niepodpiete. Koniec.")


def main() -> None:
    konfiguruj_logging()
    config = wczytaj_config()
    SmartGuard(config).run()


if __name__ == "__main__":
    main()
