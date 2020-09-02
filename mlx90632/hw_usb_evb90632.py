import time
import struct
import os
import sys
from mlx90632.hw_i2c_hal import HwI2cHalMlx90632
import platform

import mlx90632.pympt


DEFAULT_I2C_TCLOCK    =    10.0
DEFAULT_I2C_TSTART    =    10.0
DEFAULT_I2C_TSTOP     =    10.0
DEFAULT_I2C_TWRDELAY  =    10.0
DEFAULT_I2C_THOLDDATA =     0.05


class Evb90632Commands:
    CMD_ResetHardware = bytes([0])
    CMD_GetHardwareID = bytes([1])
    CMD_GetSoftwareID = bytes([3])
    CMD_I2C_Config = bytes([30])
    CMD_I2C_Master_SW = bytes([31])
    CMD_Hello = bytes([35])
    CMD_SetVdd = bytes([150])
    CMD_MeasureVddIdd = bytes([156])


class HwUsbEvb90632(HwI2cHalMlx90632):
    def __init__(self, channel=0):
        ch_index = channel
        try:
            ch_index = int(channel[len("mlx://evb:90632/"):]) - 1
        except:
            ch_index = channel
            pass
        if sys.platform == "win32":
            self.channel = mlx90632.pympt.PyWinUsbChannel()
        else:
            self.channel = mlx90632.pympt.UsbHidChannel()
        self.channel.connect(ch_index)
        self.set_i2c_config()
        self.set_vdd (0.0)
        time.sleep(0.01)
        self.set_vdd (3.3)
        time.sleep(0.01)


    def set_i2c_config(self, clock=DEFAULT_I2C_TCLOCK, start=DEFAULT_I2C_TSTART, stop=DEFAULT_I2C_TSTOP, wr_delay=DEFAULT_I2C_TSTOP, t_hold_data=DEFAULT_I2C_THOLDDATA):
        MCK = 48054857 # Hz
        l_clock = int(round(clock / 1000000 / 12 * MCK - 39 / 12 + 1))
        if l_clock < 1:
            l_clock = 1
        l_start = int(round(start / 1000000 / 6 * MCK - 19 / 6 + 1))
        if l_start < 0:
            l_start = 0
        l_stop =int(round(stop / 1000000 / 6 * MCK - 10 / 6 + 1))
        if l_stop < 0:
            l_stop = 0
        l_wr_delay = int(round(wr_delay / 1000000 / 6 * MCK - 26 / 6 + 1))
        if l_wr_delay < 0:
            l_wr_delay = 0
        l_t_hold_data = int(round(t_hold_data / 1000000 / 6 * MCK - 10 / 6 + 1))
        if l_t_hold_data < 0:
            l_t_hold_data = 0

        cmd = Evb90632Commands.CMD_I2C_Config
        cmd += struct.pack("<lllll", l_clock, l_start, l_stop, l_wr_delay, l_t_hold_data)

        result = self.channel.send_command(cmd)
        if result is None:
            return False
        if len(result) == 1:
            if result[0] == cmd[0]:
                return None
        return False


    def get_hardware_id(self):
        hardware_id = self.channel.send_command(Evb90632Commands.CMD_GetHardwareID)
        r = {}
        r['vid'] = struct.unpack('<H', hardware_id[1:3])[0]
        r['pid'] = struct.unpack('<H', hardware_id[3:5])[0]

        (r['vendor_name'], r['product_name'], r['version'], d) = hardware_id[6:].decode().split('\x01', 3)

        return r


    def get_software_id(self):
        software_id = self.channel.send_command(Evb90632Commands.CMD_GetSoftwareID)

        r = {}
        (r['template_name'], r['template_version'], r['template_timestamp'], r['firmware_name'], r['firmware_version'], r['firmware_timestamp'], d) = software_id[1:].decode().split('\x01')
        return r


    def set_vdd(self, vdd=3.3):
        """Set Vdd of the sensor"""
        cmd = Evb90632Commands.CMD_SetVdd + bytes([0])
        cmd = cmd + struct.pack("<f", float(vdd))
        self.channel.send_command(cmd)


    def measure_vdd(self):
        """
        Measure Vdd&Idd of the sensor

        @:return (vdd, idd)
        """
        data = self.channel.send_command(Evb90632Commands.CMD_MeasureVddIdd)
        vdd = struct.unpack('<f', data[1:5])[0]
        idd = struct.unpack('<f', data[5:9])[0]
        return (vdd, idd)


    def get_hello(self):
        hello = self.channel.send_command(Evb90632Commands.CMD_Hello)
        return hello[1:].decode()


    def connect(self):
        pass


    def disconnect(self):
        return self.channel.disconnect()


    def i2c_read(self, i2c_addr, addr, count=1, unpack_format='H'):
        data_bytes = bytearray()

        cmd = Evb90632Commands.CMD_I2C_Master_SW
        cmd += struct.pack(">B", i2c_addr)
        cmd += struct.pack(">H", addr)
        cmd += struct.pack("<H", int(count*2))

        read = self.channel.send_command(cmd)

        if unpack_format is None:
            return bytes(list(read[1:]))

        results = struct.unpack(">{}{}".format(count, unpack_format), bytes(list(read[2:2+int(count*2)])))
        if count == 1:
            return results[0]
        return results

    def i2c_write(self, i2c_addr, addr, data):
        data_bytes = bytearray()

        if type(data) is list:
          for d in data:
            data_bytes.append((d>>8) & 0x00FF)
            data_bytes.append(d & 0x00FF)
        else:
            data_bytes.append((data>>8) & 0x00FF)
            data_bytes.append(data & 0x00FF)

        cmd = Evb90632Commands.CMD_I2C_Master_SW
        cmd += struct.pack(">B", i2c_addr)
        cmd += struct.pack(">H", addr)
        cmd += data_bytes
        cmd += struct.pack(">H", 0)

        result = self.channel.send_command(cmd)

        if result is not None and len(result) > 1:
            if result[0] == cmd[0]:
                return None
        return False


def main():
    i2c = HwUsbEvb90632()

    print (i2c.get_hello())

    print ("hardware_id:")
    for k, v in i2c.get_hardware_id().items():
        print ("- {:20s}: {}".format (k, v))

    print ("firmware_id:")
    for k, v in i2c.get_software_id().items():
        print ("- {:20s}: {}".format (k, v))

    print("READ1 ---------------------------------")
    d = i2c.i2c_read(0x3A, 0x4000, 1)
    print("0x4000: {} {:04X} {} {}".format(d, d, int(d/256), int(d%256)))
    d = i2c.i2c_read(0x3A, 0x4001, 1)
    print("0x4001: {} {:04X} {} {}".format(d, d, int(d/256), int(d%256)))
    print("READ2 ---------------------------------")
    print("0x4000-1: {}".format(i2c.i2c_read(0x3A, 0x4000, 2)))



if __name__ == '__main__':
    main()
