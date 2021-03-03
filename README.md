# DS18B20 Temperature Sensors
> Classes and methods to handle DS18B20 temperature sensors arrached to a raspberry pi.


This file will become your README and also the index of your documentation.

## Install

`pip install ds18b20`

## How to use

Fill me in please! Don't forget code examples:

```python
device = Device(base_dir='resources/')

# values from calibration
raw_low = -1.563
raw_high = 97.75
ref_low = 0.01
ref_high = 98.7

# set calibration
device.set_calibration('28-03219779d857', raw_low, raw_high, ref_low, ref_high)

temps = device.get_temps()


for dp in temps:
    print(dp.get_device_sn(), dp.get_date_time(), format(dp.get_temp_C(), '.3f'))


```

    28-03219779d857 2021-03-03 22:29:15.202070 21.959
    28-03219779d339 2021-03-03 22:29:15.202197 20.750

