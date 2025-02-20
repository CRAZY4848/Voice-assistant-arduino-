 #include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
    Serial.begin(9600);
    lcd.begin(16, 2);
    lcd.backlight();
    lcd.print("Ask your question!");
}

void loop() {
    if (Serial.available()) {
        String answer = Serial.readStringUntil('\n');
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print(answer.substring(0, 16)); // First line (max 16 chars)
        lcd.setCursor(0, 1);
        if (answer.length() > 16) {
            lcd.print(answer.substring(16, 32)); // Second line
        }
    }
}
