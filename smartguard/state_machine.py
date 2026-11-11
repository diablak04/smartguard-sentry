"""Maszyna stanow SmartGuard.

Maszyna sterowana percepcja: step(target_in_zone, iff_friend) wykonuje JEDNO przejscie.
Realne wejscia (kamera -> YOLO -> strefa -> IFF) podaje main.py; demo.py odgrywa
scenariusz, zeby pokazac dzialanie bez kamery i sprzetu.
"""
import logging
from enum import Enum, auto

from smartguard.rules import FrameConfirmation, classify_iff


class State(Enum):
    IDLE = auto()        # czuwanie, strefa pusta
    PATROL = auto()      # ruch wahadlowy (F10)
    DETECTED = auto()    # YOLO wykrylo czlowieka w strefie
    CONFIRMING = auto()  # potwierdzanie na N klatkach
    FRIENDLY = auto()    # IFF: SWOJ -> blokada ognia
    FOE = auto()         # IFF: WROG -> eskalacja
    ENGAGE = auto()      # celowanie + strzal
    COOLDOWN = auto()    # przerwa po strzale


TRANSITIONS = {
    State.IDLE:       [State.PATROL, State.DETECTED],
    State.PATROL:     [State.DETECTED, State.IDLE],
    State.DETECTED:   [State.CONFIRMING, State.IDLE],
    State.CONFIRMING: [State.FRIENDLY, State.FOE, State.IDLE],
    State.FRIENDLY:   [State.IDLE],
    State.FOE:        [State.ENGAGE],
    State.ENGAGE:     [State.COOLDOWN],
    State.COOLDOWN:   [State.IDLE, State.PATROL],
}


def setup_logging() -> None:
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
        self.state = State.IDLE
        self.muted = False
        self.fire_ms = config.get("fire_ms", 200)
        self.confirmation = FrameConfirmation(required=config.get("potwierdzenie_klatek", 3))
        # W realu cooldown to czas (config['cooldown_s']); w szkielecie liczymy w tickach.
        self.cooldown_ticks = cooldown_ticks
        self._cooldown = 0
        self.log = logging.getLogger("smartguard")

    def _transition(self, new: State) -> None:
        if new in TRANSITIONS[self.state]:
            self.log.info("Stan: %s -> %s", self.state.name, new.name)
            self.state = new
        else:
            self.log.warning("Niedozwolone przejscie: %s -> %s", self.state.name, new.name)

    def step(self, target_in_zone: bool, iff_friend: bool):
        """Jedno przejscie maszyny na podstawie percepcji. Zwraca akcje albo None."""
        action = None
        st = self.state

        if st == State.IDLE:
            if target_in_zone:
                self._transition(State.DETECTED)

        elif st == State.DETECTED:
            self.confirmation.reset()
            self._transition(State.CONFIRMING)

        elif st == State.CONFIRMING:
            if not target_in_zone:
                self._transition(State.IDLE)                  # cel zniknal = falszywy alarm
            elif self.confirmation.update(True):
                target = classify_iff(iff_friend)
                self.log.info("Potwierdzony po %d klatkach -> %s", self.confirmation.required, target)
                self._transition(State.FRIENDLY if target == "FRIENDLY" else State.FOE)

        elif st == State.FRIENDLY:
            self.log.info("SWOJ w strefie -> BLOKADA OGNIA")
            self._transition(State.IDLE)

        elif st == State.FOE:
            self._transition(State.ENGAGE)

        elif st == State.ENGAGE:
            if self.muted:
                self.log.warning("ENGAGE, ale MUTED -> bez strzalu")
            else:
                self.log.warning("STRZAL %d ms (cel: korpus, nie glowa)", self.fire_ms)
                action = ("FIRE", self.fire_ms)
            self._cooldown = self.cooldown_ticks
            self._transition(State.COOLDOWN)

        elif st == State.COOLDOWN:
            self._cooldown -= 1
            if self._cooldown <= 0:
                self._transition(State.IDLE)

        return action

    def run_scenario(self, scenario) -> None:
        """Odgrywa liste (target_in_zone, iff_friend) — demonstracja bez sprzetu."""
        self.log.info("SmartGuard start. Stan poczatkowy: %s", self.state.name)
        for i, (target, friend) in enumerate(scenario, 1):
            action = self.step(target, friend)
            self.log.info("  [t%02d] cel=%s swoj=%s | stan=%s%s",
                          i, int(target), int(friend), self.state.name,
                          f" | AKCJA={action}" if action else "")
        self.log.info("Koniec scenariusza.")
