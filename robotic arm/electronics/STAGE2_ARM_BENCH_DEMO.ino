/*
  AGASTYA Stage 2 low-load bench demonstration scaffold.

  This sketch is not a machine controller and is not intended for the 2 m
  Stage 2 concept or PV-panel disassembly. It has no safety rating, encoder
  feedback, collision sensing, force control, validated joint limits, or
  automatic trajectory. Do not attach servos until a supervisor has reviewed
  the wiring and each axis is mechanically supported and unloaded.

  The external E-stop must interrupt the separately fused servo-power rail
  through a suitably rated device. The Arduino input below reports contact
  state only. Removing servo power can let a gravity-loaded axis fall.
*/

#include <Servo.h>
#include <stdio.h>

static const uint8_t AXIS_COUNT = 4;
static const uint8_t servoPins[AXIS_COUNT] = {2, 3, 4, 5};
static const uint8_t minLimitPins[AXIS_COUNT] = {30, 32, 34, 36};
static const uint8_t maxLimitPins[AXIS_COUNT] = {31, 33, 35, 37};
static const uint8_t eStopStatusPin = 22;       // NC contact to GND; HIGH = open/tripped
static const uint8_t safetyRelayStatusPin = 23; // optional isolated status contact

// Placeholder software ranges only. Replace after checking the mechanism and
// the selected servo's permitted travel. These are not hard stops or safety limits.
static const int softMin[AXIS_COUNT] = {20, 25, 25, 25};
static const int softMax[AXIS_COUNT] = {160, 145, 155, 155};

Servo joints[AXIS_COUNT];
int currentDeg[AXIS_COUNT] = {90, 90, 90, 90};
int targetDeg[AXIS_COUNT] = {90, 90, 90, 90};
bool enabled = false;
bool faulted = false;
unsigned long lastStepMs = 0;
String inputLine;

bool eStopHealthy() {
  return digitalRead(eStopStatusPin) == LOW;
}

bool relayHealthy() {
  return digitalRead(safetyRelayStatusPin) == LOW;
}

bool anyLimitOpen() {
  for (uint8_t i = 0; i < AXIS_COUNT; ++i) {
    if (digitalRead(minLimitPins[i]) == HIGH || digitalRead(maxLimitPins[i]) == HIGH) {
      return true; // NC loop open, activated, or broken wire: fail closed in software.
    }
  }
  return false;
}

void detachAll() {
  for (uint8_t i = 0; i < AXIS_COUNT; ++i) {
    if (joints[i].attached()) joints[i].detach();
  }
  enabled = false;
}

void stopForFault(const __FlashStringHelper *reason) {
  detachAll();
  faulted = true;
  Serial.print(F("FAULT: "));
  Serial.println(reason);
  Serial.println(F("Servo power must be interrupted by the external hardware E-stop."));
}

void printHelp() {
  Serial.println(F("Commands: STATUS | RESET | ENABLE | DISABLE | CENTER | J <1..4> <deg>"));
  Serial.println(F("Manual jog only. Do not use for a process arm."));
}

void printStatus() {
  Serial.print(F("estop=")); Serial.print(eStopHealthy() ? F("OK") : F("TRIPPED"));
  Serial.print(F(" relay=")); Serial.print(relayHealthy() ? F("OK") : F("OPEN"));
  Serial.print(F(" limits=")); Serial.print(anyLimitOpen() ? F("OPEN/FAULT") : F("OK"));
  Serial.print(F(" enabled=")); Serial.print(enabled ? F("YES") : F("NO"));
  Serial.print(F(" fault=")); Serial.println(faulted ? F("YES") : F("NO"));
}

void attachAtStoredTargets() {
  // Servo.attach() may cause motion to the stored target. The arm must be
  // unloaded, caught, manually positioned, and guarded before ENABLE.
  for (uint8_t i = 0; i < AXIS_COUNT; ++i) {
    joints[i].attach(servoPins[i]);
    joints[i].write(currentDeg[i]);
  }
  enabled = true;
}

