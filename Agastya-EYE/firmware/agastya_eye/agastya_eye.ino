#include <Arduino.h>
#include <HTTPClient.h>
#include <Preferences.h>
#include <math.h>
#include <stdlib.h>
#include <WiFi.h>
#include <esp_camera.h>
#include <time.h>

#include "secrets.h"
#include <Adafruit_INA219.h>
#include "sensor_adapter.h"

static const char *API_PATH = "/api/v1/inspections";
static const char *TIMEZONE_RULE = "UTC0";
static Preferences preferences;
static String panelReference;
static String panelTechnology = "unknown";
static String junctionBoxLocation = "unknown";
static String captureView = "front";
static String serialLine;
static float frameWidthMm = 0.0f;
static float frameHeightMm = 0.0f;
static float ratedPowerW = 0.0f;
static bool cameraReady = false;

static camera_config_t cameraConfig() {
  camera_config_t config = {};
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = 5;
  config.pin_d1 = 18;
  config.pin_d2 = 19;
  config.pin_d3 = 21;
  config.pin_d4 = 36;
  config.pin_d5 = 39;
  config.pin_d6 = 34;
  config.pin_d7 = 35;
  config.pin_xclk = 0;
  config.pin_pclk = 22;
  config.pin_vsync = 25;
  config.pin_href = 23;
  config.pin_sccb_sda = 26;
  config.pin_sccb_scl = 27;
  config.pin_pwdn = 32;
  config.pin_reset = -1;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = psramFound() ? FRAMESIZE_UXGA : FRAMESIZE_SVGA;
  config.jpeg_quality = psramFound() ? 10 : 12;
  config.fb_count = 1;
  config.fb_location = psramFound() ? CAMERA_FB_IN_PSRAM : CAMERA_FB_IN_DRAM;
  config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  return config;
}

static bool connectNetwork() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  const unsigned long started = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - started < 30000) {
    delay(400);
    Serial.print('.');
  }
  Serial.println();
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wi-Fi connection failed; restart the board after checking secrets.h");
    return false;
  }
  Serial.print("Wi-Fi connected; device address: ");
  Serial.println(WiFi.localIP());
  configTzTime(TIMEZONE_RULE, "pool.ntp.org", "time.nist.gov");
  return true;
}

static String utcTimestamp() {
  const time_t now = time(nullptr);
  if (now < 1700000000) return "";
  struct tm utc;
  gmtime_r(&now, &utc);
  char value[25];
  strftime(value, sizeof(value), "%Y-%m-%dT%H:%M:%SZ", &utc);
  return String(value);
}

static String requestId() {
  char value[33];
  snprintf(value, sizeof(value), "%08lx%08lx%08lx%08lx",
           (unsigned long)esp_random(), (unsigned long)esp_random(),
           (unsigned long)esp_random(), (unsigned long)esp_random());
  return String(value);
}

static void addNumberHeader(HTTPClient &http, const char *name, float value) {
  char text[24];
  snprintf(text, sizeof(text), "%.5f", value);
  http.addHeader(name, text);
}

