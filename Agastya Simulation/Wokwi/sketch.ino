#include <LiquidCrystal.h>

// Wokwi teaching model of the Agastya Stage 3 display/timer.
// A0/A1 potentiometers stand in for temperatures because this simulation
// does not model K-type probes or MAX6675 thermocouple interfaces.
// This is monitor/timer behavior only; it has no heater control or safety role.

LiquidCrystal lcd(12, 11, 5, 4, 3, 2); // RS, E, D4, D5, D6, D7
const int TOOL_SIM_PIN = A0;
const int INTERFACE_SIM_PIN = A1;
const int BUTTON_PIN = 7;
const unsigned long DEMO_CYCLE_MS = 60000UL; // 60-second demonstration cycle

enum TimerState { READY, RUNNING, PAUSED, DONE };
TimerState state = READY;
unsigned long remainingMs = DEMO_CYCLE_MS;
unsigned long startedAt = 0;
unsigned long lastRefresh = 0;
unsigned long lastPress = 0;
bool buttonWasHigh = true;
bool page = false;

int simulatedC(int pin) {
  return map(analogRead(pin), 0, 1023, 20, 350);
}

void buttonAction(unsigned long now) {
  if (state == READY) { state = RUNNING; startedAt = now; }
  else if (state == RUNNING) {
    unsigned long elapsed = now - startedAt;
    remainingMs = elapsed >= remainingMs ? 0 : remainingMs - elapsed;
    state = remainingMs == 0 ? DONE : PAUSED;
  } else if (state == PAUSED) { state = RUNNING; startedAt = now; }
  else { remainingMs = DEMO_CYCLE_MS; state = READY; }
}

unsigned long timeLeft(unsigned long now) {
  if (state != RUNNING) return remainingMs;
  unsigned long elapsed = now - startedAt;
  return elapsed >= remainingMs ? 0 : remainingMs - elapsed;
}

const char* stateName() {
  switch (state) {
    case READY: return "READY";
    case RUNNING: return "RUNNING";
    case PAUSED: return "PAUSED";
    case DONE: return "DONE";
  }
  return "ERROR";
}

void draw(unsigned long now) {
  char line[17];
  lcd.clear();
  if (!page) {
    snprintf(line, sizeof(line), "TOOL:%3dC", simulatedC(TOOL_SIM_PIN));
    lcd.setCursor(0, 0); lcd.print(line);
    snprintf(line, sizeof(line), "IFACE:%3dC", simulatedC(INTERFACE_SIM_PIN));
    lcd.setCursor(0, 1); lcd.print(line);
  } else {
    unsigned long seconds = timeLeft(now) / 1000UL;
    snprintf(line, sizeof(line), "LEFT %02lu:%02lu", seconds / 60UL, seconds % 60UL);
    lcd.setCursor(0, 0); lcd.print(line);
    lcd.setCursor(0, 1); lcd.print(stateName()); lcd.print("  BTN=GO");
  }
}

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  lcd.begin(16, 2);
  lcd.setCursor(0, 0); lcd.print("AGASTYA STAGE 3");
  lcd.setCursor(0, 1); lcd.print("SIM / MONITOR");
  delay(1000);
  draw(millis());
}

void loop() {
  unsigned long now = millis();
  bool high = digitalRead(BUTTON_PIN);
  if (buttonWasHigh && !high && now - lastPress > 180) {
    buttonAction(now);
    lastPress = now;
  }
  buttonWasHigh = high;
  if (state == RUNNING && timeLeft(now) == 0) {
    remainingMs = 0;
    state = DONE;
  }
  if (now - lastRefresh >= 700) {
    lastRefresh = now;
    page = !page;
    draw(now);
  }
}
