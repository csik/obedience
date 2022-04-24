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
    INPUT_PORT_0 = 0
    INPUT_PORT_1 = 1

    def __init__(self, bus, addr_0_15, addr_16_31) -> None:
        '''
        Initialize the UI Switches with the given I2C bus object.

        Args:
            bus: the I2C device to use
            addr_0_15  (int): the I2C address of PCA9555D[0]
            addr_16_31 (int): the I2C address of PCA9555D[1]
        '''
        self.bus = bus
        self.addr_0_15 = addr_0_15
        self.addr_16_31 = addr_16_31

    def _read_bank(self, addr: int) -> int:
        '''
        Read the switches in a single PCA9555D bank as one 16 bit word.

        Args:
            bank: the chip to use, either 0 or 1.

        Raises:
            IndexError if bank is not in [0, 1]
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
        Read the value of all switches at once as a 32 bit word where switch 0
        is the LSB and switch 31 is the MSB.

        Raises:
            OSError if there is a communication error with either of the PCA9555D
        '''
        bits_0_15 = self._read_bank(self.addr_0_15)
        bits_16_31 = self._read_bank(self.addr_16_31)

        return bits_16_31 << 16 | bits_0_15

    def read_single(self, switch_num: int) -> int:
        '''
        Read a single switch as the integer value 0 or 1.

        Args:
            switch_num (int): the switch number to read, in [0..31]

        Raises:
            OSError if there is a communication error with either of the PCA9555D

        '''
        if not 0 <= switch_num <= 31:
            return 0
        return (self.read_multi() >> switch_num) & 1


def do_demo():
    '''
    Do a demo to show that we can read the switches.

    The switches are read and displayed as a 32 bit binary number.
    '''
    I2C_CHANNEL = 1
    bus = smbus.SMBus(I2C_CHANNEL)

    # change these addresses to suit your physical board setup
    PCA9555D_0_ADDR = 0x20
    PCA9555D_1_ADDR = 0x21

    ui_switches = UI_Switches(bus, PCA9555D_0_ADDR, PCA9555D_1_ADDR)

    while True:
        val_ui32 = ui_switches.read_multi()

        print(f"{val_ui32:32_b}")
        time.sleep(.5)


if __name__ == "__main__":
    do_demo()
