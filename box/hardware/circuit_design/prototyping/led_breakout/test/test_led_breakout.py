#!/usr/bin/env python

'''
Prereqs:
- enable SPI in /boot/config.txt, uncomment dtparam=spi=on

'''
import time
import gpiozero


class UI_LEDs:
    '''
    User Interface LEDs.

    32 LEDs are driven by two MAX6969 LED driver chips, which are on the SPI bus.

    MAX6969[0] handles LEDs 0..15
    MAX6969[1] handles LEDs 16..31

    Requires:
        - Shared use of SPI bus.

        - One GPIO pin for the Chip Select line. A generic GPIO is used for chip
        select because the system will require more SPI devices than there are
        built-in chip select pins. The built-in chip select pins are not used.

        - One PWM enabled pin for the brightness control.
    '''

    # the number of LEDs
    NUM_LEDS = 32

    def __init__(
            self,
            spi: gpiozero.SPIDevice,
            cs_pin: int,
            pwm_pin: int
    ) -> None:
        '''
        Initialize the UI LEDs with the given SPI core and Chip Select
        pin number, and turn all the LEDs off.

        Args:
            spi: the SPI device to use
            cs_pin: the GPIO pin to use for Chip Select
            pwm_pin: the GPIO pin to use for the PWM brightness control

        Side effects:
            turns all the LEDs off

        Raises:
            PinInvalidPin if either the cs or pwm pins are not valid pin numbers.
        '''
        self.spi = spi
        self.chip_sel = gpiozero.DigitalOutputDevice(cs_pin, active_high=False)
        self.pwm = gpiozero.PWMOutputDevice(
            pwm_pin, active_high=False, initial_value=0.0)

        self.all_off()

    def set_brightness(self, level):
        '''
        Set the brightness for all of the LEDs.

        Args:
            level (float): the brightness level, in [0..1]

        Raises:
            OutputDeviceBadValue if the level is not in [0..1]
        '''
        self.pwm.value = level

    def write_multi(self, word_ui32: int) -> None:
        '''
        write_multi(word_ui32) writes the given 32 bit unsigned integer
        to the UI LEDs.

        Args:
            word_ui32: the unsigned 32 bit int to write, in [0x0..0xFFFFFFFF]

        Side effects:
            illuminates LEDs that correspond to a set bit in word_ui32

        Examples:
            write_multi(0x00000001) -> the 0th LED lights up
            write_multi(0x80000005) -> the 0th, 2nd, and 31st LEDs light up
        '''
        # split the ui32 into four bytes
        bytes_ = word_ui32.to_bytes(4, 'little')

        # write to the LEDs
        self.chip_sel.on()
        self.spi._spi.transfer(
            [bytes_[3], bytes_[2], bytes_[1], bytes_[0]]
        )
        self.chip_sel.off()

    def single_on(self, led_num: int) -> None:
        '''
        single_on(led_num) turns the single LED at the given position on and
        all other LEDs off.

        Args:
            led_num: the LED number to turn on, in [0..31]

        Side effects:
            illuminates the single LED at the given number and turns all other
            LEDs off

        Examples:
            single_on(0) -> the 0th LED lights up
            single_on(24) -> the 24the LED lights up
            single_on(32) -> out of range, do nothing
            single_on(-1) -> out of range, do nothing
        '''
        if not 0 <= led_num < self.NUM_LEDS:
            return  # invalid LED, should some other error handling happen here?

        self.write_multi(1 << led_num)

    def all_off(self) -> None:
        '''
        all_off() turns all the LEDs off

        Side effects:
            turns all the LEDs off
        '''
        self.write_multi(0x00000000)


def do_demo(num_secs, delay_secs):
    '''
    Do a demo to show that the LEDs work. Lights up LEDs in sequence.
    '''

    DEMO_CHIP_SELECT_PIN = 17
    DEMO_PWM_PIN = 12

    ui_leds = UI_LEDs(gpiozero.SPIDevice(), DEMO_CHIP_SELECT_PIN, DEMO_PWM_PIN)

    ui_leds.set_brightness(0.8)

    counter = 0

    DEMO_LENGTH_SEC = num_secs
    STOP_TIME = time.monotonic() + DEMO_LENGTH_SEC

    while time.monotonic() < STOP_TIME:
        ui_leds.single_on(counter)
        counter += 1
        counter &= UI_LEDs.NUM_LEDS - 1
        time.sleep(delay_secs)


if __name__ == "__main__":
    do_demo(5, 0.1)
