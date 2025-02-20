#include <Wire.h>
#include <hd44780.h>  
#include <hd44780ioClass/hd44780_I2Cexp.h>

hd44780_I2Cexp lcd;  // Auto-detect I2C address

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Voice Assistant");
  delay(2000);
  lcd.clear();
}

void loop() {
  if (Serial.available()) {
    String text = Serial.readStringUntil('\n');  // Read text from Python
    lcd.clear();  
    lcd.setCursor(0, 0);
    lcd.print(text.substring(0, 16));  // Print first 16 characters
    if (text.length() > 16) {
      lcd.setCursor(0, 1);
      lcd.print(text.substring(16, 32));  // Print second line
    }
  }
}
