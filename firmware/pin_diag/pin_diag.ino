// Diagnostyka pinow: rusza NAJPIERW tylko GPIO13, potem przerwa, potem tylko GPIO12.
// Patrz, ktore fizyczne serwo (gorne/dolne) rusza w ktorej fazie.
#include <ESP32Servo.h>

Servo s13, s12;
const int P13 = 13, P12 = 12;

void wiggle(Servo &s, int c, int amp, int razy) {
  for (int k = 0; k < razy; k++) {
    for (int a = c; a <= c + amp; a += 2) { s.write(a); delay(15); }
    for (int a = c + amp; a >= c - amp; a -= 2) { s.write(a); delay(15); }
    for (int a = c - amp; a <= c; a += 2) { s.write(a); delay(15); }
  }
}

void setup() {
  Serial.begin(115200);
  s13.setPeriodHertz(50); s13.attach(P13, 500, 2400);
  s12.setPeriodHertz(50); s12.attach(P12, 500, 2400);
  s13.write(90); s12.write(90);
  delay(800);
}

void loop() {
  Serial.println("FAZA 1: rusza tylko GPIO13");
  s12.write(90);               // GPIO12 trzyma srodek
  wiggle(s13, 90, 20, 3);      // GPIO13 macha
  delay(1500);

  Serial.println("FAZA 2: rusza tylko GPIO12");
  s13.write(90);               // GPIO13 trzyma srodek
  wiggle(s12, 90, 20, 3);      // GPIO12 macha
  delay(1500);
}
