# mlx90632-driver

## Validation

| Interface      | Win PC   | Linux PC      | Raspberry Pi (linux) | Nvidia Jetson Nano (linux) |
| -------------- | -------- | ------------- | -------------------- | -------------------------- |
| EVB90632(usb)  | 1.1.0    | 1.1.0         | 1.1.0                | 1.1.0                      |
| FTDI(FT2232H)  | 1.1.0    | 1.1.0         | 1.1.0                | 1.1.0                      |
| I2C-bus(40pin) | N/A      | N/A           | 1.1.0                | 1.1.0                      |


# mlx90632-driver 

## Intro

This python driver for MLX90632 aims to facilitate the interfacing on a PC.

Currently this driver supports 3 type of interfaces:
- [Ready] EVB90632 on WinPC, LinuxPC, Raspberry Pi ==> https://www.melexis.com/en/product/EVB90632/EVB90632
- [Ready] Raspberry Pi on built-in hardware I2C bus ==> https://www.raspberrypi.org/.
- [Ready] FTDI FT2232H on WinPC, LinuxPC, Raspberry Pi ==> https://www.mikroe.com/click-usb-adapter.

## Getting started

See below for [installation](#installation) instructions


### Running the driver demo

* Connect the EVB to your PC.  
* Open a terminal and run following command:  


```bash
mlx90632-dump
```

This program takes 1 optional argument.

```bash
mlx90632-dump <interface> <reading_count>
```

`<interface>` can be:
- `auto` (default) search for the first port available with EVB90632 hardware as interface to MLX90632.
- `I2C-1` on raspberry pi use the I2C hardware; it requires raspi-config to enable i2c hardware.
- `mlx://evb:90632/1` use first EVB90632 on USB.
- `mlx://evb:90632/2` use second EVB90632 on USB.
- `ftdi://ftdi:2232/1` use first FT2232 port on USB.

### Usage

Below you can find an example on how to read a sample of the MLX90632 senor with I2C address 0x3A. Please look into mlx90632.py for more advanced features.

```python
from mlx90632.mlx90632 import Mlx90632

dev = Mlx90632('mlx://evb:90632/1')              # establish communication between EVB90632 and PC
dev.init()                                       # read EEPROM and pre-compute calibration parameters.
dev.wait_new_data()                              # wait until there is new data.
raw_data = dev.read_measurement_data()           # read new measurement data.
ta, to = dev.do_compensation(raw_data)           # compute the temperature.
print ("TA: {} -- TO: {} DegC".format (ta, to))  # print the results
```

## Issues and new Features

In case you have any problems with usage of the plugin, please open an issue on GitHub.  
Provide as many valid information as possible, as this will help us to resolve Issues faster.  
We would also like to hear your suggestions about new features which would help your user experience.


## Installation

https://pypi.org/project/mlx90632-driver/

```bash
pip install mlx90632-driver
```

### Windows + FTDI I2C interface

In order to use the FTDI chip, FT2232H or FT232H, an alternative driver needs to be installed.

Procedure:

1. Plug your FT232H or FT2232H into the usb port of your PC, and let windows install the default drivers.
1. download the zadig tool https://zadig.akeo.ie/.
1. download the libusb https://libusb.info/ => Downloads menu => Latest Windows Binaries.
1. run zadig tool as admin.
1. menu => options => list all devices.
1. Select Dual RS232.
1. Select with the up-down arrows `libusb0 (v1.2.6.0)`.
1. Click re-install driver button.


### Linux + EVB90632 interface

1. Install libhid library.

```bash
sudo apt update
sudo apt install libhidapi-libusb0
```
2. Add these udev-rules to the [file](udev_rules/20-melexis-evb.rules):  
`/etc/udev/rules.d/20-melexis-evb.rules`  

```txt
# EVB90632
SUBSYSTEM=="usb", ATTR{manufacturer}=="Melexis", ATTR{product}=="EVB90632", GROUP="plugdev", MODE="0666"
```
3. Now reboot to make the new udev rules active.


### Linux + FTDI I2C interface

1. Add these udev-rules to the [file](udev_rules/21-ftdi.rules):  
`/etc/udev/rules.d/21-ftdi.rules`  

```txt
# FTDI rules
ATTR{idVendor}=="0403", ATTR{idProduct}=="6010", MODE="666", GROUP="dialout"
ATTR{idVendor}=="0403", ATTR{idProduct}=="6014", MODE="666", GROUP="dialout"
```
2. Now reboot to make the new udev rules active.


### Linux + Raspberry Pi & Nvidia Jetson Nano + 40 pin HW I2C bus

Enable the I2C interface
`sudo raspi-config`

  - 'enable i2c' in interface; in case you want to connect MLX9064x on the I2C bus of RPi.
  - optional: 'enable ssh' in interface; now you can login remotely over the network.
