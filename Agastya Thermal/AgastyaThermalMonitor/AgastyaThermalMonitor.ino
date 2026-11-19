#include <Wire.h>

// Agastya thermal pretreatment monitor: measurement and timer only.
// This sketch does not drive, regulate, or make a safety decision for a heater.

// ---------- Hardware configuration ----------
const uint8_t LCD_I2C_ADDRESS = 0x27;  // Common PCF8574 backpack address; verify yours.
const uint8_t LCD_BACKLIGHT_BIT = 3;
const uint8_t LCD_ENABLE_BIT = 2;
const uint8_t LCD_READ_WRITE_BIT = 1;
const uint8_t LCD_REGISTER_SELECT_BIT = 0;
const uint8_t LCD_FIRE_GLYPH = 1;

const uint8_t TOOL_TC_CS_PIN = 10;       // MAX6675 chip select, tool/blade probe
const uint8_t INTERFACE_TC_CS_PIN = 9;   // MAX6675 chip select, material/interface probe
const uint8_t TC_CLOCK_PIN = 13;         // MAX6675 SCK
const uint8_t TC_DATA_PIN = 12;          // MAX6675 SO
const uint8_t TIMER_BUTTON_PIN = 2;      // Momentary button from D2 to GND

// Illustrative display values based on legacy thesis language, NOT approved
// operating settings. 200 C is the midpoint of the thesis's proposed 180-220 C
// blade range. 55 seconds is a demo countdown representing its "under a minute"
// claim. The current research treats thermal delamination as optional and these
// values have not been validated in an Agastya physical trial.
const uint16_t THESIS_REFERENCE_TEMP_C = 200;
const uint16_t DEMO_CYCLE_TIME_SECONDS = 55;

const unsigned long SENSOR_INTERVAL_MS = 1000UL;
const unsigned long DISPLAY_PAGE_INTERVAL_MS = 1000UL;
const unsigned long DEBOUNCE_MS = 35UL;
const unsigned long RESET_HOLD_MS = 1500UL;

enum TimerState : uint8_t { TIMER_READY, TIMER_RUNNING, TIMER_PAUSED, TIMER_DONE };

struct ThermocoupleReading {
  bool valid;
  bool openCircuit;
  float celsius;
};

ThermocoupleReading toolReading = {false, false, 0.0f};
ThermocoupleReading interfaceReading = {false, false, 0.0f};
TimerState timerState = TIMER_READY;
unsigned long remainingMs = (unsigned long)DEMO_CYCLE_TIME_SECONDS * 1000UL;
unsigned long timerStartedMs = 0;
unsigned long lastSensorReadMs = 0;
unsigned long lastDisplayMs = 0;
unsigned long buttonPressedAtMs = 0;
unsigned long lastButtonChangeMs = 0;
bool buttonStableState = HIGH;
bool buttonLastRawState = HIGH;
bool buttonHoldHandled = false;
uint8_t displayPage = 0;

// ----------- Minimal PCF8574 / HD44780 LCD driver -----------
void lcdWriteNibble(uint8_t nibble, bool registerSelect) {
  uint8_t output = (nibble & 0x0F) << 4;
  if (registerSelect) output |= (1U << LCD_REGISTER_SELECT_BIT);
  output |= (1U << LCD_BACKLIGHT_BIT);
  Wire.beginTransmission(LCD_I2C_ADDRESS);
  Wire.write(output | (1U << LCD_ENABLE_BIT));
  Wire.endTransmission();
  delayMicroseconds(1);
  Wire.beginTransmission(LCD_I2C_ADDRESS);
  Wire.write(output & ~(1U << LCD_ENABLE_BIT));
  Wire.endTransmission();
  delayMicroseconds(50);
}

void lcdSend(uint8_t value, bool registerSelect) {
  lcdWriteNibble(value >> 4, registerSelect);
  lcdWriteNibble(value & 0x0F, registerSelect);
}

void lcdCommand(uint8_t command) {
  lcdSend(command, false);
  if (command == 0x01 || command == 0x02) delayMicroseconds(1800);
}

void lcdCreateChar(uint8_t location, const uint8_t glyph[8]) {
  lcdCommand(0x40 | ((location & 0x07) << 3));
  for (uint8_t row = 0; row < 8; ++row) lcdSend(glyph[row], true);
}