static void captureAndSend() {
  if (!cameraReady) {
    Serial.println("Camera is not initialized; check setup messages and restart the board");
    return;
  }
  if (WiFi.status() != WL_CONNECTED && !connectNetwork()) return;
  if ((frameWidthMm > 0.0f) != (frameHeightMm > 0.0f)) {
    Serial.println("Record both width and height, or clear both, before capture");
    return;
  }
  camera_fb_t *frame = esp_camera_fb_get();
  if (frame == nullptr) {
    Serial.println("Camera capture failed");
    return;
  }

  const ElectricalSample sample = readElectricalSample();
  const String url = String(LAPTOP_BASE_URL) + API_PATH;
  const String idempotencyKey = requestId();
  const String capturedAt = utcTimestamp();
  bool completed = false;

  for (int attempt = 1; attempt <= 3 && !completed; ++attempt) {
    WiFiClient client;
    HTTPClient http;
    http.setTimeout(20000);
    if (!http.begin(client, url)) {
      Serial.println("Could not open laptop API connection");
      break;
    }
    http.addHeader("Content-Type", "image/jpeg");
    http.addHeader("Authorization", String("Bearer ") + DEVICE_TOKEN);
    http.addHeader("X-Device-ID", DEVICE_ID);
    http.addHeader("X-Request-ID", idempotencyKey);
    http.addHeader("X-Camera-Modality", "visible_rgb");
    http.addHeader("X-Camera-Sensor-ID", DEVICE_ID);
    http.addHeader("X-Capture-View", captureView);
    http.addHeader("X-Electrical-Test", sample.testStatus);
    http.addHeader("X-Panel-Technology", panelTechnology);
    http.addHeader("X-Junction-Box", junctionBoxLocation);
    if (panelReference.length()) http.addHeader("X-Panel-Ref", panelReference);
    if (frameWidthMm > 0.0f) addNumberHeader(http, "X-Frame-Width-MM", frameWidthMm);
    if (frameHeightMm > 0.0f) addNumberHeader(http, "X-Frame-Height-MM", frameHeightMm);
    if (ratedPowerW > 0.0f) addNumberHeader(http, "X-Rated-Power-W", ratedPowerW);
    if (capturedAt.length()) http.addHeader("X-Captured-At", capturedAt);
    if (sample.hasVoltage) addNumberHeader(http, "X-Voltage-V", sample.voltageV);
    if (sample.hasCurrent) addNumberHeader(http, "X-Current-A", sample.currentA);
    if (sample.hasPower) addNumberHeader(http, "X-Power-W", sample.powerW);

    const int status = http.POST(frame->buf, frame->len);
    const String response = http.getString();
    Serial.printf("Laptop API response (%d):\n", status);
    Serial.println(response);
    completed = status == HTTP_CODE_CREATED || status == HTTP_CODE_OK;
    http.end();
    const bool retryable = status <= 0 || status == 429 || status >= 500;
    if (!completed && retryable && attempt < 3) delay(1200 * attempt);
    if (!completed && !retryable) break;
  }

  if (!completed) Serial.printf("Upload failed; request id %s\n", idempotencyKey.c_str());
  esp_camera_fb_return(frame);
}

