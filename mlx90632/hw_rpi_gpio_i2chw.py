from smbus2 import SMBus, i2c_msg
import time
import struct
import os
from mlx90632.hw_i2c_hal import HwI2cHalMlx90632
import platform


class HwRpiI2cHw(HwI2cHalMlx90632):
    support_buffer = False
    pass

    def __init__(self, channel=1):
        if isinstance(channel, str) and channel.startswith ("I2C-"):
            channel = int(channel[4:])

        if channel == 1 and platform.machine().startswith('armv'):
            os.system('raspi-gpio set 2 a0')
            os.system('raspi-gpio set 3 a0')
        self.i2c = SMBus(channel)

    def connect(self):
        pass

    def disconnect(self):
        pass

    def i2c_read(self, i2c_addr, addr, count=1, unpack_format='H'):
        addr_msb = addr >> 8 & 0x00FF
        addr_lsb = addr & 0x00FF

        write = i2c_msg.write(i2c_addr, [addr_msb, addr_lsb])
        read = i2c_msg.read(i2c_addr, count*2)
        self.i2c.i2c_rdwr(write, read)

        if unpack_format is None:
            return bytes(list(read))
        results = struct.unpack(">{}{}".format(count, unpack_format), bytes(list(read)))
        if count == 1:
            return results[0]
        return results

    def i2c_write(self, i2c_addr, addr, data):
        cmd = []
        reg_msb = addr >> 8
        cmd.append(addr & 0x00FF)

        if type(data) is list:
          for d in data:
            cmd.append((d>>8) & 0x00FF)
            cmd.append(d & 0x00FF)
        else:
            cmd.append((data>>8) & 0x00FF)
            cmd.append(data & 0x00FF)
        # print(reg_msb, cmd)
        self.i2c.write_i2c_block_data(i2c_addr, reg_msb, cmd)


        if (addr & 0xFF00) == 0x2400: # Wait after EEWRITE!
            time.sleep(0.010) # 10ms

        return 0

    def get_hardware_id(self):
        return "Raspberry Pi I2C Hardware"


def main():
    i2c = HwRpiI2cHw()
    d = i2c.i2c_read (0x3A, 0x4000, 9) # example to read 9 first words...
    print(struct.unpack(">9h", d[0]))



    i2c.i2c_write(0x3A, 0x3004, 0x0006)
    i2c.i2c_write(0x3A, 0x3005, 0x0006)


    d = i2c.i2c_read (0x3A, 0x3004, 2) # example to read 2 first words...
    print(struct.unpack(">2h", d[0]))

    i2c.i2c_write(0x3A, 0x3004, 0x0006)
    d = i2c.i2c_read (0x3A, 0x3004, 2) # example to read 2 first words...
    print(struct.unpack(">2h", d[0]))


    d = i2c.i2c_read (0x3A, 0x4000, 9) # example to read 9 first words...
    print(struct.unpack(">9h", d[0]))
    d = i2c.i2c_read (0x3A, 0x4000, 9) # example to read 9 first words...
    print(struct.unpack(">9h", d[0]))
    d = i2c.i2c_read (0x3A, 0x4000, 9) # example to read 9 first words...
    print(struct.unpack(">9h", d[0]))
    d = i2c.i2c_read (0x3A, 0x4000, 9) # example to read 9 first words...
    print(struct.unpack(">9h", d[0]))


    for i2c_addr in range(127):
        try:
            read_data = i2c.i2c.read_byte_data(i2c_addr, 0)
        except Exception as e:
            pass
        else:
            print ("0x{:02X} => ACK!".format (i2c_addr))


if __name__ == '__main__':
    main()
