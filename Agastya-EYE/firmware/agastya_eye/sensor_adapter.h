#pragma once

#include <math.h>

#ifndef AGASTYA_ENABLE_INA219
#define AGASTYA_ENABLE_INA219 1
#endif

#if AGASTYA_ENABLE_INA219
#include <Wire.h>
#include <Adafruit_INA219.h>
#define AGASTYA_HAS_INA219 1
#ifndef AGASTYA_INA219_I2C_ADDRESS
#define AGASTYA_INA219_I2C_ADDRESS 0x41
#endif
#else
#define AGASTYA_HAS_INA219 0
#endif

struct ElectricalSample {
  const char *testStatus;
  bool hasVoltage;
  float voltageV;
  bool hasCurrent;
  float currentA;
  bool hasPower;
  float powerW;
};

// Optional low-voltage demo sensor. Readings never establish a pass/fail result.
#if AGASTYA_HAS_INA219
static Adafruit_INA219 agastyaIna219(AGASTYA_INA219_I2C_ADDRESS);
static bool agastyaIna219Initialized = false;
static bool agastyaIna219Available = false;

inline bool initializeElectricalAdapter() {
  if (!agastyaIna219Initialized) {
    Wire.begin(13, 14);  // AI Thinker ESP32-CAM; shared with microSD.
    agastyaIna219Available = agastyaIna219.begin();
    if (agastyaIna219Available) agastyaIna219.setCalibration_16V_400mA();
    agastyaIna219Initialized = true;
  }
  return agastyaIna219Available;
}
#else
inline bool initializeElectricalAdapter() { return false; }
#endif

inline ElectricalSample readElectricalSample() {
#if AGASTYA_HAS_INA219
  if (initializeElectricalAdapter()) {
    const float voltage = agastyaIna219.getBusVoltage_V();
    const float current = agastyaIna219.getCurrent_mA() / 1000.0f;
    const float power = agastyaIna219.getPower_mW() / 1000.0f;
    if (isfinite(voltage) && isfinite(current) && isfinite(power)
        && voltage >= 0 && current >= 0 && power >= 0) {
      return {"not_tested", true, voltage, true, current, true, power};
    }
  }
#endif
  return {"not_tested", false, 0.0f, false, 0.0f, false, 0.0f};
}
