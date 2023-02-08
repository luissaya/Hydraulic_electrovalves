import time
import smbus

DEVICE_ADDRESS = 0x48
I2C_CHANNEL = 1

PULL_UP_RESIST = 41.2
PULL_DOWN_RESIST = 10.0
ADC_REF_VOLT = 5.0
DEFAULT_RATIO = 1.0
ADC_RESOLUTION = 4095.0

# ADC7828 CONTROL REGISTER
ADS7828_CONFIG_SD_DIFFERENTIAL = 0x00
ADS7828_CONFIG_SD_SINGLE = 0x80
ADS7828_CONFIG_CS_CH0 = 0x00
ADS7828_CONFIG_CS_CH1 = 0x40
ADS7828_CONFIG_CS_CH2 = 0x10
ADS7828_CONFIG_CS_CH3 = 0x50
ADS7828_CONFIG_CS_CH4 = 0x20
ADS7828_CONFIG_CS_CH5 = 0x60
ADS7828_CONFIG_CS_CH6 = 0x30
ADS7828_CONFIG_CS_CH7 = 0x70
ADS7828_CONFIG_PD_OFF = 0x00
ADS7828_CONFIG_PD_REFOFF_ADON = 0x04
ADS7828_CONFIG_PD_REFON_ADOFF = 0x08
ADS7828_CONFIG_PD_REFON_ADON = 0x0C

# ADS 7828 I2C CONTROL CLASS
class ADS7828:
    def __init__(self, bus_id=I2C_CHANNEL, address=DEVICE_ADDRESS, 
        vref=ADC_REF_VOLT, default_ratio=DEFAULT_RATIO,offset=0,
        debug=False):
        self.i2c = bus_id
        self.address = address
        self.debug = debug

        self.adc_resol = ADC_RESOLUTION
        self.vref = vref
        self.ratio = [self.adc_resol / (default_ratio * self.vref)] * 8
        self.offset = [offset] * 8
        self.adc_ratio_int()

    def adc_ratio_int(self):
        self.ratio_set(0, 0, 1)
        self.ratio_set(1, 0, 1)
        self.ratio_set(2, 0, 1)  
        self.ratio_set(3, 0, 1) 
        self.ratio_set(4, 0, 1)
        self.ratio_set(5, 0, 1)
        self.ratio_set(6, 0, 1)
        self.ratio_set(7, 0, 1)

    def ratio_set(self, ch, PULL_UP_RESIST=PULL_UP_RESIST, 
                  PULL_DOWN_RESIST=PULL_DOWN_RESIST):  
        regSum = PULL_UP_RESIST + PULL_DOWN_RESIST
        self.ratio[ch] = self.adc_resol / ((regSum / PULL_DOWN_RESIST) * self.vref)

    def read_raw_adc(self, ch):
        config = 0
        config |= ADS7828_CONFIG_SD_SINGLE
        config |= ADS7828_CONFIG_PD_REFOFF_ADON
        if ch == 0:
            config |= ADS7828_CONFIG_CS_CH0
        elif ch == 1:
            config |= ADS7828_CONFIG_CS_CH1
        elif ch == 2:
            config |= ADS7828_CONFIG_CS_CH2
        elif ch == 3:
            config |= ADS7828_CONFIG_CS_CH3
        elif ch == 4:
            config |= ADS7828_CONFIG_CS_CH4
        elif ch == 5:
            config |= ADS7828_CONFIG_CS_CH5
        elif ch == 6:
            config |= ADS7828_CONFIG_CS_CH6
        elif ch == 7:
            config |= ADS7828_CONFIG_CS_CH7

        # adc convertion time waiting
        time.sleep(0.01)  
        data = [0, 0]
        data = self.i2c.read_i2c_block_data(self.address, config, 2)
        time.sleep(0.01)
        return (data[0] << 8) + data[1]
    
    def read_voltage(self, ch):
        ch_value = self.read_raw_adc(ch) / self.ratio[ch] - self.offset[ch]
        return round(ch_value, 2)

    def all_ch_value_display(self):
        data = [0] * 8
        data[0] = self.read_temp(0)
        for i in range(1, 8):
            # an sensibility of 0.185V/A is used because the current is less than 5A
            data[i] = (self.read_voltage(i) - 2.5) / 0.185

        print(
            "ch0=%2.2fA, ch1=%2.2fA, ch2=%2.2fA, ch3=%2.2fA, ch4=%2.2fA, ch5=%2.2fA, In ch6=%2.2fA, ch7=%2.2fA"
            % (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
        )
    
    def rms_channel_0_current(self):
        c_sum = 0
        for x in range(100):
            v = self.read_voltage(0)
            c_sum += v
            # time.sleep(0.01)
        return (c_sum/100.0 - 2.5) / 0.185

    def all_ch_raw_adc_display(self):
        data = [0] * 8
        for i in range(8):
            data[i] = self.read_raw_adc(i)
        print(
            "ch0=%d, ch1=%d, ch2=%d, ch3=%d, ch4=%d, ch5=%d, ch6=%d, ch7=%d"
            % (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
        )


if __name__ == "__main__":
    bus = smbus.SMBus(1)
    adc_= ADS7828(bus,0x48)
    while True:
        print(adc_.rms_channel_0_current())