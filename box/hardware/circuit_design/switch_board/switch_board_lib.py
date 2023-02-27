#!/usr/bin/env python

'''
Prereqs:
- this is intended to be installed on a Raspberry Pi

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
from typing import Callable
import gpiozero
import time
import smbus
from enum import Enum


class UI_Switches:
    '''
    User Interface Switches.

    32 switches are read with PCA9555D GPIO expander chips on the I2C bus.

    30 of the switches are the voltage-intensity switches which set the (spoofed)
    voltage shock level, from 15 to 450 volts.

    The extra two switches are "auxilliary" switches which can be used for other
    purposes, such as the "MAIN POWER" toggle switch on the front panel.

    Requires:
      - Shared use of I2C bus, with four addresses in the range [0x20, 0x27].
      - A GPIO pin to use as the interrupt pin, which goes LOW whenever any of the
        32 switches change state, and goes high again after an I2C reading occurs.

    Note:
      It is possible for the interrupt line to become stuck down if the switches
      have lots of mechanical chatter. A manual read will clear the interrupt
      and un-stick the line.
    '''
    NUM_SWITCHES = 32  # total number of switches
    NUM_V_SWITCHES = 30  # just the voltage switches minus the two aux switches
    V_SWITCH_MASK = 0x3FFF_FFFF  # binary mask to extract just the voltage switches

    class Row(Enum):
        '''
        The physical switches are DPDT Center Off. The UP and MIDDLE positions are
        latching, and the DOWN position is momentary.
        '''
        BOTTOM = 0
        TOP = 1

    class SwitchPos(Enum):
        '''
        The switches can either be UP, in the MIDDLE, or DOWN, as seen by a user looking
        at the front panel.
        '''
        UP = 0
        MIDDLE = 1
        DOWN = 2

    class AuxSwitch(Enum):
        '''
        There are four aux switches that can be used on the second daisy-chained
        switch board.
        '''
        ONE = 0
        TWO = 1
        THREE = 2
        FOUR = 3

    class StatusCode(Enum):
        '''
        Enumerated status for identifying I2C errors.
        '''
        OK = 0
        I2C_ERROR = 1

    def __init__(
        self,
        bus: smbus.SMBus,
        addr_0_15_top: int,
        addr_16_31_top: int,
        addr_0_15_btm: int,
        addr_16_31_btm: int,
        interrupt_pin: int,
        callback: Callable = (lambda: None)
    ) -> None:
        '''
        Initialize the UI Switches with the given I2C bus object and addresses
        of the PCA9555D I2C chips.

        Args:
            bus            : the I2C device to use
            addr_0_15_top  : the I2C address of PCA9555D[0]
            addr_16_31_top : the I2C address of PCA9555D[1]
            addr_0_15_btm  : the I2C address of PCA9555D[2]
            addr_16_31_btm : the I2C address of PCA9555D[3]
            interrupt_pin  : the pin number of the interrupt pin
            callback       : the callback function to run when the interrupt pin fires

        Note:
            All I2C addresses for the PCA9555D chips must be in the range [0x20, 0x27], this
            is set with solder jumpers on the physical PCBs.
        '''
        self._bus = bus

        # since the switches have built in pullups, we short them to ground to engage a switch
        self.ACTIVE_LEVEL = 0

        self.STATUS = self.StatusCode.OK

        self._top_row_addrs = [addr_0_15_top, addr_16_31_top]
        self._btm_row_addrs = [addr_0_15_btm, addr_16_31_btm]

        self._interrupt_pin = gpiozero.Button(interrupt_pin)

        self._callback = callback

        self._addrs_with_errors = set()

        self._cached_top_row = 0
        self._cached_btm_row = 0

        self._change_occured = False

        # each time the interrupt pin activates call the function to read all of the switches
        self._interrupt_pin.when_pressed = self.poll

        # manually trigger the poll function to cache initial switch readings
        self.poll()

    def poll(self) -> None:
        '''
        `poll()` reads all of the switches and caches their values as 32 bit 
        numbers, this included the voltage switches and also the two aux switches.

        After the switches are read the callback function is executed.

        This function is intended to be called automatically when the interrupt pin
        fires, but it can also be manually triggered.
        '''
        try:
            self._change_occured = True

            self._cached_top_row = self._read_row(self.Row.TOP)
            self._cached_btm_row = self._read_row(self.Row.BOTTOM)

            self.STATUS = self.StatusCode.OK

            self._callback()
        except Exception:
            self.STATUS = self.StatusCode.I2C_ERROR

    def _read_bank(self, addr: int) -> int:
        '''
        `_read_bank(addr)` the switches in a single PCA9555D bank at I2c address
        `addr` as one 16 bit word.

        Args:
            `addr`: the address of the chip to read.

        Raises:
            OSError if there is a problem reading the I2C bank.
        '''
        try:
            INPUT_PORT_0 = 0

            bits_0_to_7 = self._bus.read_byte_data(
                addr,
                INPUT_PORT_0
            )
            bits_8_to_15 = self._bus.read_byte(addr)

            self._addrs_with_errors.discard(addr)

            return bits_8_to_15 << 8 | bits_0_to_7
        except Exception:
            self._addrs_with_errors.add(addr)
            raise OSError

    def _read_row(self, row: Row) -> int:
        '''
        `_read_row(row)` is the value of all switches on the given row, read at once as
        a 32 bit word where switch 0 is the LSB and switch 31 is the MSB. This includes
        the voltage switches as well as the two aux switches.

        Args:
            `row`: the enumerated row to read

        Examples:
            - no switches are on -> 0x0000_0000
            - switch 0 is on -> 0x0000_0001
            - switches 2, 5, 19, and 30 are on -> 0x4008_0024

        Raises:
            OSError if there is a problem reading the I2C bank.
        '''
        addrs = self._btm_row_addrs if row == self.Row.BOTTOM else self._top_row_addrs

        bits_0_15 = self._read_bank(addrs[0])
        bits_16_31 = self._read_bank(addrs[1])

        return bits_16_31 << 16 | bits_0_15

    def change_occured(self):
        '''
        `change_occured()` is true if a change to any of the switch states has
        occured since the last time this function was called, and false otherwise.
        '''
        if self._change_occured:
            self._change_occured = False
            return True
        return False

    def v_switch_position_at(self, i: int) -> SwitchPos:
        '''
        `v_switch_position_at(i)` is the enumerated switch position of switch number `i`.
        '''
        def bit_at(num: int, pos: int) -> int:
            return (num >> pos) & 1

        nc_row = self._cached_top_row
        no_row = self._cached_btm_row

        if bit_at(nc_row, i) == self.ACTIVE_LEVEL and bit_at(no_row, i) != self.ACTIVE_LEVEL:
            return self.SwitchPos.UP
        elif bit_at(nc_row, i) != self.ACTIVE_LEVEL and bit_at(no_row, i) != self.ACTIVE_LEVEL:
            return self.SwitchPos.MIDDLE
        else:
            return self.SwitchPos.DOWN

    def list_of_v_switch_positions(self) -> list[SwitchPos]:
        '''
        `list_of_v_switch_positions()` is all 30 voltage switches represented
        as a list of enumerated switch positions. Voltage switch 0 is at
        index zero, and voltage switch 29 is at index 29.
        '''
        return [self.v_switch_position_at(i) for i in range(self.NUM_V_SWITCHES)]

    def get_voltage_switch_row(self, row: Row) -> int:
        '''
        `get_voltage_switch_row(row)` is the given enumerated row of switches represented
        as an integer where switch 0 is the LSB and switch 29 is the MSB.

        The returned value only contains the 30 voltage switches, not the two aux
        switches.
        '''
        row_as_ui32 = self._cached_btm_row if row == self.Row.BOTTOM else self._cached_top_row

        # ignore the two aux switches
        return row_as_ui32 & self.V_SWITCH_MASK

    def get_shock_level(self) -> int:
        '''
        `get_shock_level()` is the position of the highest DOWN voltage switch.
        A result of 0 means that none of the switches are DOWN. A result of an
        integer `n` in the range [1..30] means that `n` is the highest of
        the switches that are currently in the DOWN position. The returned value
        is one-higher than the bit position of the highest switch, to account
        for the zero setting where no switches are DOWN.

        Examples:
            - no switches are DOWN -> 0
            - switch 0 is DOWN and all others are with UP or in the MIDDLE -> 1
            - switches 3, 7, and 14 are DOWN -> 15
        '''
        n = self.get_voltage_switch_row(self.Row.BOTTOM)

        # look from high to low for a switch that is engaged
        for i in reversed(range(self.NUM_V_SWITCHES)):
            if ((n >> i) & 1) == self.ACTIVE_LEVEL:
                return i + 1

        # if we get here none of the switches are DOWN
        return 0

    def get_aux_switch(self, switch: AuxSwitch) -> bool:
        '''
        `get_aux_switch(sw)` is true iff the enumerated aux switch `sw` is
        physically closed.
        '''
        if switch == self.AuxSwitch.ONE:
            return ((self._cached_top_row >> 30) & 1) == self.ACTIVE_LEVEL
        elif switch == self.AuxSwitch.TWO:
            return ((self._cached_btm_row >> 30) & 1) == self.ACTIVE_LEVEL
        elif switch == self.AuxSwitch.THREE:
            return ((self._cached_top_row >> 31) & 1) == self.ACTIVE_LEVEL
        elif switch == self.AuxSwitch.FOUR:
            return ((self._cached_btm_row >> 31) & 1) == self.ACTIVE_LEVEL
        else:
            return False

    def get_status(self) -> StatusCode:
        '''
        `get_status()` is the current value of the enumerated status code.
        '''
        return self.STATUS


def do_demo():
    '''
    Do a demo to show that we can read the switches.
    '''
    I2C_CHANNEL = 1
    bus = smbus.SMBus(I2C_CHANNEL)

    # change these addresses to suit your physical board setup
    # note that valid address are in the range [0x20, 0x27]
    # the three LSBs of the address are set by solder jumpers on the boards
    ADDR_0_15_TOP = 0x20
    ADDR_0_15_BTM = 0x21
    ADDR_16_31_TOP = 0x22
    ADDR_16_31_BTM = 0x23

    INTERRUPT_PIN = 19

    class Demo_Callback(object):
        '''
        Simple callable object to demonstrate a callback
        '''

        def __init__(self):
            self.num_times_called = 0

        def __call__(self):
            print(
                f"\nI'm the interrupt callback, the switches have been read {self.num_times_called} times\n")
            self.num_times_called += 1

    ui_switches = UI_Switches(
        bus,
        ADDR_0_15_TOP,
        ADDR_16_31_TOP, ADDR_0_15_BTM,
        ADDR_16_31_BTM,
        INTERRUPT_PIN,
        Demo_Callback()
    )

    def print_switch_summary():
        print('\n' + '*'*100 + '\n')

        # you can read a whole row as an integer like this
        val_ui30_closed = ui_switches.get_voltage_switch_row(
            UI_Switches.Row.TOP)
        print(f"Top row:    {val_ui30_closed:32_b}")

        val_ui30_open = ui_switches.get_voltage_switch_row(
            UI_Switches.Row.BOTTOM)
        print(f"Bottom row: {val_ui30_open:32_b}\n")

        # get the voltage switches as a list of [UP, MIDDLE, DOWN] positions like this
        pos_list = ui_switches.list_of_v_switch_positions()
        print(f"Switch positions:\n{pos_list}\n")

        # get the position of a single switch like this
        switch_to_check = 17
        pos_at_idx = ui_switches.v_switch_position_at(switch_to_check)
        print(f"Switch at index {switch_to_check} is: {pos_at_idx}\n")

        # you can ask for the shock level like this (the highest switch that is currently held down)
        shock_level = ui_switches.get_shock_level()
        print(f"Shock level is: {shock_level}\n")

        # you can read the aux switches like this
        for sw in UI_Switches.AuxSwitch:
            if ui_switches.get_aux_switch(sw):
                print(f"{sw} engaged\n")

        # check the I2C health like this
        print(f"I2C communication status: {ui_switches.get_status()}")

        if len(ui_switches._addrs_with_errors) != 0:
            print(
                f"Error at address(es): {[hex(x) for x in ui_switches._addrs_with_errors] }")

    # heartbeat to un-stick potential stuck interrupt line
    heartbeat_t = time.time()
    heartbeat_period = 5

    while True:

        if ui_switches.change_occured():
            print_switch_summary()

        # brief sleep so that the terminal doesn't get bogged down on switch chattering
        time.sleep(.25)

        if (heartbeat_t + heartbeat_period) < time.time():
            print("\nheart beat")
            heartbeat_t += heartbeat_period

            # Because of the way the PCA9555 works, it is possible for it to get stuck with an un-cleared interrupt.
            # Interrupts are cleared when the pin state changes OR a read is performed. If the switches do a lot of
            # mechanical chattering it can miss a pin state change and get stuck low, which will stop the system from
            # working.
            # Manually reading the switches un-sticks any frozen interrupts if it is a problem. Maybe it makes sense to
            # just periodically poll the switches instead or relying on the interrrupt line, I'm not decided yet.
            ui_switches.poll()


if __name__ == "__main__":
    do_demo()
