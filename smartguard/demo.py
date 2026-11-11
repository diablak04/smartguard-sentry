"""Demo bez kamery i sprzetu: maszyna stanow odgrywa scenariusz z intruzem.

Wynik w konsoli konczy sie linia 'Koniec scenariusza.' - to znaczy, ze instalacja dziala.
"""
from smartguard.config import load_config
from smartguard.state_machine import SmartGuard, setup_logging


def run() -> None:
    setup_logging()
    config = load_config()
    sg = SmartGuard(config)
    # Demo: intruz (WROG) wchodzi w strefe i zostaje w niej kilka klatek.
    scenario = [(False, False)] + [(True, False)] * 6 + [(False, False)] * 4
    sg.run_scenario(scenario)

