void setup() {
  Serial.begin(38400);
}

int count=0;

void loop() {
  count++;
  Serial.print("count is: ");
  delay(750);
}
