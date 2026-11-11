# SmartGuard: Sentry Edition

System ochrony posesji: kamera wykrywa ludzi (YOLO), wieżyczka Pan-Tilt strzela wodą we wroga,
swój jest rozpoznawany po breloku BLE (IFF), powiadomienia idą przez n8n + Telegram.
Projekt z **Inżynierii Oprogramowania** (Informatyka, rok II).

**Zespół:** diablak04 (Product Owner) · DEV (Lead Hardware) · AxmBro (Scrum Master)

## Szybki start (Windows + VS Code)

Sprzęt niepotrzebny — wieżyczka jest symulowana, wystarczy kamerka.

**1. Zainstaluj (raz):**
- [Python 3.13](https://www.python.org/downloads/windows/) — w instalatorze **zaznacz „Add python.exe to PATH”**,
- [VS Code](https://code.visualstudio.com/) + rozszerzenie **Python** (Microsoft).

**2. Pobierz projekt:** `git clone` albo **Code → Download ZIP** i rozpakuj. W VS Code: *File → Open Folder*.

**3. Zainstaluj biblioteki** — *Terminal → New Terminal* i wklej:
```bat
py -3.13 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```
Powstaje folder `.venv`: osobny Python z bibliotekami projektu (~1,2 GB, ok. 5 min).
Nie miesza się z systemem; usunięcie `.venv` = odinstalowanie.

**4. Wskaż VS Code `.venv`** (raz): `Ctrl+Shift+P` → *Python: Select Interpreter* → **`.venv`**.

**5. Uruchamiaj** przyciskiem **▶ Run Python File** (prawy górny róg):

| Plik | Co robi | Klawisze (kliknij najpierw w okno kamery) |
|---|---|---|
| `main.py` | demo bez kamery; `Koniec scenariusza.` = instalacja OK | — |
| `detekcja_test.py` | wykrywanie ludzi + strefa | `q` wyjście |
| `kalibracja_strefy.py` | klikasz rogi strefy chronionej | klik = punkt, `z` zapisz, `r` reset, `q` wyjście |
| `integracja.py` | cały system na żywo | `s` swój/wróg, `m` wycisz, `q` wyjście |

Model YOLO (5 MB) pobiera się sam przy pierwszym uruchomieniu z kamerą.

### Gdy nie działa
- **`No module named 'cv2'`** → VS Code używa systemowego Pythona: zrób krok 4. Używasz „Run Code”
  (rozszerzenie *Code Runner*)? Ono zawsze bierze systemowego Pythona — klikaj **Run Python File**.
- **`'py' is not recognized`** → zainstaluj Pythona ponownie z „Add python.exe to PATH”.
- **Czarne okno / zła kamera** → ustaw `"kamera_glowna": 1` w `config.local.json` (niżej).
- **Kamera zajęta** → zamknij Teams/Zoom/Discord.

## Ustawienia tylko u siebie — `config.local.json`

- `config.json` — wspólny, w repo. Zmiana trafia do wszystkich.
- `config.local.json` — Twój, **poza gitem**. Nadpisuje `config.json`. Opcjonalny: póki działa, nie twórz go.

Utworzenie (w terminalu VS Code), potem edytujesz go w VS Code:
```bat
copy config.local.example.json config.local.json
```
- `"kamera_glowna"` — `0` = wbudowana, `1` = druga (np. USB),
- `"esp32_port"` — zostaw `"auto"` (sam znajduje ESP32); wpisz np. `"COM5"` tylko, gdy auto nie znajdzie płytki.

Strefę dopisuje tam sam `kalibracja_strefy.py`. Można nadpisać każdy klucz z `config.json`.
`config.local.example.json` to tylko wzór — program go nie czyta. Nie edytuj go i nie usuwaj.

## ESP32 (tylko osoba od firmware)
1. [Arduino IDE 2](https://www.arduino.cc/en/software) → *Boards Manager*: **esp32** (Espressif) → *Library Manager*: **ESP32Servo**.
2. ESP32 podłącz kablem USB **z danymi** (nie „tylko ładowanie”). Brak nowego portu COM w Menedżerze urządzeń →
   sterownik wg kostki przy złączu USB: **CP2102** → Silicon Labs CP210x, **CH340** → WCH CH340.
3. Otwórz szkic z `firmware/` (na start `ble_test`), *Board: ESP32 Dev Module*, *Port: COMx*, **Upload**.
   Wisi na `Connecting....` → przytrzymaj **BOOT**. *Serial Monitor*: 115200.

⚠️ Przed podłączeniem serw i pompki: „Złote zasady” w `CLAUDE.md` (serwa max 6 V, dioda flyback, BHP).

**n8n + Telegram** (Faza 7) — jeszcze nie instaluj. Będzie potrzebny Docker Desktop i plik `.env` (wzór: `.env.example`).

## Stan projektu (listopad 2026)
Działa (software, wieżyczka symulowana):
- ✅ detekcja YOLO `yolo11n` na CPU (~40–60 ms/klatkę),
- ✅ strefa chroniona (wielokąt) + potwierdzanie na 3 klatkach,
- ✅ maszyna stanów IDLE → DETECTED → CONFIRMING → FRIENDLY/FOE → ENGAGE → COOLDOWN (+ wyciszenie),
- ✅ IFF: ESP32 skanuje BLE i rozpoznaje swojego po MAC/nazwie + RSSI (sprawdzone na płytce),
- ✅ integracja na żywo (`integracja.py`): cały łańcuch na kamerze.

Czeka na sprzęt: serwa, zasilanie, pompka, pierwszy strzał.
Następne (bez sprzętu): n8n + Telegram, zapis zdarzeń i zdjęć (SQLite), panel WWW.

## Jak to działa
Kamera → `capture.py` → `detector.py` (YOLO) → `zona.py` (strefa) + `rules.py` (3 klatki + IFF)
→ `main.py` (maszyna stanów) → `turret_controller.py` → ESP32 (serwa, pompka, laser).
ESP32 wysyła do PC `IFF:<0/1>,<rssi>` (swój w pobliżu + siła sygnału).

| Plik | Rola |
|---|---|
| `capture.py` | odczyt kamery w osobnym wątku |
| `detector.py` | YOLO `yolo11n`, tylko ludzie |
| `zona.py`, `kalibracja_strefy.py` | strefa chroniona + jej kalibracja |
| `rules.py` | potwierdzanie na 3 klatkach, swój/wróg |
| `main.py` | maszyna stanów + logi |
| `turret_controller.py` | komendy do ESP32 (AIM/FIRE/LASER/BUZZ), tryb SIM, auto-port |
| `integracja.py` | pełna pętla na żywo |
| `config.py` | wczytuje `config.json` + `config.local.json` |
| `ble_scanner.py` | skan BLE z PC (zapas — normalnie skanuje ESP32) |
| `events.py` | zapis zdarzeń + n8n — **do zrobienia** (Faza 7) |
| `firmware/` | ESP32: `smartguard_esp32` (główny), `ble_test`, `serwo_test` |

## Git
- Każdy pracuje na swojej gałęzi `<type>/<short-description>` (np. `feat/web-panel`, `fix/camera-index`).
- Do `main` tylko przez **Pull Request** zatwierdzony przez kogoś z zespołu (1 approval).
- Commity: `<type>(<scope>): <opis>`, np. `fix(zona): poprawne domkniecie strefy`.
- Kto co robi: `docs/podzial_pracy.md`.
