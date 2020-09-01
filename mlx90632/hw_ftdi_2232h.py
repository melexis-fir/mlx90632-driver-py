from pyftdi.i2c import I2cController
import time
import struct
import os
from hw_i2c_hal import HwI2cHalMlx90632
import platform


class HwFtdi2232h(HwI2cHalMlx90632):
    support_buffer = False
    pass

    def __init__(self, channel=1):
        try:
            ch_nr = int(channel)
            channel = 'ftdi://ftdi:2232h/{}'.format(ch_nr)
        except:
            pass
        self.i2c = I2cController()
        self.i2c.configure(channel)

    def connect(self):
        pass

    def i2c_read(self, i2c_addr, addr, count=1, unpack_format='H'):

        slave = self.i2c.get_port(i2c_addr)

        addr_msb = addr >> 8 & 0x00FF
        addr_lsb = addr & 0x00FF

        read = slave.exchange(struct.pack(">1H", addr), 2*count)

        if unpack_format is None:
            return bytes(list(read))
        results = struct.unpack(">{}{}".format(count, unpack_format), bytes(list(read)))
        if count == 1:
            return results[0]
        return results

    def i2c_write(self, i2c_addr, addr, data):
        data_bytes = bytearray()
        slave = self.i2c.get_port(i2c_addr)

        if type(data) is list:
          for d in data:
            data_bytes.append((d>>8) & 0x00FF)
            data_bytes.append(d & 0x00FF)
        else:
            data_bytes.append((data>>8) & 0x00FF)
            data_bytes.append(data & 0x00FF)

        slave.write(struct.pack(">1H", addr) + data_bytes)

        if (addr & 0xFF00) == 0x2400: # Wait after EEWRITE!
            time.sleep(0.010) # 10ms

        return 0

    def get_hardware_id(self):
        return "FT2232H I2C master"


def main():
    i2c = HwFtdi2232h()
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)



    i2c.i2c_write(0x3A, 0x3004, 0x0006)
    i2c.i2c_write(0x3A, 0x3005, 0x0006)


    d = i2c.i2c_read (0x3A, 0x3004, 2) # example to read 2 first words...
    print (d)

    i2c.i2c_write(0x3A, 0x3004, 0x0006)
    d = i2c.i2c_read (0x3A, 0x3004, 2) # example to read 2 first words...
    print (d)


    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)
    d = i2c.i2c_read (0x3A, 0x4000, 9, 'h') # example to read 9 first words...
    print (d)




if __name__ == '__main__':
    main()
