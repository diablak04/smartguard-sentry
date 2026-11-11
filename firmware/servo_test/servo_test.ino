// SmartGuard — TEST pojedynczego serwa (os Pan).
// Powolny sweep 30..150 stopni, zeby ograniczyc skoki pradu (bezpieczniej).
//
// PODLACZENIE (wazne!):
//   - sygnal (pomaranczowy/zolty) -> GPIO13
//   - zasilanie + (czerwony)      -> 5-6 V z ZEWNETRZNEGO zrodla (NIE z 3.3V ESP32!)
//   - masa - (brazowy/czarny)     -> GND zrodla ORAZ wspolna masa z ESP32
// MG996R potrafi ciagnac >1 A przy ruchu — NIE zasilaj z pinu 3.3V.

#include <ESP32Servo.h>

Servo serwo;
const int PIN_SERWO = 13;
const int KAT_MIN = 30, KAT_MAX = 150;   // limity jak w projekcie (Pan)

void setup() {
  Serial.begin(115200);
  delay(300);
  Serial.println("SERWO-TEST: powolny sweep 30..150 na GPIO13");
  serwo.setPeriodHertz(50);               // 50 Hz = standard dla serw
  serwo.attach(PIN_SERWO, 500, 2400);     // zakres impulsu MG996R
  serwo.write(90);                        // srodek
  delay(600);
}

void loop() {
  for (int a = KAT_MIN; a <= KAT_MAX; a += 2) { serwo.write(a); Serial.printf("kat=%d\n", a); delay(30); }
  delay(500);
  for (int a = KAT_MAX; a >= KAT_MIN; a -= 2) { serwo.write(a); Serial.printf("kat=%d\n", a); delay(30); }
  delay(500);
}
