"""Orkiestrator głównej pętli SmartGuard (maszyna stanów).

Stany: PATROL -> DETECTED -> CONFIRMING -> (FRIENDLY|FOE) -> ENGAGE -> COOLDOWN
Nakładki: MUTED, poza godzinami czuwania = tylko monitoring.

TODO (Dzień 6): spiąć capture -> detector -> rules -> turret_controller -> events.
"""
import json


def wczytaj_config(sciezka="config.json"):
    with open(sciezka, encoding="utf-8") as f:
        return json.load(f)


def main():
    cfg = wczytaj_config()
    print("SmartGuard start. Config wczytany:", list(cfg.keys()))
    # TODO: główna pętla (patrz Instrukcja wykonawcza, Dzień 6)


if __name__ == "__main__":
    main()
