#!/usr/bin/env python

'''
Prereqs:
- enable I2C in /boot/config.txt, uncomment dtparam=i2c_arm=on
- install some I2C utilities
    - sudo apt install -y i2c-tools python3-smbus

- to check the I2C busses:
    - ls /dev/*i2c*
    - you should see /dev/i2c-1 in there

- to check that the I2C devices exist and get its address:
    - sudo i2cdetect -y 1
    - you should see the address of the I2C devices on the bus in the grid
'''
import time
import smbus


class UI_Switches:
    '''
    User Interface Switches.

    32 switches are read with two PCA9555D GPIO expander chips on the I2C bus.

    PCA9555D[0] handles switches 0..15
    PCA9555D[1] handles switches 16..31

    Requires:
      - Shared use of I2C bus.
    '''
    NUM_SWITCHES = 32 # total number of switches
    NUM_V_SWITCHES = 30 # just the voltage switches
    V_SWITCH_MASK = 0x3FFF_FFFF # binary mask to extract just the voltage switches

    INPUT_PORT_0 = 0
    INPUT_PORT_1 = 1

    def __init__(self, bus, addr_0_15, addr_16_31) -> None:
        '''
        Initialize the UI Switches with the given I2C bus object and addresses
        of the two PCA9555D I2C chips.

        Args:
            bus: the I2C device to use
            addr_0_15  (int): the I2C address of PCA9555D[0]
            addr_16_31 (int): the I2C address of PCA9555D[1]
        '''
        self.bus = bus
        self.addr_0_15 = addr_0_15
        self.addr_16_31 = addr_16_31

        self.cached_read = self.read_multi()

    def _read_bank(self, addr: int) -> int:
        '''
        `_read_bank(addr)` the switches in a single PCA9555D bank at I2c address
        `addr` as one 16 bit word.

        Args:
            `addr`: the address of the chip to read.

        Raises:
            OSError if there is a communication error with either of the PCA9555D
        '''
        bits_0_to_7 = self.bus.read_byte_data(
            addr,
            self.INPUT_PORT_0
        )
        bits_8_to_15 = self.bus.read_byte(addr)

        return bits_8_to_15 << 8 | bits_0_to_7

    def read_multi(self) -> int:
        '''
        `read_multi()` is the value of all switches at once as a 32 bit word 
        where switch 0 is the LSB and switch 31 is the MSB.

        Examples:
            - no switches are on -> 0x0000_0000
            - switch 0 is on -> 0x0000_0001
            - switches 2, 5, 19, and 30 are on -> 0x4008_0024

        Raises:
            OSError if there is a communication error with either of the PCA9555D
        '''
        bits_0_15 = self._read_bank(self.addr_0_15)
        bits_16_31 = self._read_bank(self.addr_16_31)

        self.cached_read = bits_16_31 << 16 | bits_0_15

        return self.cached_read

    def read_single(self, switch_num: int) -> int:
        '''
        `read_single(switch_num)` the integer value 0 or 1 of the switch at 
        position `switch_num`.

        Args:
            `switch_num` (int): the switch number to read, in [0..31]

        Raises:
            OSError if there is a communication error with either of the PCA9555D
        '''
        if not 0 <= switch_num <= 31:
            return 0
        return (self.read_multi() >> switch_num) & 1

    def get_shock_level(self) -> int:
        '''
        `get_shock_level()` is the position of the highest "on" voltage switch.
        A result of 0 means that none of the switches are on. A result of an 
        integer `n` in the range [1..30] means that `n` is the highest of
        the switches that are currently in the "on" position. The returned value 
        is one-higher than the bit position of the highest switch, to account
        for the zero setting where no switches are on.

        Examples:
            - all switches are off -> 0
            - switch 0 is on and all others are off -> 1
            - switches 3, 7, and 14 are on -> 15

        Raises:
            OSError if there is a communication error with either of the PCA9555D
        '''
        # ignore the aux switches
        n = self.read_multi() & self.V_SWITCH_MASK

        # look from high to low for a switch that is on
        for i in reversed(range(self.NUM_V_SWITCHES)):
            if ((n >> i) & 1) == 1:
                return i + 1

        # if we get here all the switches are off
        return 0

    def get_aux_switch_1(self) -> int:
        '''
        `get_aux_switch_1()` is the state of aux switch 1, which is the 30th
        switch. Returns either 0 or 1.

        Raises:
            OSError if there is a communication error with either of the PCA9555D
        '''
        return (self.read_multi() >> 30) & 1

    def get_aux_switch_2(self) -> int:
        '''
        `get_aux_switch_2()` is the state of aux switch 2, which is the 31st
        switch. Returns either 0 or 1.

        Raises:
            OSError if there is a communication error with either of the PCA9555D
        '''
        return (self.read_multi() >> 31) & 1


def do_demo():
    '''
    Do a demo to show that we can read the switches.

    The switches are read and displayed as a 32 bit binary number.
    '''
    I2C_CHANNEL = 1
    bus = smbus.SMBus(I2C_CHANNEL)

    # change these addresses to suit your physical board setup
    # note that valid address are in the range [0x20, 0x27]
    PCA9555D_0_ADDR = 0x20
    PCA9555D_1_ADDR = 0x21

    ui_switches = UI_Switches(bus, PCA9555D_0_ADDR, PCA9555D_1_ADDR)

    while True:
        val_ui32 = ui_switches.read_multi()

        print(f"{val_ui32:32_b}")
        print(ui_switches.get_shock_level())
        time.sleep(.5)


if __name__ == "__main__":
    do_demo()