static void handleCommand(String command) {
  command.trim();
  if (command == "capture") {
    captureAndSend();
    return;
  }
  if (command.startsWith("panel=")) {
    String nextReference = command.substring(6);
    nextReference.trim();
    const bool clearReference = nextReference == "clear";
    if (clearReference) nextReference = "";
    const bool changedPanel = nextReference != panelReference;
    panelReference = nextReference;
    preferences.putString("panel_ref", panelReference);
    if (changedPanel || clearReference) {
      panelTechnology = "unknown";
      frameWidthMm = 0.0f;
      frameHeightMm = 0.0f;
      junctionBoxLocation = "unknown";
      preferences.putString("panel_tech", panelTechnology);
      preferences.putFloat("frame_width", frameWidthMm);
      preferences.putFloat("frame_height", frameHeightMm);
      ratedPowerW = 0.0f;
      preferences.putFloat("rated_power", ratedPowerW);
      preferences.putString("junction_box", junctionBoxLocation);
    }
    Serial.printf("Panel reference: %s\n", panelReference.length() ? panelReference.c_str() : "(new ID per capture)");
    return;
  }
  if (command.startsWith("tech=")) {
    const String value = command.substring(5);
    if (value != "unknown" && value != "c_si" && value != "thin_film" && value != "other") {
      Serial.println("Technology must be unknown, c_si, thin_film, or other");
      return;
    }
    panelTechnology = value;
    preferences.putString("panel_tech", panelTechnology);
    Serial.printf("Panel technology: %s\n", panelTechnology.c_str());
    return;
  }
  if (command.startsWith("width=") || command.startsWith("height=")) {
    const bool isWidth = command.startsWith("width=");
    String value = command.substring(isWidth ? 6 : 7);
    value.trim();
    float measurement = 0.0f;
    if (value != "clear") {
      char *end = nullptr;
      measurement = strtof(value.c_str(), &end);
      if (end == value.c_str() || *end != '\0' || !isfinite(measurement)
          || measurement < 10.0f || measurement > 5000.0f) {
        Serial.println("Frame dimensions must be 10..5000 mm, or use clear");
        return;
      }
    }
    if (isWidth) {
      frameWidthMm = measurement;
      preferences.putFloat("frame_width", frameWidthMm);
    } else {
      frameHeightMm = measurement;
      preferences.putFloat("frame_height", frameHeightMm);
    }
    Serial.printf("Frame %s: %.1f mm\n", isWidth ? "width" : "height", measurement);
    return;
  }
  if (command.startsWith("rated=")) {
    String value = command.substring(6);
    value.trim();
    float measurement = 0.0f;
    if (value != "clear") {
      char *end = nullptr;
      measurement = strtof(value.c_str(), &end);
      if (end == value.c_str() || *end != '\0' || !isfinite(measurement)
          || measurement < 1.0f || measurement > 5000.0f) {
        Serial.println("Nameplate power must be 1..5000 W, or use clear");
        return;
      }
    }
    ratedPowerW = measurement;
    preferences.putFloat("rated_power", ratedPowerW);
    Serial.printf("Nameplate power: %.1f W\n", ratedPowerW);
    return;
  }
  if (command.startsWith("junction=")) {
    const String value = command.substring(9);
    if (value != "unknown" && value != "rear_center" && value != "rear_upper"
        && value != "rear_lower" && value != "rear_left" && value != "rear_right"
        && value != "other") {
      Serial.println("Junction box must be unknown, rear_center, rear_upper, rear_lower, rear_left, rear_right, or other");
      return;
    }
    junctionBoxLocation = value;
    preferences.putString("junction_box", junctionBoxLocation);
    Serial.printf("Junction box: %s\n", junctionBoxLocation.c_str());
    return;
  }
  if (command.startsWith("view=")) {
    const String value = command.substring(5);
    if (value != "front" && value != "rear_nameplate" && value != "rear_junction_box"
        && value != "rear_overview" && value != "unspecified") {
      Serial.println("View must be front, rear_nameplate, rear_junction_box, rear_overview, or unspecified");
      return;
    }
    captureView = value;
    preferences.putString("capture_view", captureView);
    Serial.printf("Capture view: %s\n", captureView.c_str());
    return;
  }
  if (command == "status") {
    Serial.printf("Device: %s | Wi-Fi: %s | Panel: %s | View: %s | Technology: %s | Frame: %.1f x %.1f mm | Nameplate: %.1f W | J-box: %s\n", DEVICE_ID,
                  WiFi.status() == WL_CONNECTED ? "connected" : "offline",
                  panelReference.length() ? panelReference.c_str() : "unassigned",
                  captureView.c_str(), panelTechnology.c_str(), frameWidthMm, frameHeightMm, ratedPowerW, junctionBoxLocation.c_str());
    return;
  }
  Serial.println("Commands: capture | panel=<ref>|clear | view=front|rear_nameplate|rear_junction_box|rear_overview|unspecified | tech=unknown|c_si|thin_film|other | width=<mm>|clear | height=<mm>|clear | rated=<W>|clear | junction=<location> | status");
}

void setup() {
  Serial.begin(115200);
  delay(500);
  preferences.begin("agastya-eye", false);
  panelReference = preferences.getString("panel_ref", "");
  panelTechnology = preferences.getString("panel_tech", "unknown");
  frameWidthMm = preferences.getFloat("frame_width", 0.0f);
  frameHeightMm = preferences.getFloat("frame_height", 0.0f);
  ratedPowerW = preferences.getFloat("rated_power", 0.0f);
  junctionBoxLocation = preferences.getString("junction_box", "unknown");
  captureView = preferences.getString("capture_view", "front");

  camera_config_t config = cameraConfig();
  const esp_err_t cameraResult = esp_camera_init(&config);
  if (cameraResult != ESP_OK) {
    Serial.printf("Camera initialization failed: 0x%x\n", cameraResult);
    return;
  }
  cameraReady = true;
  Serial.printf("INA219 adapter: %s (telemetry only; never a pass/fail test)\n",
                initializeElectricalAdapter() ? "detected" : "not detected / not installed");
  Serial.println("Agastya-EYE device ready. Send 'capture' in Serial Monitor.");
  Serial.printf("Stored panel reference: %s\n", panelReference.length() ? panelReference.c_str() : "(none)");
  if (!connectNetwork()) {
    Serial.println("Camera is ready; upload will retry Wi-Fi when you send 'capture'.");
  }
}

void loop() {
  while (Serial.available()) {
    const char character = (char)Serial.read();
    if (character == '\n' || character == '\r') {
      if (serialLine.length()) handleCommand(serialLine);
      serialLine = "";
    } else if (serialLine.length() < 140) {
      serialLine += character;
    }
  }
  delay(10);
}
