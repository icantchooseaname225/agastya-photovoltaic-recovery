# Agastya process walkthroughs

Open index.html for a four-stage conceptual animation. The stage labels follow the current project architecture: Stage 1 inspection/routing, Stage 2 manual mechanical preparation, Stage 3 thermal treatment/delamination, and Stage 4 silver removal/recovery. Stage 4's method, feed preparation, product form, and receiving criteria remain open. Sampling, assay, and mass accounting validate every stage.

The walkthrough shows proposed material movement. It is not a physics simulation, validated machine design, throughput estimate, thermal/energy calculation, safety system, or recovery prediction. Stage 3's depicted output is front glass plus cell/EVA/backsheet laminate; it does not establish EVA-free cells. Stage 4 appears as a route-selection gate, with no separation mechanism or output invented.

A separate 3D kinematic concept is available in machine.html. It illustrates the same four stages. Neither view is evidence that equipment was built, tested, or operated.

The associated Python/NumPy datasets are described in the Agastya Physics Simulation guide. Their 200,080 rows are historical virtual scenarios and model time histories; the former size-classification “Stage 4” rows do not model current Stage 4 silver removal.

## Free cloud monitor demonstration: Wokwi

The Wokwi folder contains an Arduino Uno and LCD mock-up of the Stage 3 temperature-display/timer interface. Open https://wokwi.com/projects/new/arduino-uno, select the Code tab, and replace the default sketch with Wokwi/sketch.ino. In the diagram editor, replace the diagram with Wokwi/diagram.json, then start the simulation. Turn the two potentiometers to adjust illustrative tool/interface temperatures; press the green button to start, pause, resume, or reset the demonstration timer.

Wokwi does not model the project's MAX6675/K-type thermocouple measurement chain in this circuit. Potentiometers are simulated inputs, neither input is calibrated, and the shortened timer is for demonstration only. The sketch does not drive a heater or perform a safety function. The physical Stage 3 monitor design in Agastya Thermal/AgastyaThermalMonitor is a separate proposal.

Open the HTML pages locally for the visual walkthroughs. They do not solve process physics or control machinery.