void lcdBegin() {
  delay(50);
  lcdWriteNibble(0x03, false);
  delay(5);
  lcdWriteNibble(0x03, false);
  delayMicroseconds(150);
  lcdWriteNibble(0x03, false);
  lcdWriteNibble(0x02, false);
  lcdCommand(0x28);  // 4-bit, 2-line, 5x8 font
  lcdCommand(0x0C);  // Display on, cursor off
  lcdCommand(0x06);  // Increment cursor
  lcdCommand(0x01);
}

void lcdSetCursor(uint8_t column, uint8_t row) {
  const uint8_t rowAddress[] = {0x00, 0x40};
  lcdCommand(0x80 | (rowAddress[row & 1] + column));
}

void lcdPrintLine(uint8_t row, const char *text) {
  lcdSetCursor(0, row);
  for (uint8_t i = 0; i < 16; ++i) {
    char c = text[i];
    lcdSend(c == '\0' ? ' ' : (uint8_t)c, true);
    if (c == '\0') {
      for (++i; i < 16; ++i) lcdSend(' ', true);
      break;
    }
  }
}

void makeTimerLine(char *line, const char *timeText) {
  snprintf(line, 17, "LEFT %s", timeText);
  uint8_t length = (uint8_t)strlen(line);
  if (timerState == TIMER_RUNNING) {
    line[length++] = ' ';
    line[length++] = LCD_FIRE_GLYPH;
    line[length++] = ' ';
    line[length++] = 'R';
    line[length++] = 'U';
    line[length++] = 'N';
  } else if (timerState == TIMER_PAUSED) {
    strcat(line, " PAUSE");
  } else if (timerState == TIMER_DONE) {
    strcat(line, " DONE");
  } else {
    strcat(line, " RDY");
  }
}

// ----------- MAX6675 reader (no third-party library required) -----------
ThermocoupleReading readMax6675(uint8_t chipSelectPin) {
  ThermocoupleReading result = {false, false, 0.0f};
  digitalWrite(chipSelectPin, HIGH);
  delayMicroseconds(2);
  digitalWrite(chipSelectPin, LOW);
  delayMicroseconds(2);

  uint16_t raw = 0;
  for (uint8_t bit = 0; bit < 16; ++bit) {
    digitalWrite(TC_CLOCK_PIN, HIGH);
    raw <<= 1;
    if (digitalRead(TC_DATA_PIN)) raw |= 1;
    digitalWrite(TC_CLOCK_PIN, LOW);
  }
  digitalWrite(chipSelectPin, HIGH);

  result.openCircuit = (raw & 0x0004) != 0;
  if (result.openCircuit) return result;

  // D14..D3 contain the temperature in 0.25 C increments.
  uint16_t quarterDegrees = (raw >> 3) & 0x0FFF;
  result.celsius = quarterDegrees * 0.25f;
  result.valid = true;
  return result;
}

void refreshSensors(unsigned long now) {
  if (now - lastSensorReadMs < SENSOR_INTERVAL_MS) return;
  lastSensorReadMs = now;
  toolReading = readMax6675(TOOL_TC_CS_PIN);
  interfaceReading = readMax6675(INTERFACE_TC_CS_PIN);
}

// ----------- Timer and button -----------
unsigned long currentRemainingMs(unsigned long now) {
  if (timerState == TIMER_RUNNING) {
    unsigned long elapsed = now - timerStartedMs;
    return elapsed >= remainingMs ? 0 : remainingMs - elapsed;
  }
  return remainingMs;
}

void toggleTimer(unsigned long now) {
  if (timerState == TIMER_READY) {
    timerStartedMs = now;
    timerState = TIMER_RUNNING;
  } else if (timerState == TIMER_RUNNING) {
    remainingMs = currentRemainingMs(now);
    timerState = remainingMs == 0 ? TIMER_DONE : TIMER_PAUSED;
  } else if (timerState == TIMER_PAUSED) {
    timerStartedMs = now;
    timerState = TIMER_RUNNING;
  } else {
    remainingMs = (unsigned long)DEMO_CYCLE_TIME_SECONDS * 1000UL;
    timerState = TIMER_READY;
  }
}

void resetTimer() {
  remainingMs = (unsigned long)DEMO_CYCLE_TIME_SECONDS * 1000UL;
  timerState = TIMER_READY;
}

