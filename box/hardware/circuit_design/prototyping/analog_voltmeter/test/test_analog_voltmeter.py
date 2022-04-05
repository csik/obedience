#!/usr/bin/env python

import time
import gpiozero


class Voltmeter:
    '''
    User interface Analog Voltmeter.

    A single analog needle voltmeter is driven by PMW.

    Requires:
      - One PWM enabled GPIO pin
    '''

    def __init__(self, pwm_pin) -> None:
        '''
        `Voltmeter(pwm)` initializes a Voltmeter object with the given PWM pin
        number `pwm`, and sets the initial voltmeter value to 0.0

        Args:
            `pwm_pin` (int): the GPIO pin number to use to control the voltmeter

        Note:
            prefer pins 12, 13, 18, or 19 for the PWM pin, these are hardware
            PWM pins, other pins will use software PWM

        Raises:
            PinInvalidPin if the `pwm` pin is not a valid pin number
        '''
        self.pwm = gpiozero.PWMOutputDevice(
            pwm_pin,
            active_high=True,
            initial_value=0.0
        )

    def set(self, val):
        '''
        `set(v)` sets the voltmeter value to the value `v`

        Args:
            `v` (float): zero is full off and 1.0 is full scale

        Requires:
            `v` is in [0.0, 1.0], the value will be clamped if it falls
            outside of this range
        '''
        if val < 0.0:
            val = 0.0
        if 1.0 < val:
            val = 1.0

        self.pwm.value = val


def do_demo(duration_secs, delay_secs):
    '''
    Do a demo to show that the voltemter works by wiggling the needle
    '''
    DEMO_PWM_PIN = 12

    value = 0.0
    max_val = 1.0
    increment = 0.01

    meter = Voltmeter(DEMO_PWM_PIN)

    stop_time = time.monotonic() + duration_secs

    while time.monotonic() < stop_time:
        meter.set(value)
        value += increment

        if (max_val < value):
            value = 0.0

        time.sleep(delay_secs)


if __name__ == '__main__':
    do_demo(10, 0.1)
