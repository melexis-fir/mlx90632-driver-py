"""MptChannel for USB-HID using pywinusb class device"""

from mlx90632.pympt.core import *
from mlx90632.pympt.channel import *

import pywinusb.hid as hid

import queue
import time


DEBUG_PRINT=False


class PyWinUsbChannel(MptChannel):
    def __init__(self):
        self.in_buffer = b""
        self.dev = None
        self.in_report = None
        self.out_report = None
        self.hid_device_index = 0
        self.in_queue = queue.Queue()


    def in_handler(self, data):
        if DEBUG_PRINT:
            print ('in_handler', len(data), list(data[:10]), '...')
        self.in_queue.put(data[1:])


    def connect(self, hid_device_index):
        """Initialize USB connection to EVB90632"""
        if hid_device_index is None:
            hid_device_index = self.hid_device_index

        # find EVB90632
        all_devices = hid.HidDeviceFilter(vendor_name = "Melexis", product_name="EVB90632").get_devices()

        if len(all_devices) <= hid_device_index:
            return len(all_devices)
        
        self.dev = all_devices[hid_device_index]

        self.dev.open()

        self.in_report = self.dev.find_input_reports()[0]
        self.out_report = self.dev.find_output_reports()[0]
        self.dev.set_raw_data_handler(self.in_handler)


    def disconnect(self):
        if self.dev is not None:
            self.dev.close()
        self.dev = None
        self.in_report = None
        self.out_report = None
 

    def flush_buffers(self):
        self.in_buffer = b""
        self.in_queue.queue.clear()


    def write(self, data):
        if self.out_report is None:
            raise NotConnectedException()
        # HID reports must be sent with full buffer size data -> 64 bytes

        if not self.dev.is_plugged():
            raise NotConnectedException()

        n = len(data)
        if n % 64 != 0:
            data += b"\x00" * (64 - n % 64)
        for i in range(0, len(data), 64):
            if DEBUG_PRINT:
                print('Sending: {} ...'.format(list(data[i:i+10])))
            self.out_report.set_raw_data(bytes([0]) + data[i:i+64])
            self.out_report.send()
        if DEBUG_PRINT:
            print('----------')


    def read(self, nbytes):
        if self.in_report is None:
            raise NotConnectedException()

        if not self.dev.is_plugged():
            raise NotConnectedException()

        # we have setup the in_hander function, each time there is new data a new item appears in the in_queue
        # so all we have to do now is to get a message from that queue
        res_data = self.in_buffer
        self.in_buffer = b""
        while len(res_data) < nbytes:
            data = self.in_queue.get(block=True, timeout=5)
            if DEBUG_PRINT:
                print('PyWinUsbChannel: read:', data[:10], '...')
            res_data += bytearray(data)
        n = len(res_data) - nbytes
        if n > 0:
            self.in_buffer = res_data[-n:]
            res_data = res_data[:-n]
        if DEBUG_PRINT:
            print('PyWinUsbChannel: res_data:', list(res_data[:10]), '...')
        return res_data