void handleLine(String line) {
  line.trim();
  if (!line.length()) return;

  if (line.equalsIgnoreCase("STATUS")) { printStatus(); return; }
  if (line.equalsIgnoreCase("HELP")) { printHelp(); return; }
  if (line.equalsIgnoreCase("DISABLE")) { detachAll(); Serial.println(F("Disabled.")); return; }

  if (line.equalsIgnoreCase("RESET")) {
    if (!eStopHealthy() || !relayHealthy() || anyLimitOpen()) {
      Serial.println(F("Reset refused: inspect and close all NC loops first."));
      return;
    }
    faulted = false;
    detachAll();
    Serial.println(F("Software fault reset; servo outputs remain detached."));
    return;
  }

  if (line.equalsIgnoreCase("ENABLE")) {
    if (faulted || !eStopHealthy() || !relayHealthy() || anyLimitOpen()) {
      Serial.println(F("Enable refused: reset and verify all input loops."));
      return;
    }
    attachAtStoredTargets();
    Serial.println(F("Enabled at stored open-loop targets. Check the arm continuously."));
    return;
  }

  if (line.equalsIgnoreCase("CENTER")) {
    for (uint8_t i = 0; i < AXIS_COUNT; ++i) targetDeg[i] = 90;
    Serial.println(F("Targets set to 90 deg; motion occurs only while enabled."));
    return;
  }

  if (line.startsWith("J ") || line.startsWith("j ")) {
    int axis = -1;
    int angle = -1;
    char command[32];
    line.toCharArray(command, sizeof(command));
    if (sscanf(command, "J %d %d", &axis, &angle) != 2 || axis < 1 || axis > AXIS_COUNT) {
      Serial.println(F("Use J <axis 1..4> <angle deg>."));
      return;
    }
    const uint8_t i = (uint8_t)(axis - 1);
    if (angle < softMin[i] || angle > softMax[i]) {
      Serial.println(F("Target rejected by placeholder software range."));
      return;
    }
    targetDeg[i] = angle;
    Serial.println(F("Target accepted; no feedback confirms actual joint position."));
    return;
  }

  Serial.println(F("Unknown command."));
  printHelp();
}

void serviceSerial() {
  while (Serial.available()) {
    const char ch = (char)Serial.read();
    if (ch == '\n' || ch == '\r') {
      if (inputLine.length()) {
        handleLine(inputLine);
        inputLine = "";
      }
    } else if (inputLine.length() < 50) {
      inputLine += ch;
    } else {
      inputLine = "";
      Serial.println(F("Input line too long; discarded."));
    }
  }
}

void serviceMotion() {
  if (!enabled || millis() - lastStepMs < 35) return;
  lastStepMs = millis();
  for (uint8_t i = 0; i < AXIS_COUNT; ++i) {
    if (currentDeg[i] < targetDeg[i]) ++currentDeg[i];
    else if (currentDeg[i] > targetDeg[i]) --currentDeg[i];
    joints[i].write(currentDeg[i]);
  }
}

void setup() {
  pinMode(eStopStatusPin, INPUT_PULLUP);
  pinMode(safetyRelayStatusPin, INPUT_PULLUP);
  for (uint8_t i = 0; i < AXIS_COUNT; ++i) {
    pinMode(minLimitPins[i], INPUT_PULLUP);
    pinMode(maxLimitPins[i], INPUT_PULLUP);
  }
  Serial.begin(115200);
  detachAll();
  Serial.println(F("AGASTYA low-load Stage 2 bench scaffold; outputs start detached."));
  printHelp();
  printStatus();
  if (!eStopHealthy() || !relayHealthy() || anyLimitOpen()) {
    faulted = true;
    Serial.println(F("Input loop fault at boot; inspect before RESET."));
  }
}

void loop() {
  serviceSerial();
  if (!faulted) {
    if (!eStopHealthy()) stopForFault(F("E-stop status open"));
    else if (!relayHealthy()) stopForFault(F("safety relay status open"));
    else if (anyLimitOpen()) stopForFault(F("limit loop open or wire fault"));
  }
  serviceMotion();
}
