# TEST HIDRAULIC ELECTROVALVES
I2C addresses in use 
|        Device     | Address |
|-------------------|---------|
|      PCA9685      |   0x40  |
|      PCA9536      |   0x41  |
| ADS7828 + ACS7112 |   0x48  |
|     PCA9685       |   0x70  |

smbus library: https://github.com/adafruit/Adafruit_Python_PureIO/blob/main/Adafruit_PureIO/smbus.py

## PCA9685 
    PCA9685 8-Channel 8W 12V FET Driver Proportional Valve Controller with IoT Interface
    Datasheet: https://cdn-shop.adafruit.com/datasheets/PCA9685.pdf

## PCA9536
    2-Channel Signal Relay 1A SPDT I2C Mini Module
    Datasheet: https://www.ti.com/lit/ds/scps125h/scps125h.pdf?ts=1675463898501&ref_url=https%253A%252F%252Fwww.google.com%252F

## ADS7828 + ACS7112
    8-Channel DC Current Monitor with I2C Interface
    Datasheets:
    + ADS7828: https://media.ncd.io/sites/2/20170721134916/ADS7828-2.pdf?_ga=2.226438362.1942944568.1675366777-1088693194.1675366777
    + ACS712: https://www.sparkfun.com/datasheets/BreakoutBoards/0712.pdf

