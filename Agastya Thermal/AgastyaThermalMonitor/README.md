# Agastya thermal monitor LCD sketch

This Arduino sketch reads two K-type thermocouples through MAX6675 modules and shows tool temperature, interface temperature, a thesis reference temperature, and a manually controlled countdown on a 16x2 I2C LCD. It is a measurement and timer display only. It has no heater output, heater regulation, interlock, alarm, or safety function.

## Illustrative display values and project context

- `THESIS_REFERENCE_TEMP_C = 200` is the midpoint of the legacy thesis's proposed 180-220 C blade range. It is labeled as a reference on screen; it is not an approved heater setting.
- `DEMO_CYCLE_TIME_SECONDS = 55` is an invented demonstration countdown representing the thesis's "under a minute" concept. Literature benchmarks are about 50 seconds/module (IEA) and 60 seconds/panel (NPC), but those are external process references, not Agastya trial data.
- The thesis's immediately following heated roller / EVA-stripping claim is unvalidated. The display does not claim that the roller step is happening or that the laminate reaches any particular temperature.
- Research records document desk study and numerical thermal modelling only; no physical thermal trial is recorded. The current project architecture assigns thermal delamination to Stage 3, using a hot-knife as a literature-based reference concept. The monitor remains a display/timer proposal and does not validate or control that process.

These values let the LCD demonstrate realistic information flow. Replace them only through a supervisor-reviewed test plan when an actual experiment has approved conditions; do not treat the demo values as validated process settings.

## Assumed hardware

- Arduino Uno or Nano (ATmega328P, 5 V)
- 16x2 HD44780-compatible LCD with PCF8574 I2C backpack (default address `0x27`)
- Two MAX6675 modules and K-type probes: one mounted to the tool and one to the material/interface
- Momentary normally-open button between D2 and GND

The display backpack pin mapping is the common PCF8574 layout: P0=RS, P1=R/W, P2=E, P3=backlight, P4..P7=D4..D7. Some backpack boards use another mapping. The code uses only Arduino's built-in `Wire` library and has no library-manager dependencies.

## Pin map

| Arduino | Connection |
|---|---|
| A4 / SDA | LCD SDA |
| A5 / SCL | LCD SCL |
| D10 | Tool MAX6675 CS |
| D9 | Interface MAX6675 CS |
| D13 | Both MAX6675 SCK |
| D12 | Both MAX6675 SO |
| D2 | Timer button to GND |
| 5V / GND | Modules and LCD, according to module ratings |

Use separate chip-select lines for the two MAX6675 boards. Check the actual board pin labels and supply requirements before wiring. On some LCD backpacks, powering from 5 V while connecting I2C to a 3.3 V controller requires level shifting.

## Timer operation and LCD pages

- The display updates once per second. It alternates between the measured tool temperature plus thesis reference, and the measured material/interface temperature. Both pages show the countdown and timer state.
- A custom flame glyph appears beside the countdown while the timer is running. It is only a visual timer indicator, not a flame sensor or heater status.
- A short press starts the timer, pauses it, resumes it, or returns a completed timer to READY.
- Hold the button for 1.5 seconds to reset to READY.
- The timer is a manual elapsed-time aid. It does not start/stop heating, persist across power loss, or indicate that a process is safe or complete.
- The 55-second default is for demonstration only. It is not a recorded trial duration.
- `THESIS_REFERENCE_TEMP_C` is a visual reference only, never a heater setpoint.

The LCD alternates every 2.5 seconds between temperatures and remaining timer. `OPEN` indicates the MAX6675 thermocouple-open fault bit; `ERROR` means the reading is invalid. Check the sensor and wiring. The MAX6675 range is finite and this display is not a calibrated or independent over-temperature instrument.

## Build

Open `AgastyaThermalMonitor.ino` in Arduino IDE and select **Arduino Uno** (or the matching ATmega328P board). Compile before wiring or using any thermal equipment. The timer and temperature display do not replace the lab's equipment review, independent over-temperature protection, guarding, or emergency stop.
