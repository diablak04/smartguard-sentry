# Sentry: sprzęt, złote zasady, protokół ESP32

> **Kiedy czytać:** przed zmianą w `firmware/**`, w module wieżyczki (`turret_controller.py`), w IFF/BLE
> (`ble_scanner.py`) i przed każdą pracą przy okablowaniu. Właściciel obszaru: PO.

## Złote zasady (NIE łamać)
1. **Serwa max 6 V**: ustaw XL4015 miernikiem PRZED podłączeniem serw.
2. **Wylot lufy Ø1,5 mm**, nie szerszy (zweryfikowane CFD: strumień ~13,4 m/s, ~0,9 bar, ~1,4 l/min).
3. **Dioda flyback 1N4007** na pompce jest obowiązkowa (chroni MOSFET).
4. **ESP32 = logika 3,3 V**: laser przez tranzystor; MOSFET D4184 łapie 3,3 V.
5. **Prąd pompki i serw NIE przez płytkę stykową**, tylko bezpośrednie przewody.
6. **Celować w korpus, nigdy w głowę** (BHP); impuls pompki max 200 ms.
7. Kąty serw i czas impulsu strojone w `config.json`, nie w kodzie Pythona (`docs/agents/code.md` § Konfiguracja).

## Protokół PC ↔ ESP32 (UART 115200)
- PC → ESP32: `AIM:<pan>,<tilt>` · `FIRE:<ms>` · `LASER:0/1` · `BUZZ` (działają w `turret_controller.py` i firmware)
  · `SCAN:ON/OFF` (jeszcze nie ma).
- ESP32 → PC: `IFF:<0/1>,<rssi>`: swój widoczny (brelok BLE) + siła sygnału (jeszcze nie ma; stan w
  `docs/project/decisions.md` § D-01 (skan BLE na ESP32)).
- **Skan BLE robi ESP32** (ma wbudowane BLE; PC nie ma Bluetooth; uzasadnienie: `docs/project/decisions.md` § D-01).
  `bleak` na PC to tylko opcjonalny zapas.

## Mikrokontroler
**ESP32** (NIE Arduino Nano, zmienione), Arduino C++ + `ESP32Servo`.

## Wgrywanie firmware
1. Arduino IDE 2 → *Boards Manager*: **esp32** (Espressif) → *Library Manager*: **ESP32Servo**.
2. Kabel USB z danymi. Brak portu COM → sterownik: CP2102 → Silicon Labs CP210x, CH340 → WCH CH340.
3. Szkic z `firmware/`, *Board: ESP32 Dev Module*, **Upload** (wisi na `Connecting....` → przytrzymaj **BOOT**).
   Monitor portu: 115200.

## Finalny BOM (kluczowe, zweryfikowane)
- 2× serwo MG996R (metal, 180°), **zasilanie MAX 6 V**.
- Uchwyt Pan-Tilt (z łożyskiem), kupiony (albo druk 3D).
- Pompka spryskiwacza 12 V + wężyk silikonowy 4/6 mm + **lufa: rurka mosiężna Ø2,5/1,5 mm, wylot Ø1,5 mm**.
- ESP32, moduł MOSFET D4184 (trigger 3,3 V), przetwornica **XL4015 5A** (12 V → 5–6 V dla serw), kondensator 1000 µF,
  dioda 1N4007 (flyback na pompce).
- Laser 650 nm 5 V przez tranzystor 2N2222 (+ rez. 1 kΩ baza, 10 kΩ pull-down), buzzer aktywny 5 V.
- Zasilacz 12 V ≥3 A, gniazdo DC 5.5/2.1, płytka 830 pól, przewody Dupont.
- IFF: brelok BLE (stały MAC) w kieszeni.

## Źródła poza repo
Dokumenty robocze Sentry: `SmartGuard_Karta_Projektu_Sentry_Edition_v2.pdf`, `SmartGuard_Instrukcja_wykonawcza.pdf`
(plan dzień po dniu, BOM). Symulacja CFD lufy: lokalnie u PO (OpenFOAM/SimScale).
