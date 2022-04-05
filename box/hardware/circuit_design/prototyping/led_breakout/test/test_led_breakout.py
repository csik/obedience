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
        select because the system may require more SPI devices than there are
        built in chip select pins. The built-in chip select pins are not used.
        If the final system uses 2 or fewer total SPI devices then the built in
        CS pins could be used.

        - One PWM enabled pin for the brightness control.
    '''

    # the number of LEDs
    NUM_LEDS = 32

    def __init__(self, spi, cs_pin, pwm_pin) -> None:
        '''
        `UI_LEDs(spi, cs, pwm)` initializes the UI LEDs with the given SPI core
        `spi`, Chip Select pin number `cs`, and PWM pin number `pwm`, and finally
        turns all the LEDs off.

        Args:
            `spi` (gpiozero.SPIDevice): the SPI device to use
            `cs_pin` (int): the GPIO pin number to use for Chip Select
            `pwm_pin`(int): the GPIO pin number to use for the PWM brightness control

        Note:
            prefer pins 12, 13, 18, or 19 for the PWM pin, these are hardware
            PWM pins, other pins will use software PWM.

        Side effects:
            turns all the LEDs off

        Raises:
            PinInvalidPin if either the `cs` or `pwm` pins are not valid pin numbers.
        '''
        self.spi = spi
        self.chip_sel = gpiozero.DigitalOutputDevice(cs_pin, active_high=False)
        self.pwm = gpiozero.PWMOutputDevice(
            pwm_pin, active_high=False, initial_value=0.0)

        self.all_off()
        self._cached_write = 0

    def set_brightness(self, level) -> None:
        '''
        `set_brightness(b)` sets the brightness for all of the LEDs to the 
        brightness level `b`.

        Args:
            `level` (float): the brightness level

        Requires:
            `level` is in [0.0, 1.0], the value will be clamped if it falls
            outside of this range

        '''
        if level < 0.0:
            level = 0.0
        if 1.0 < level:
            level = 1.0

        self.pwm.value = level

    def write_multi(self, word_ui32) -> None:
        '''
        `write_multi(w)` sets the UI LEDs to the pattern described by the bits
        in the 32 bit word `w`.

        Args:
            `word_ui32` (int): the unsigned 32 bit int to write

        Requires:
            `word_ui32` is in [0x0..0xFFFFFFFF]

        Side effects:
            illuminates LEDs that correspond to the set bits in `word_ui32`. The
            LSB corresponds to LED 0 and the MSB corresponds to LED 31.

        Examples:
            `write_multi(0x00000001)` -> the 0th LED lights up
            `write_multi(0x80000005)` -> the 0th, 2nd, and 31st LEDs light up
        '''
        self.chip_sel.on()
        self.spi._spi.transfer(
            word_ui32.to_bytes(4, 'big')
        )
        self.chip_sel.off()
        self._cached_write = word_ui32

    def write_single(self, led_num, state) -> None:
        '''
        `write_single(n, s)` sets the single LED at the given position `n` to 
        the given state `s`. The state of all other LEDs is left alone.

        Args:
            `led_num` (int): the LED number to turn on, in [0..31]
            `state` (int): the state to write, in [0..1]

        Requires:
            `led_num` is an integer in [0..31]
            `state` is an integer in [0, 1]

        Examples:
            `write_single(13, 1)` -> the 13th LED turns on if it was previously 
            off, or stays on if it was already on

            `write_single(3, 0)` -> the 3rd LED turns off if it was previously 
            on, or stays off if it was already off
        '''
        val_to_write = self._cached_write & ~(1 << led_num)
        val_to_write = val_to_write | (state << led_num)
        self.write_multi(val_to_write)

    def single_on(self, led_num) -> None:
        '''
        `single_on(n)` turns the single LED at position `n` on and turns
        all other LEDs off.

        Args:
            `led_num` (int): the LED number to turn on

        Requires:
            `led_num` is an integer in [0..31]

        Side effects:
            a single LED is left illuminated

        Examples:
            `single_on(0)` -> the 0th LED lights up, all other LEDs off
            `single_on(24)` -> the 24th LED lights up, all other LEDs off
        '''
        self.write_multi(1 << led_num)

    def all_off(self) -> None:
        '''
        `all_off()` turns all the LEDs off

        Side effects:
            turns all the LEDs off
        '''
        self.write_multi(0x00000000)


def do_demo(duration_secs, delay_secs):
    '''
    Do a demo to show that the LEDs work. Lights up LEDs in sequence.
    '''

    DEMO_CHIP_SELECT_PIN = 17
    DEMO_PWM_PIN = 12

    ui_leds = UI_LEDs(gpiozero.SPIDevice(), DEMO_CHIP_SELECT_PIN, DEMO_PWM_PIN)

    ui_leds.set_brightness(0.8)

    counter = 0

    DEMO_LENGTH_SEC = duration_secs
    STOP_TIME = time.monotonic() + DEMO_LENGTH_SEC

    while time.monotonic() < STOP_TIME:
        ui_leds.single_on(counter)
        counter += 1
        counter &= UI_LEDs.NUM_LEDS - 1
        time.sleep(delay_secs)


if __name__ == "__main__":
    do_demo(5, 0.1)
