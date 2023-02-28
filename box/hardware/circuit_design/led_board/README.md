# LED Driver Board Set

### Meant to be used as a set of two identical boards
- Each board can drive up to 16 LEDs
- The first board connects to the Raspberry Pi
- The second is daisy chained with a jumper
- Besides the 30 main Milgram voltage LEDs, 2 auxilliary LEDs are available on the second board
- A small `3V3 OK` LED on the board illuminates when the board has power

### An optional `VBUS` connection is available for driving the LEDS with a different DC voltage source
- Select the DC voltage source with a solder jumper
- The `3V3` setting is typical
- The `VBUS` setting is included in case there are issues with driving the LEDs from the Raspberry Pi power supply
- Note that the `VBUS OK` LED will only light up if there is a DC source connected to `VBUS`
  - it is normal for this LED to be dim if using the `3V3` DC source

### View from the back
![](./docs/2D/connections.png)
