# PRE-RELEASE

Testing phase! Please do not yet use...

## Validation

| Interface      | Win PC   | Linux PC      | Raspberry Pi (linux) | Nvidia Jetson Nano (linux) |
| -------------- | -------- | ------------- | -------------------- | -------------------------- |
| EVB90632(usb)  | 0.1.5    | 0.1.5         | 0.1.5                | 0.1.5                      |
| FTDI(FT2232H)  | 0.1.5    | 0.1.5         | 0.1.5                | 0.1.5                      |
| I2C-bus(40pin) | N/A      | N/A           | 0.1.5                | 0.1.5                      |


# mlx90632-driver 

## Intro

This python driver for MLX90632 aims to facilitate the interfacing on a PC.

Currently this driver supports 3 type of interfaces:
- [Ready] EVB90632 on WinPC, LinuxPC, Raspberry Pi ==> https://www.melexis.com/en/product/EVB90632/EVB90632
- [Ready] Raspberry Pi on built-in hardware I2C bus ==> https://www.raspberrypi.org/.
- [Ready] FTDI FT2232H on WinPC, LinuxPC, Raspberry Pi ==> https://www.mikroe.com/click-usb-adapter.

## Getting started

### Installation

https://pypi.org/project/mlx90632-driver/

```bash
pip install mlx90632-driver
```

On any linux platform for interfacing the EVB90632 we need to install `hidapi`.

```bash
sudo apt update
sudo apt install libhidapi-libusb0
```

*****

See below for extra Raspberry pi installation instructions.  

*****


### Running the driver demo

* Connect the EVB to your PC.  
* Open a terminal and run following command:  


```bash
mlx90632-dump
```

This program takes 1 optional argument.

```bash
mlx90632-dump <communication-url>
```

`<communication-url>` can be:
- `auto` (default) search for the first port available with EVB90632 hardware as interface to MLX90632.
- `I2C-1` on raspberry pi use the I2C hardware; it requires raspi-config to enable i2c hardware.
- `mlx://evb:90632/1` use first EVB90632 on USB.
- `mlx://evb:90632/2` use second EVB90632 on USB.
- `ftdi://ftdi:2232/1` use first FT2232 port on USB.

### Usage

Below you can find an example on how to read a sample of the MLX90632 senor with I2C address 0x3A. Please look into mlx90632.py for more advanced features.

```python
import mlx.mlx90640 as mlx

dev = mlx.Mlx9064x('COM4', i2c_addr=0x33, frame_rate=8.0) # establish communication between EVB90640 and
                                                          # PC, the I2C address of the MLX90640 sensor is
                                                          # 0x33 and change the frame rate to 8Hz
dev.init()                      # read EEPROM and pre-compute calibration parameters.
frame = dev.read_frame()        # Read a frame from MLX90640
                                # In case EVB90640 hw is used, the EVB will buffer up to 4 frames, so possibly you get a cached frame.
f = dev.do_compensation(frame)  # calculates the temperatures for each pixel
```

## Issues and new Features

In case you have any problems with usage of the plugin, please open an issue on GitHub.  
Provide as many valid information as possible, as this will help us to resolve Issues faster.  
We would also like to hear your suggestions about new features which would help your Continuous Integration run better.

## Raspberry pi 3B+/4B

This driver is validated to work on a Rapberry Pi 4 configuration with raspbian buster february 2020 release.

### Installation

- `sudo raspi-config`
    - 'enable i2c' in interface; in case you want to connect MLX9064x on the I2C bus of RPi.
    - optional: 'enable ssh' in interface; now you can login remotely over the network.
- `sudo pip3 install virtualenv`
- `sudo apt update`
- `sudo apt install libhidapi-libusb0`
- `virtualenv --system-site-packages pyvenv`
- `. pyvenv/bin/activate`
- `pip install mlx90632-driver`
