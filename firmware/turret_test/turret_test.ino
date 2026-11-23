// Test: PAN +-30° (prawo/lewo), potem TILT +-30° (gora/dol). Srodek 90/90. W petli.
#include <ESP32Servo.h>

Servo pan, tilt;
const int PIN_PAN = 12, PIN_TILT = 13;

void plynnie(Servo &s, int from, int to) {
  int krok = (from < to) ? 1 : -1;
  for (int a = from; a != to; a += krok) { s.write(a); delay(15); }
  s.write(to);
}

void setup() {
  pan.setPeriodHertz(50);  pan.attach(PIN_PAN, 500, 2400);
  tilt.setPeriodHertz(50); tilt.attach(PIN_TILT, 500, 2400);
  pan.write(90); tilt.write(90);
  delay(1000);
}

void loop() {
  // PAN +-30° (prawo -> srodek -> lewo -> srodek)
  plynnie(pan, 90, 120); delay(600);
  plynnie(pan, 120, 90); delay(600);
  plynnie(pan, 90, 60);  delay(600);
  plynnie(pan, 60, 90);  delay(800);

  // TILT +-30° (gora -> srodek -> dol -> srodek)
  plynnie(tilt, 90, 120); delay(600);
  plynnie(tilt, 120, 90); delay(600);
  plynnie(tilt, 90, 60);  delay(600);
  plynnie(tilt, 60, 90);  delay(800);

  delay(2000);
}
