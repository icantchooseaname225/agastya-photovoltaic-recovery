#include <Servo.h>

// AGASTYA-EYE tabletop control-interface demo.
// Commands are synthetic operator inputs over USB serial; this sketch is not
// connected to the AGASTYA-EYE classifier and is not an industrial gate control.

const byte SERVO_PIN = 9;
const int HOLD_ANGLE = 90;
const int APPROVE_ANGLE = 35;
const int REJECT_ANGLE = 145;
const unsigned long DECISION_TIMEOUT_MS = 2000;
const size_t COMMAND_CAPACITY = 24;

Servo gateServo;
char commandBuffer[COMMAND_CAPACITY];
size_t commandLength = 0;
unsigned long lastDecisionMs = 0;
bool decisionActive = false;

void applyState(const char *state, int angle) {
  gateServo.write(angle);
  lastDecisionMs = millis();
  decisionActive = true;
  Serial.print("STATE=");
  Serial.print(state);
  Serial.print("; SERVO_ANGLE_DEG=");
  Serial.println(angle);
}

void handleCommand() {
  commandBuffer[commandLength] = '\0';
  if (strcmp(commandBuffer, "APPROVE") == 0) {
    applyState("APPROVE_DEMO", APPROVE_ANGLE);
  } else if (strcmp(commandBuffer, "REJECT") == 0) {
    applyState("REJECT_DEMO", REJECT_ANGLE);
  } else if (strcmp(commandBuffer, "HOLD") == 0) {
    applyState("HOLD", HOLD_ANGLE);
  } else if (commandLength > 0) {
    Serial.println("ERROR=UNKNOWN_COMMAND; STATE_UNCHANGED");
  }
  commandLength = 0;
}

void setup() {
  Serial.begin(115200);
  gateServo.attach(SERVO_PIN);
  gateServo.write(HOLD_ANGLE);
  lastDecisionMs = millis();
  Serial.println("AGASTYA-EYE servo gate tabletop demo");
  Serial.println("Send APPROVE, REJECT, or HOLD followed by newline.");
  Serial.println("Synthetic serial commands only; not a classifier or safety controller.");
}

void loop() {
  while (Serial.available() > 0) {
    const char incoming = (char)Serial.read();
    if (incoming == '\r' || incoming == '\n') {
      handleCommand();
    } else if (commandLength < COMMAND_CAPACITY - 1) {
      commandBuffer[commandLength++] = incoming;
    } else {
      commandLength = 0;
      Serial.println("ERROR=COMMAND_TOO_LONG; STATE_UNCHANGED");
    }
  }

  if (decisionActive && millis() - lastDecisionMs >= DECISION_TIMEOUT_MS) {
    gateServo.write(HOLD_ANGLE);
    decisionActive = false;
    Serial.println("STATE=HOLD_TIMEOUT");
  }
}
