// ===== PINOS =====
const int PIN_RED = 10;    // LED vermelho
const int PIN_GREEN = 8;   // LED verde
const int PIN_TRIGGER = 5; // Sensor ultrassônico principal TRIG
const int PIN_ECHO = 4;    // Sensor ultrassônico principal ECHO
const int PIN_BUZZER = 2;  // buzzer

// Sensores de resposta
const int TRIG_A = 6;
const int ECHO_A = 7;
const int TRIG_B = 9;
const int ECHO_B = 11;
const int TRIG_C = 12;
const int ECHO_C = 13;

// LEDs de resposta
const int LED_A = A2;
const int LED_B = A1;
const int LED_C = A0;

// ===== CONTROLE =====
unsigned long tempoSaida = 0;
bool objetoDetectado = false;
bool aguardandoVerde = false;
bool quizAtivo = false;

// Temporizadores para LEDs de resposta
unsigned long tempoLED_A = 0;
unsigned long tempoLED_B = 0;
unsigned long tempoLED_C = 0;
const unsigned long TEMPO_RESET_LED = 3000; // 3 segundos

// ===== FUNÇÕES =====
long readUltrasonicDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  return pulseIn(echoPin, HIGH, 30000); // timeout 30ms
}

float distanciaCM(int trig, int echo) {
  long duracao = readUltrasonicDistance(trig, echo);
  if(duracao == 0) return 100; // sem eco → valor alto para ignorar
  return duracao * 0.01723;
}

void resetRespostas() {
  digitalWrite(LED_A, LOW);
  digitalWrite(LED_B, LOW);
  digitalWrite(LED_C, LOW);
}

// ===== SETUP =====
void setup() {
  Serial.begin(9600);

  pinMode(PIN_RED, OUTPUT);
  pinMode(PIN_GREEN, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);

  pinMode(LED_A, OUTPUT);
  pinMode(LED_B, OUTPUT);
  pinMode(LED_C, OUTPUT);

  pinMode(TRIG_A, OUTPUT); pinMode(ECHO_A, INPUT);
  pinMode(TRIG_B, OUTPUT); pinMode(ECHO_B, INPUT);
  pinMode(TRIG_C, OUTPUT); pinMode(ECHO_C, INPUT);

  digitalWrite(PIN_GREEN, HIGH); // LED verde inicialmente ligado
  digitalWrite(PIN_RED, LOW);

  quizAtivo = true;  // ativa o quiz já no início
  resetRespostas();

  Serial.println("LED VERDE ON - Quiz ativado"); // mensagem inicial para Python
}

// ===== LOOP PRINCIPAL =====
void loop() {
  // === SENSOR PRINCIPAL ===
  float distPrincipal = distanciaCM(PIN_TRIGGER, PIN_ECHO);

  if(distPrincipal > 0 && distPrincipal <= 5) {
    digitalWrite(PIN_RED, HIGH);
    digitalWrite(PIN_GREEN, LOW);
    tone(PIN_BUZZER, 523);

    objetoDetectado = true;
    aguardandoVerde = true;
    quizAtivo = false;
    tempoSaida = millis();

    resetRespostas();
  }
  else {
    digitalWrite(PIN_RED, LOW);
    noTone(PIN_BUZZER);

    if(objetoDetectado && aguardandoVerde && millis() - tempoSaida >= 5000) {
      digitalWrite(PIN_GREEN, HIGH);
      quizAtivo = true;
      aguardandoVerde = false;
      objetoDetectado = false;
      resetRespostas();

      Serial.println("LED VERDE ON - Quiz ativado"); // envia mensagem ao Python
    }
  }

  // === SENSORES DE RESPOSTA ===
  if(quizAtivo && digitalRead(PIN_GREEN) == HIGH) {
    float dA = distanciaCM(TRIG_A, ECHO_A);
    float dB = distanciaCM(TRIG_B, ECHO_B);
    float dC = distanciaCM(TRIG_C, ECHO_C);

    // Sensor A
    if(dA > 0 && dA <= 5) {
      digitalWrite(LED_A, HIGH);
      tempoLED_A = millis();
      Serial.println("RESPOSTA_A"); // envia para Python
    }

    // Sensor B
    if(dB > 0 && dB <= 5) {
      digitalWrite(LED_B, HIGH);
      tempoLED_B = millis();
      Serial.println("RESPOSTA_B"); // envia para Python
    }

    // Sensor C
    if(dC > 0 && dC <= 5) {
      digitalWrite(LED_C, HIGH);
      tempoLED_C = millis();
      Serial.println("RESPOSTA_C"); // envia para Python
    }

    // Reset automático após 3 segundos sem detecção
    if(digitalRead(LED_A) == HIGH && millis() - tempoLED_A >= TEMPO_RESET_LED) digitalWrite(LED_A, LOW);
    if(digitalRead(LED_B) == HIGH && millis() - tempoLED_B >= TEMPO_RESET_LED) digitalWrite(LED_B, LOW);
    if(digitalRead(LED_C) == HIGH && millis() - tempoLED_C >= TEMPO_RESET_LED) digitalWrite(LED_C, LOW);
  }

  delay(100); // mantém leitura estável
}