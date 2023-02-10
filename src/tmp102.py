import smbus

from tools import logs
from tools.config import Tmp102


def twos_comp(val, bits):
    """Calculate the 2's complement of a given number."""
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val


def main():

    # Initialize logging
    log = logs.create_log("DEBUG")

    # Initialize I2C (SMBus)
    bus = smbus.SMBus(Tmp102.channel)

    # Read the CONFIG register (2 bytes)
    val = bus.read_i2c_block_data(Tmp102.address, Tmp102.reg_config, 2)
    # print("Old CONFIG:", val)

    # Set to 4 Hz sampling (CR1, CR0 = 0b10)
    val[1] = val[1] & 0b00111111
    val[1] = val[1] | (0b10 << 6)

    # Write 4 Hz sampling back to CONFIG
    bus.write_i2c_block_data(Tmp102.address, Tmp102.reg_config, val)

    # Read CONFIG to verify that we changed it
    val = bus.read_i2c_block_data(Tmp102.address, Tmp102.reg_config, 2)

    # Read temperature registers
    val = bus.read_i2c_block_data(Tmp102.address, Tmp102.reg_tmp, 2)
    temp_c = (val[0] << 4) | (val[1] >> 5)

    # Convert to 2s complement (temperatures can be negative)
    temp_c = twos_comp(temp_c, 12)

    # Convert registers value to temperature (C)
    temp_c = temp_c * 0.0625

    log.info(f"Temperature: {round(temp_c, 2)} C")


if __name__ == "__main__":
    main()
