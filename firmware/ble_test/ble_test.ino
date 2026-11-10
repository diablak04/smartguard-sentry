// SmartGuard — TEST skanera BLE (IFF).
// ESP32 skanuje otoczenie BLE i wypisuje przez USB (115200) MAC + RSSI + nazwe.
// Cel: znalezc MAC "swojego" (telefon teraz, brelok docelowo). Pozniej logika IFF
// trafi do glownego firmware (smartguard_esp32.ino) i bedzie slac do PC: IFF:<0/1>,<rssi>.
//
// Plytka: ESP32 Dev Module. Nic nie trzeba podlaczac poza samym ESP32 (USB).

#include <BLEDevice.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

BLEScan* scanner;
const int CZAS_SKANU = 3;  // sekundy na jeden skan

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("BLE-TEST start — skanuje co ~4 s. Zblizaj telefon, by rosl RSSI.");
  BLEDevice::init("");
  scanner = BLEDevice::getScan();
  scanner->setActiveScan(true);  // aktywny skan = wiecej danych (nazwy urzadzen)
  scanner->setInterval(100);
  scanner->setWindow(99);
}

void loop() {
  BLEScanResults* r = scanner->start(CZAS_SKANU, false);
  int n = r->getCount();
  Serial.printf("--- skan: %d urzadzen ---\n", n);
  for (int i = 0; i < n; i++) {
    BLEAdvertisedDevice d = r->getDevice(i);
    Serial.printf("BLE %s  RSSI=%d dBm  name=%s\n",
                  d.getAddress().toString().c_str(),
                  d.getRSSI(),
                  d.haveName() ? d.getName().c_str() : "-");
  }
  scanner->clearResults();
  delay(1000);
}
