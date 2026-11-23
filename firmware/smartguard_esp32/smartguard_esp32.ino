// SmartGuard — firmware ESP32 (Arduino C++)
// Odbiera komendy z PC przez USB UART (115200): AIM / FIRE / LASER / BUZZ / SCAN
// Wymaga biblioteki: ESP32Servo

#include <ESP32Servo.h>

Servo pan, tilt;
const int PIN_PAN = 12, PIN_TILT = 13;   // pan(obrot poziomy)=GPIO12, tilt(kiwanie)=GPIO13
const int LASER = 26, BUZZER = 27, POMPA = 25;

// Limity BHP (nie celować w twarz) — WARTOSCI STARTOWE, dostroic kalibracja.
// Po montazu 3D tilt sklejony na srodku=90°, wiec zakres wokol 90.
const int TILT_MIN = 65, TILT_MAX = 115;
const int PAN_MIN = 30,  PAN_MAX = 150;

int zacisnij(int v, int lo, int hi) { return v < lo ? lo : (v > hi ? hi : v); }

void setup() {
  Serial.begin(115200);
  pan.setPeriodHertz(50);  pan.attach(PIN_PAN, 500, 2400);
  tilt.setPeriodHertz(50); tilt.attach(PIN_TILT, 500, 2400);
  pinMode(LASER, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  pinMode(POMPA, OUTPUT);
  pan.write(90);
  tilt.write(90);   // start na srodku (tilt sklejony poziomo przy 90°)
}

void loop() {
  if (!Serial.available()) return;
  String s = Serial.readStringUntil('\n');
  s.trim();

  if (s.startsWith("AIM:")) {                 // AIM:<pan>,<tilt>
    int sep = s.indexOf(',');
    int p = s.substring(4, sep).toInt();
    int t = s.substring(sep + 1).toInt();
    pan.write(zacisnij(p, PAN_MIN, PAN_MAX));
    tilt.write(zacisnij(t, TILT_MIN, TILT_MAX));
  } else if (s.startsWith("FIRE:")) {         // FIRE:<ms>  (max 250 ms — BHP)
    int ms = zacisnij(s.substring(5).toInt(), 0, 250);
    // "strzal": na teraz buzzer + (docelowo) pompa; laser dojdzie jak wroci kabel
    digitalWrite(POMPA, HIGH); digitalWrite(BUZZER, HIGH);
    delay(ms);
    digitalWrite(POMPA, LOW);  digitalWrite(BUZZER, LOW);
  } else if (s == "LASER:1") {
    digitalWrite(LASER, HIGH);
  } else if (s == "LASER:0") {
    digitalWrite(LASER, LOW);
  } else if (s == "BUZZ") {
    digitalWrite(BUZZER, HIGH); delay(200); digitalWrite(BUZZER, LOW);
  }
  // TODO (Dzień 9): SCAN:ON / SCAN:OFF — tryb patrolu wahadłowego
}
