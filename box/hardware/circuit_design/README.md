# Circuit Design for the Obedience Box User Interface

## Brief Description
### A Raspberry Pi manages the User Interface:
- 30 switches set the voltage for the mock electric shocks
- 30 LEDs show the user the current voltage setting
- An analog voltmeter shows the user the voltage setting

There may also be a few other UI switches and LEDs in the final design

The above elements will eventually be incorporated into a Raspberry Pi HAT, or otherwise interface with the 40 pin Pi GPIO header.

## Current state:
- Boards for reading the switches and driving the LEDs have been manufactured
- Both boards have been briefly tested by connecting to a Raspberry Pi with jumper wires
- Each board has an initial python library included to interact with the board
  - The python drivers have a demo function included for an example of usage
