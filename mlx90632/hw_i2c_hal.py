import struct

class HwI2cHalMlx90632:
    support_buffer = False
    sensor_type = None
    pass

    def connect(self):
        print("connect function not implemented")

    def i2c_read(self, i2c_addr, addr, count=1):
        print("i2c_read function not implemented")
        return bytes([0] * count), 0

    def i2c_write(self, i2c_addr, addr, data):
        print("i2c_write function not implemented")
        return 0

    def get_sensor_type(self, i2c_addr):
        sensor, stat = self.i2c_read(i2c_addr, 0x240A, 2)
        sensor = struct.unpack(">H",sensor)[0]
        self.sensor_type = (sensor & 0x40) >> 6
        return self.sensor_type

    def get_hardware_id(self):
        return "HardWare Abstraction Layer (dummy)"
