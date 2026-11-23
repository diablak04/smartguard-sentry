// Trzymaj serwa na SRODKU (90°) - do montazu/klejenia platformy.
// Serwo stoi nieruchomo na 90°, zeby zafiksowac orczyk/platforme w pozycji poziomej.
#include <ESP32Servo.h>

Servo pan, tilt;
const int PIN_PAN = 13, PIN_TILT = 12;

void setup() {
  pan.setPeriodHertz(50);  pan.attach(PIN_PAN, 500, 2400);
  tilt.setPeriodHertz(50); tilt.attach(PIN_TILT, 500, 2400);
  pan.write(90);
  tilt.write(90);   // srodek mechaniczny - rowny zakres gora/dol
}

void loop() {
  // nic - serwa trzymaja 90°
}
