# SmartGuard: Sentry Edition — Podział pracy (3 osoby)

> Projekt na Inżynierię Oprogramowania (Informatyka, rok II).
> Repo: `D:\smartguard\smartguard-app` · Termin oddania: 24.01.2027.
> Ustalenie: rdzeń systemu i całe spięcie trzyma lider; dwie pozostałe osoby
> dostają odseparowane, wymienne moduły na końcach przepływu.

---

## Filozofia podziału

- **Rdzeń (krytyczna ścieżka demo)** zostaje u lidera: hardware, firmware, wizja,
  logika, integracja i n8n. Od tego zależy, czy wieżyczka w ogóle zadziała.
- **Reszta zespołu** dostaje moduły **odseparowane interfejsem** — jeśli zrobią je
  źle, demo dalej działa (po prostu bez historii / panelu / powiadomień).
- Interfejs definiuje lider; zespół „wypełnia środek" wg podpisów funkcji i schematów.
- Git: gałęzie `<type>/<short-description>` (np. `feat/web-panel`) + **PR z 1 approval (lidera)** — nic nie wchodzi na
  `main` bez przeglądu.

---

## 🔧 LIDER (rdzeń + glue) — fizyczna budowa

Wszystko na krytycznej ścieżce demo.

### Hardware / mechanika / zasilanie
- Elektronika wg BOM i „złotych zasad": XL4015 ustawiona miernikiem na **≤6 V przed**
  podłączeniem serw, MOSFET D4184, dioda flyback 1N4007 na pompce, laser przez
  tranzystor 2N2222, kondensator 1000 µF.
- Prąd pompki/serw **nie** przez płytkę stykową — bezpośrednie przewody.
- Mechanika Pan-Tilt (łożysko), lufa mosiężna wylot **Ø1,5 mm** (nie szerszy — CFD),
  pompka + wężyk, zasilanie 12 V.

### Firmware ESP32 (`firmware/smartguard_esp32`)
- Pełny protokół UART (115200):
  - PC→ESP32: `AIM:<pan>,<tilt>` · `FIRE:<ms>` · `LASER:0/1` · `BUZZ` · `SCAN:ON/OFF`
  - ESP32→PC: `IFF:<0/1>,<rssi>`
- Serwa przez `ESP32Servo`.
- **Skan BLE / IFF robi ESP32** (PC nie ma Bluetootha) → wysyła `IFF:<0/1>,<rssi>`.

### Software rdzenia
- `rules.py` — potwierdzenie detekcji na **3 klatkach** + fuzja IFF (czyta `IFF:...`
  z portu szeregowego).
- `turret_controller.py` — **visual servoing**: piksel → kąty pan/tilt, wysyłka
  `AIM`/`FIRE` po UART.
- `main.py` — maszyna stanów (IDLE→…→COOLDOWN) + orkiestracja całości.

### Spięcie / przepływ
- **n8n** (lokalnie w Dockerze) — cała logika powiadomień.
- **Webhook n8n → Telegram** (to część spięcia, robi lider).
- Decyzja co kogo woła i kiedy.

### BHP
- Impuls pompki max 200 ms, celowanie w korpus (nigdy w głowę), zakresy kątów serw.

---

## 💻 OSOBA B () — dane + panel

Produkuje dane i je wyświetla. Lider je konsumuje w `main.py` i rozsyła przez n8n.
Jeśli zawali — demo dalej strzela, tylko bez historii/panelu.

- **`events.py`** — zapis zdarzeń do **SQLite** + zapis klatek **JPG** w `events/`.
- **Panel WWW (FastAPI)** — lista zdarzeń + podgląd zdjęć + status systemu;
  czyta wyłącznie bazę z `events.py`.

**Kontrakt od lidera:** schemat tabeli SQLite + podpis funkcji, np.
```python
def zapisz_zdarzenie(typ: str, pewnosc: float, klatka) -> int:
    """Zapisz zdarzenie do SQLite i klatkę jako JPG w events/.
    Zwróć id wiersza. Schemat tabeli: id, ts, typ, pewnosc, sciezka_foto."""
    ...  # <- to wypełnia osoba B
```

---

## 📋 OSOBA C () — powiadomienia + proces

Zadania o niskim ryzyku technicznym, wysokiej wartości na ocenę (proces IO).

- **Bot Telegram** — założenie bota, token do `.env`, test „czy wiadomość dochodzi".
  (Webhook n8n→Telegram robi lider; osoba C dostarcza działającego bota + `chat_id`.)
- **Kanban / Scrum** — aktualizacja tablicy, sprinty, retrospektywy.
- **Dokumentacja** — README, instrukcja użytkownika, diagramy architektury, zapisy sesji.
- **Testy manualne + raporty** — uruchamianie `detekcja_test.py`, `kalibracja_strefy.py`,
  spisywanie wyników.
- **Prezentacja na obronę** — slajdy + nagranie demo.

**Kontrakt od lidera:** osoba C przekazuje `token` bota i `chat_id`; co i kiedy wysłać
ustala lider w n8n.

---

## Dwa „kontrakty", które spinają wszystko

1. **Schemat SQLite + podpis `zapisz_zdarzenie(...)`** — granica lider ↔ osoba B
   (panel i `main.py` czytają/piszą to samo).
2. **`token` + `chat_id` bota Telegram** — granica lider ↔ osoba C
   (resztę przepływu ogarnia n8n po stronie lidera).

Dodatkowo `config.json` = jedno źródło konfiguracji (strefa, kąty, progi) — zero
sztywnych wartości w kodzie.

---

## Mapowanie na plan 10-dniowy

| Faza | LIDER (rdzeń+glue) | OSOBA B (dane/panel) | OSOBA C (proces) |
|---|---|---|---|
| **Dni 1–3** *(bez sprzętu)* | kompletowanie BOM, montaż uchwytu, firmware „na sucho" (test serw), `rules.py` + servoing na mocku | szkielet `events.py` (SQLite + JPG) | założenie bota Telegram, start Kanban, szkielet dokumentacji |
| **Dni 4–6** *(sprzęt)* | elektronika + firmware + woda, integracja `turret_controller` z ESP32 (**pierwszy strzał**), n8n | panel WWW (lista zdarzeń + zdjęcia) | testy manualne + raporty, aktualizacja Kanbana |
| **Dni 7–10** | tryby pracy + BHP w logice, spięcie n8n→Telegram, testy końcowe | finalizacja panelu + statusu | dokumentacja końcowa + prezentacja + demo |

---

*Dokument roboczy — ustalenia zespołu SmartGuard.*