void updateButton(unsigned long now) {
  bool rawState = digitalRead(TIMER_BUTTON_PIN);
  if (rawState != buttonLastRawState) {
    buttonLastRawState = rawState;
    lastButtonChangeMs = now;
  }

  if (now - lastButtonChangeMs >= DEBOUNCE_MS && rawState != buttonStableState) {
    buttonStableState = rawState;
    if (buttonStableState == LOW) {
      buttonPressedAtMs = now;
      buttonHoldHandled = false;
    } else if (!buttonHoldHandled) {
      toggleTimer(now);
    }
  }

  if (buttonStableState == LOW && !buttonHoldHandled &&
      now - buttonPressedAtMs >= RESET_HOLD_MS) {
    resetTimer();
    buttonHoldHandled = true;
  }
}

void updateTimerCompletion(unsigned long now) {
  if (timerState == TIMER_RUNNING && currentRemainingMs(now) == 0) {
    remainingMs = 0;
    timerState = TIMER_DONE;
  }
}

// ----------- Display formatting -----------
void formatCountdown(unsigned long totalSeconds, char *destination) {
  unsigned long minutes = totalSeconds / 60UL;
  unsigned long seconds = totalSeconds % 60UL;
  if (minutes > 99) minutes = 99;
  snprintf(destination, 6, "%02lu:%02lu", minutes, seconds);
}

void formatTemperature(const ThermocoupleReading &reading, char *destination) {
  if (!reading.valid) {
    strcpy(destination, reading.openCircuit ? "OPEN" : "ERROR");
  } else {
    int rounded = (int)(reading.celsius + 0.5f);
    snprintf(destination, 6, "%3dC", rounded);
  }
}

const char *timerLabel() {
  switch (timerState) {
    case TIMER_READY: return "READY";
    case TIMER_RUNNING: return "RUNNING";
    case TIMER_PAUSED: return "PAUSED";
    case TIMER_DONE: return "DONE";
  }
  return "ERROR";
}

void renderDisplay(unsigned long now) {
  char line1[17] = "";
  char line2[17] = "";
  char toolTemp[6];
  char interfaceTemp[6];
  char timeText[6];
  formatTemperature(toolReading, toolTemp);
  formatTemperature(interfaceReading, interfaceTemp);
  formatCountdown(currentRemainingMs(now) / 1000UL, timeText);

  if (displayPage == 0) {
    snprintf(line1, sizeof(line1), "T:%s REF:%uC", toolTemp, THESIS_REFERENCE_TEMP_C);
  } else {
    snprintf(line1, sizeof(line1), "IFACE:%s", interfaceTemp);
  }
  makeTimerLine(line2, timeText);
  lcdPrintLine(0, line1);
  lcdPrintLine(1, line2);
}

void setup() {
  pinMode(TOOL_TC_CS_PIN, OUTPUT);
  pinMode(INTERFACE_TC_CS_PIN, OUTPUT);
  digitalWrite(TOOL_TC_CS_PIN, HIGH);
  digitalWrite(INTERFACE_TC_CS_PIN, HIGH);
  pinMode(TC_CLOCK_PIN, OUTPUT);
  digitalWrite(TC_CLOCK_PIN, LOW);
  pinMode(TC_DATA_PIN, INPUT);
  pinMode(TIMER_BUTTON_PIN, INPUT_PULLUP);

  Wire.begin();
  lcdBegin();
  const uint8_t fireGlyph[8] = {
    0x04, 0x06, 0x0C, 0x0E, 0x1E, 0x1F, 0x0E, 0x04
  };
  lcdCreateChar(LCD_FIRE_GLYPH, fireGlyph);
  lcdPrintLine(0, "AGASTYA THERMAL");
  lcdPrintLine(1, "MONITOR ONLY");
  delay(1200);
  lastSensorReadMs = millis() - SENSOR_INTERVAL_MS;
}

void loop() {
  unsigned long now = millis();
  updateButton(now);
  refreshSensors(now);
  updateTimerCompletion(now);

  if (now - lastDisplayMs >= DISPLAY_PAGE_INTERVAL_MS) {
    lastDisplayMs = now;
    displayPage = (displayPage + 1) % 2;
    renderDisplay(now);
  }
}
