#include <Servo.h>
#include <stdlib.h>
#include <string.h>

const uint8_t SERVO_PIN = 9;
const uint8_t CLOSED_ANGLE_DEG = 0;
const uint8_t OPEN_ANGLE_DEG = 90;
const unsigned long MIN_OPEN_DURATION_MS = 1000;
const unsigned long MAX_OPEN_DURATION_MS = 30000;
const size_t COMMAND_CAPACITY = 64;

Servo gateServo;
char commandBuffer[COMMAND_CAPACITY];
char lastCommandId[33] = "";
size_t commandLength = 0;
bool commandOverflow = false;
bool gateOpen = false;
unsigned long closeDeadline = 0;

bool isHexId(const char *value) {
  if (strlen(value) != 32) return false;
  for (size_t index = 0; index < 32; ++index) {
    const char character = value[index];
    if (!((character >= '0' && character <= '9') ||
          (character >= 'a' && character <= 'f'))) return false;
  }
  return true;
}

bool isDecimal(const char *value) {
  if (*value == '\0') return false;
  for (const char *cursor = value; *cursor != '\0'; ++cursor) {
    if (*cursor < '0' || *cursor > '9') return false;
  }
  return true;
}

void closeGate(bool reportCompletion) {
  gateServo.write(CLOSED_ANGLE_DEG);
  gateOpen = false;
  if (reportCompletion && lastCommandId[0] != '\0') {
    Serial.print("DONE ");
    Serial.println(lastCommandId);
  }
}

void rejectCommand(const char *reason) {
  closeGate(false);
  Serial.print("ERR ");
  Serial.println(reason);
}

void handlePing(char *nonce) {
  if (!isHexId(nonce)) {
    rejectCommand("INVALID_PING");
    return;
  }
  Serial.print("READY ");
  Serial.println(nonce);
}

void handleRelease(char *arguments) {
  char *separator = strchr(arguments, ' ');
  if (separator == NULL) {
    rejectCommand("INVALID_RELEASE");
    return;
  }
  *separator = '\0';
  char *durationText = separator + 1;
  if (!isHexId(arguments) || !isDecimal(durationText)) {
    rejectCommand("INVALID_RELEASE");
    return;
  }

  const unsigned long durationMs = strtoul(durationText, NULL, 10);
  if (durationMs < MIN_OPEN_DURATION_MS || durationMs > MAX_OPEN_DURATION_MS) {
    rejectCommand("INVALID_DURATION");
    return;
  }
  if (strcmp(arguments, lastCommandId) == 0) {
    Serial.print("ACK DUPLICATE ");
    Serial.println(arguments);
    return;
  }
  if (gateOpen) {
    rejectCommand("BUSY");
    return;
  }

  memcpy(lastCommandId, arguments, 33);
  gateServo.write(OPEN_ANGLE_DEG);
  gateOpen = true;
  closeDeadline = millis() + durationMs;
  Serial.print("ACK RELEASE ");
  Serial.println(lastCommandId);
}

void handleCommand() {
  commandBuffer[commandLength] = '\0';
  if (commandOverflow) {
    rejectCommand("COMMAND_TOO_LONG");
  } else if (commandLength == 0) {
    // Ignore blank CR/LF separators.
  } else if (strncmp(commandBuffer, "PING ", 5) == 0) {
    handlePing(commandBuffer + 5);
  } else if (strncmp(commandBuffer, "RELEASE ", 8) == 0) {
    handleRelease(commandBuffer + 8);
  } else {
    rejectCommand("UNKNOWN_COMMAND");
  }
  commandLength = 0;
  commandOverflow = false;
}

void setup() {
  gateServo.attach(SERVO_PIN);
  gateServo.write(CLOSED_ANGLE_DEG);
  gateOpen = false;
  Serial.begin(9600);
  Serial.println("READY");
}

void loop() {
  while (Serial.available() > 0) {
    const char incoming = static_cast<char>(Serial.read());
    if (incoming == '\r' || incoming == '\n') {
      handleCommand();
    } else if (!commandOverflow && commandLength < COMMAND_CAPACITY - 1) {
      commandBuffer[commandLength++] = incoming;
    } else {
      commandOverflow = true;
    }
  }

  if (gateOpen && static_cast<long>(millis() - closeDeadline) >= 0) {
    closeGate(true);
  }
}
