from ds18b20.device import *

device = Device()

# values from calibration
ref_low = 0.01
ref_high = 98.7

# set calibration
device.set_calibration('28-03219779d339', -0.781, 97.1663333, ref_low, ref_high)
device.set_calibration('28-032197791b3c', -1.5583125, 96.4163333, ref_low, ref_high)

# get current temperature from all available devices
temps = device.get_temps()

# print device serial number, date and time, and the temperature in C
for dp in temps:
    print(dp.get_device_sn(), dp.get_date_time(), format(dp.get_temp_raw() / 1000.00, '.3f'), format(dp.get_temp_C(), '.3f'))
