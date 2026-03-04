/* Projeto Medidor de Temperatura - LM35 */

int tempPadrao = 28;
const int sensorLM35 = A0;

void setup() {
  Serial.begin(9600);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
}

void loop() {
  int valorSensor = analogRead(sensorLM35);
  float tensao = valorSensor * (5.0 / 1024.0);
  float temperaturaC = tensao * 100.0;

  // Formato estruturado para o app Python
  Serial.print("SENSOR=LM35;VALOR=");
  Serial.print(temperaturaC, 2);
  Serial.println(";UNIDADE=C");

  if (temperaturaC < tempPadrao) {
    digitalWrite(10, HIGH);
    digitalWrite(11, LOW);
  } else {
    digitalWrite(10, LOW);
    digitalWrite(11, HIGH);
  }

  delay(1000);
}
