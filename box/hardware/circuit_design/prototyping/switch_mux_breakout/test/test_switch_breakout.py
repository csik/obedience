#!/usr/bin/env python

'''
Prereqs:
- enable SPI in /boot/config.txt, uncomment dtparam=spi=on

'''
import time
import gpiozero


class UI_Switches:
    '''
    User Interface Switches.

    32 switches are read with two MCP23S18 GPIO expander chips, on the SPI bus.

    MCP23S18[0] handles switches 0..15
    MCP23S18[1] handles switches 16..31

    Requires:
      - Shared use of SPI bus.

      - Two GPIO pins for the Chip Select lines. A generic GPIO is used for chip
      select because the system will require more SPI devices than there are
      built-in chip select pins. The built-in chip select pins are not used.
    '''

    NUM_SWITCHES = 32

    # register addresses
    GPIOA = 0x12

    # bit 0 on indicates a "read" operation, bits 1..7 are the fixed address
    CONTROL_BYTE_READ = 0x41

    def __init__(
        self,
        spi: gpiozero.SPIDevice,
        cs_0_pin: int,
        cs_1_pin: int
    ) -> None:
        '''
        Initialize the UI Switches with the given SPI core and Chip Select pin.

        Args:
            spi: the SPI device to use
            cs_[n]_pin: the two GPIO pins to use for Chip Select, cs0 is for
            switches 0..15, and cs1 is for switches 16..31

        The default MCP23S18 settings are perfect for what we want to do, so 
        very little register manipulation is needed.

        Raises:
            PinInvalidPin if either cs pin is not a valid GPIO pin number. 
        '''
        self.spi = spi
        self.chip_sel_0 = gpiozero.DigitalOutputDevice(
            cs_0_pin, active_high=False
        )
        self.chip_sel_1 = gpiozero.DigitalOutputDevice(
            cs_1_pin, active_high=False
        )

    def _read_bank(self, chip_sel: gpiozero.DigitalOutputDevice) -> int:
        '''
        Read the switches in a single MCP23S18 bank as one 16 bit word.

        Args:
            chip_sel: the chip select pin to use.
        '''
        chip_sel.on()
        self.spi._spi.write(
            # the MCP23S18 defaults to sequential mode, so we can just send the
            # address of port A, and if we do two reads it will automatically
            # increment the address into port B for the second read operation
            [self.CONTROL_BYTE_READ, self.GPIOA]
        )
        val = self.spi._spi.read(2)
        chip_sel.off()

        return val[0] << 8 | val[1]

    def read_multi(self) -> int:
        '''
        Read the value of all switched at once as a 32 bit word where switch 0
        is the LSB and switch 31 is the MSB.
        '''
        val_0_15 = self._read_bank(self.chip_sel_0)
        val_16_31 = self._read_bank(self.chip_sel_1)

        return val_16_31 << 16 | val_0_15

    def read_single(self, switch_num: int) -> int:
        '''
        Read a single switch as the integer value 0 or 1.

        Args:
            switch_num (int): the switch number to read, in [0..31]

        '''
        if not 0 <= switch_num <= 31:
            return 0
        return (self.read_multi() >> switch_num) & 1


def do_demo():
    '''
    Do a demo to show that we can read the switches.

    The switches are read and displayed as a 32 bit binary number.
    '''
    SPI = gpiozero.SPIDevice()

    SWICH_CS_0_PIN = 16
    SWICH_CS_1_PIN = 20
    ui_switches = UI_Switches(SPI, SWICH_CS_0_PIN, SWICH_CS_1_PIN)

    while True:
        val_ui32 = ui_switches.read_multi()

        print(f"{val_ui32:32_b}")
        time.sleep(.5)


if __name__ == "__main__":
    do_demo()
