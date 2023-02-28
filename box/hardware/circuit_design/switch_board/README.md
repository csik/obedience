# Switch Reader Board Set

### Meant to be used as a set of two identical boards
- Each board can read up to 16 switches
- The first board connects to the Raspberry Pi
- The second is daisy chained with a jumper
- Besides the 30 main Milgram voltage switches, 4 auxilliary switches are available on the second board
- A small `3V3 OK` LED on the board illuminates when the board has power
- Note that you don't need to solder every switch lug, only 1 of the switch poles is wired

### The I2C addresses must be set with solder jumpers
- These jumpers make up the low 3-bits of the binary address for each PC9555 chip
- The most likely pattern, looking from left to right is: `0b010, 0b011, 0b000, 0b001`
  - this matches the addresses in the demo function of `[0x20, 0x21, 0x22, 0x23]`
- Valid addresses for the chips are in `[0x20..0x27]`
  - the `2` in the upper byte is fixed, and the lower byte can be changed 
- Other addresses are possible if more I2C devices are added and there is an address collision

### View from the back
![](./docs/2D/connections.png)
