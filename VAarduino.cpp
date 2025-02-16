void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readString();
    command.trim();
    
    if (command == "turn on light") digitalWrite(13, HIGH);
    else if (command == "turn off light") digitalWrite(13, LOW);
  }
}
