// SmartGuard — firmware ESP32 (Arduino C++)
// Odbiera komendy z PC przez USB UART (115200): AIM / FIRE / LASER / BUZZ / SCAN
// Wymaga biblioteki: ESP32Servo

#include <ESP32Servo.h>

Servo pan, tilt;
const int PIN_PAN = 13, PIN_TILT = 12;
const int LASER = 26, BUZZER = 27, POMPA = 25;

// Limity BHP (nie celować w twarz) — dostosuj po kalibracji
const int TILT_MIN = 20, TILT_MAX = 60;
const int PAN_MIN = 30,  PAN_MAX = 150;

int zacisnij(int v, int lo, int hi) { return v < lo ? lo : (v > hi ? hi : v); }

void setup() {
  Serial.begin(115200);
  pan.attach(PIN_PAN);
  tilt.attach(PIN_TILT);
  pinMode(LASER, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  pinMode(POMPA, OUTPUT);
  pan.write(90);
  tilt.write(TILT_MIN);
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
    digitalWrite(POMPA, HIGH); delay(ms); digitalWrite(POMPA, LOW);
  } else if (s == "LASER:1") {
    digitalWrite(LASER, HIGH);
  } else if (s == "LASER:0") {
    digitalWrite(LASER, LOW);
  } else if (s == "BUZZ") {
    digitalWrite(BUZZER, HIGH); delay(200); digitalWrite(BUZZER, LOW);
  }
  // TODO (Dzień 9): SCAN:ON / SCAN:OFF — tryb patrolu wahadłowego
}
