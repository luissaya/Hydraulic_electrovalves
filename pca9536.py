import math
import time
from enum import IntEnum

import smbus


class Pin(IntEnum):
    P0 = 1 << 0  # CON1
    P1 = 1 << 1  # CON2
    P2 = 1 << 2  # ND
    P3 = 1 << 3  # ND


class Mode(IntEnum):
    OUTPUT = 0
    INPUT = 1


class Value(IntEnum):
    HIGH = 1
    LOW = 0


class PCA9536:
    def __init__(self, bus, address=0x41, debug=False):
        # self.bus = smbus.SMBus(1)
        self.bus = bus
        self.address = address
        self.debug = debug
        if self.debug:
            print("Reseting PCA9536")
        # Registers Address
        self.__INPUT_PORT_ADDR = 0x00
        self.__OUTPUT_PORT_ADDR = 0x01
        self.__POLARITY_INV_ADDR = 0x02
        self.__CONF_PORT_ADDR = 0x03
        # Registers Values
        self.__INPUT_PORT_VAL = 0xF0
        self.__OUTPUT_PORT_VAL = 0xFF
        self.__POLARITY_INV_VAL = 0x00
        self.__CONF_PORT_VAL = 0xFF

    def pin_mode(self, pin, mode):
        if self.debug:
            print("--- Pin Mode ---")
        p = int(pin)
        m = int(mode)
        if m:
            # input mode
            self.__CONF_PORT_VAL = self.__CONF_PORT_VAL | p
            if self.debug:
                print(">>Pin:{}  Mode:{}".format(int(math.log2(p)), m))
                print(">>>CONF_PORT_1: 0b{:08b}".format(self.__CONF_PORT_VAL))
        else:
            # output mode
            self.__CONF_PORT_VAL = self.__CONF_PORT_VAL & ~p
            if self.debug:
                print(">>Pin:{}  Mode:{}".format(int(math.log2(p)), m))
                print(">>>CONF_PORT_1: 0b{:08b}".format(self.__CONF_PORT_VAL))

        self.bus.write_byte_data(
            self.address, self.__CONF_PORT_ADDR, self.__CONF_PORT_VAL
        )
        time.sleep(0.005)

    def digital_write(self, pin, value):
        if self.debug:
            print("digital_write")
        p = int(pin)
        v = int(value)
        if v:
            # high value
            self.__OUTPUT_PORT_VAL = self.__OUTPUT_PORT_VAL | p
            if self.debug:
                print(">>Pin:{}  Value:{}".format(int(math.log2(p)), v))
                print(">>>OUTPUT_PORT_1:{0:b}".format(self.__OUTPUT_PORT_VAL))
        else:
            # low value
            self.__OUTPUT_PORT_VAL = self.__OUTPUT_PORT_VAL & ~p
            if self.debug:
                print(">>Pin:{}  Value:{}".format(int(math.log2(p)), v))
                print(">>>OUTPUT_PORT_1:{0:b}".format(self.__OUTPUT_PORT_VAL))
        self.bus.write_byte_data(
            self.address, self.__OUTPUT_PORT_ADDR, self.__OUTPUT_PORT_VAL
        )
        time.sleep(0.005)

    def digital_read(self, pin):
        if self.debug:
            print("digital_read")
        p = int(pin)
        data = self.bus.read_byte_data(self.address, self.__INPUT_PORT_ADDR)
        self.__INPUT_PORT_VAL = data & 0x0F
        r = (self.__INPUT_PORT_VAL & p) >> int(math.log2(p))
        if r:
            return Value.HIGH
        else:
            return Value.LOW


if __name__ == "__main__":
    # get I2C bus
    bus = smbus.SMBus(1)
    relays = PCA9536(bus, 0x41, True)
    relays.pin_mode(Pin.P0, Mode.OUTPUT)
    relays.pin_mode(Pin.P1, Mode.OUTPUT)
    while 1:
        relays.digital_write(Pin.P0, Value.HIGH)
        relays.digital_write(Pin.P1, Value.HIGH)
        time.sleep(2)
        relays.digital_write(Pin.P0, Value.LOW)
        relays.digital_write(Pin.P1, Value.LOW)
        time.sleep(2)
