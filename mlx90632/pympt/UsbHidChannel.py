"""MptChannel for USB-HID class device"""
from mlx90632.pympt.core import *
from mlx90632.pympt.channel import *
import time

try:
    import hid
# requires installing the binary package hidapi
# https://github.com/apmorton/pyhidapi#installing-hidapi
except ImportError as e:
    print ("The python package 'hid' requires installing the binary package hidapi")
    print ("https://github.com/apmorton/pyhidapi#installing-hidapi")
    print ("for debian/ubuntu: ")
    print ("")
    print ("sudo apt update")
    print ("sudo apt install libhidapi-libusb0")
    print ("")
    raise ImportError(e)


DEBUG_PRINT=False

VID = 0x03e9
PID = 0x0019


class UsbHidChannel(MptChannel):
    def __init__(self):
        self.in_buffer = b""
        self.hid = None
        self.timeout_ms = 300

    def connect(self, ch_index):
        """Initialize USB connection to EVB90632"""
        # find EVB90632

        hid_enumerate = hid.enumerate(VID, PID)
        if hid_enumerate is None:
            print ("no EVB found!")
            return False

        if len(hid_enumerate) <= ch_index:
            print ("no EVB at index {} found!".format(ch_index+1))
            return False

        self.hid = hid.Device(path=hid_enumerate[ch_index]['path'])

        if self.hid is None:
            print ("no EVB found!")
            return False

        self.flush_buffers()
        return True


    def disconnect(self):
        if self.hid is not None:
            self.flush_buffers()
            self.hid.close()
            self.hid = None


    def flush_buffers(self):
        self.in_buffer = b""
        while True:
            try:
                r = self.hid.read(64, 1)
                if r == b'':
                    break
            except Exception as e:
                break


    def write(self, data):
        self.flush_buffers()
        if self.hid is None:
            raise NotConnectedException()
        # HID reports must be sent with full buffer size data -> 64 bytes
        n = len(data)
        if n % 64 != 0:
            data += b"\x00" * (64 - n % 64)
        for i in range(0, len(data), 64):
            if DEBUG_PRINT:
                time.sleep(0.1)
                print('Sending: {}'.format(data[i:i+64]))
            self.hid.write(data[i:i+64])
        if DEBUG_PRINT:
            time.sleep(0.1)
            print('----------')


    def read(self, nbytes):
        if self.hid is None:
            raise NotConnectedException()
        res_data = self.in_buffer
        self.in_buffer = b""
        while len(res_data) < nbytes:
            try:
                data = self.hid.read(64, self.timeout_ms)
            except Exception as e:
                print ('error', e)
                continue

            if DEBUG_PRINT:
                time.sleep(0.1)
                print(data)
            res_data += data
        n = len(res_data) - nbytes
        if n > 0:
            self.in_buffer = res_data[-n:]
            res_data = res_data[:-n]
        return res_data
