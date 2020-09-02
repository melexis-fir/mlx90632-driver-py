"""A python interface for Mlx90632."""

from datetime import datetime
from sys import platform
import atexit

# MLX90632 mode
STEP_SLEEP = 1
STEP = 2
CONTINIOUS = 3

# ACCURACY_RANGE
MEDICAL = 1
COMMERCIAL = 2


class Mlx90632:
    def __init__(self, hw, i2c_addr=0x3A):
        self.word_size_bits = 16
        self.startup = False
        self.use_only_latest_IR_adc = False
        self.reload_calibration_data_on_brownout = True
        self.wait_new_data_until_end_of_full_cycle = False
        self.hw = None
        if hw is None:
            hw = 'auto'
        if isinstance(hw, str):
            if hw.startswith("I2C-"):
                from mlx90632.hw_rpi_gpio_i2chw import HwRpiI2cHw
                # from hw_rpi_gpio_i2chw import HwRpiI2cHw
                self.hw = HwRpiI2cHw(hw)
            if hw.startswith("I2CBB-"):
                from mlx90632.hw_rpi_gpio_bitbang import HwRpiGpioBitBang
                # from hw_rpi_gpio_bitbang import HwRpiGpioBitBang
                self.hw = HwRpiGpioBitBang(hw)
            if hw.startswith("ftdi://ftdi:2232"):
                from mlx90632.hw_ftdi_2232h import HwFtdi2232h
                # from hw_ftdi_2232h import HwFtdi2232h
                self.hw = HwFtdi2232h(hw)
            if hw.startswith("mlx://evb:90632"):
                from mlx90632.hw_usb_evb90632 import HwUsbEvb90632
                # from hw_usb_evb90632 import HwUsbEvb90632
                self.hw = HwUsbEvb90632(hw)

        else:
            self.hw = hw
        self.i2c_addr = i2c_addr

        self.connect()

        atexit.register(self.disconnect)


    def init(self):
        self.read_status()
        self.clear_new_data()
        self.read_status()
        self.read_control()
        self.read_calibration_data()

    def read_calibration_data(self):
        
        trim_version = 0
        dsp_version = 0
        cal_Ea = 74.0
        cal_Eb = 22260.0
        cal_Fa = 7e-7
        cal_Ga = -0.0005
        cal_Fb = -0.0004
        cal_Gb = 0
        cal_Ka = 0

        w = self.hw.i2c_read (self.i2c_addr, 0x240B)
        trim_version = w >> 8
        dsp_version = w & 0x0FF

        w = self.hw.i2c_read (self.i2c_addr, 0x2424)
        EE_cal_Ea = w
        w = self.hw.i2c_read (self.i2c_addr, 0x2425)
        EE_cal_Ea += (w * 2**16)
        cal_Ea = EE_cal_Ea * 2**-16

        w = self.hw.i2c_read (self.i2c_addr, 0x2426)
        EE_cal_Eb = w
        w = self.hw.i2c_read (self.i2c_addr, 0x2427)
        EE_cal_Eb += (w * 2**16)
        cal_Eb = EE_cal_Eb * 2**-8
      
        w = self.hw.i2c_read (self.i2c_addr, 0x2428)
        EE_cal_Fa = w
        w = self.hw.i2c_read (self.i2c_addr, 0x2429)
        EE_cal_Fa += (w * 2**16)
        cal_Fa = EE_cal_Fa * 2**-46
      
        w = self.hw.i2c_read (self.i2c_addr, 0x242A)
        EE_cal_Fb = w
        w = self.hw.i2c_read (self.i2c_addr, 0x242B)
        EE_cal_Fb += (w * 2**16)
        if (EE_cal_Fb & 0x80000000):
          EE_cal_Fb -= 2**32
        cal_Fb = EE_cal_Fb * 2**-36
      
        w = self.hw.i2c_read (self.i2c_addr, 0x242C)
        EE_cal_Ga = w
        w = self.hw.i2c_read (self.i2c_addr, 0x242D)
        EE_cal_Ga += (w * 2**16)
        if (EE_cal_Ga & 0x80000000):
          EE_cal_Ga -= 2**32
        cal_Ga = EE_cal_Ga * 2**-36
      
        w = self.hw.i2c_read (self.i2c_addr, 0x242E)
        EE_cal_Gb = w
        if (EE_cal_Gb & 0x8000):
          EE_cal_Gb -= 2**16
        cal_Gb = EE_cal_Gb * 2**-10
      
        w = self.hw.i2c_read (self.i2c_addr, 0x242F)
        EE_cal_Ka = w
        if (EE_cal_Ka & 0x8000):
          EE_cal_Ka -= 2**16
        cal_Ka = EE_cal_Ka * 2**-10
      
        w = self.hw.i2c_read (self.i2c_addr, 0x2481)
        EE_cal_Ha = w
        if (EE_cal_Ha & 0x8000):
          EE_cal_Ha -= 2**16
        cal_Ha = EE_cal_Ha * 2**-14
      
        w = self.hw.i2c_read (self.i2c_addr, 0x2482)
        EE_cal_Hb = w
        if (EE_cal_Hb & 0x8000):
          EE_cal_Hb -= 2**16
        cal_Hb = EE_cal_Hb * 2**-10

        w = self.hw.i2c_read (self.i2c_addr, 0x2430)
        EE_cal_VddMonOffset = w
        if (EE_cal_VddMonOffset & 0x8000):
          EE_cal_VddMonOffset -= 2**16
        cal_VddMonOffset = EE_cal_VddMonOffset

            
        self.calib_data = {
                'cal_Ea'  : cal_Ea, 
                'cal_Eb'  : cal_Eb, 
                'cal_Fa'  : cal_Fa, 
                'cal_Ga'  : cal_Ga, 
                'cal_Fb'  : cal_Fb, 
                'cal_Gb'  : cal_Gb, 
                'cal_Ka'  : cal_Ka, 
                'cal_Ha'  : cal_Ha,
                'cal_Hb'  : cal_Hb,
                'cal_VddMonOffset'  : cal_VddMonOffset,
                'EE_cal_Ea'  : EE_cal_Ea, 
                'EE_cal_Eb'  : EE_cal_Eb, 
                'EE_cal_Fa'  : EE_cal_Fa, 
                'EE_cal_Ga'  : EE_cal_Ga, 
                'EE_cal_Fb'  : EE_cal_Fb,
                'EE_cal_Gb'  : EE_cal_Gb,
                'EE_cal_Ka'  : EE_cal_Ka,
                'EE_cal_Ha'  : EE_cal_Ha,
                'EE_cal_Hb'  : EE_cal_Hb,
                'EE_cal_VddMonOffset'  : EE_cal_VddMonOffset,
                'dsp_version'   : dsp_version,
                'trim_version'  : trim_version
        }
        self.set_brownout(use_cache=False)
        return self.calib_data

    def set_vdd(self, vdd):
        """Set Vdd of the sensor"""
        # if supported...
        if callable(getattr(self.hw, 'set_vdd', None)):
            self.hw.set_vdd(vdd)

    def get_refresh_rate(self):
        return self.frame_rate

    def clear_error(self):
        if callable(getattr(self.hw, 'clear_error', None)):
            self.hw.clear_error(self.i2c_addr)

    def write_ee_refresh_rate(self, refresh_rate, unit='Hz'):
        """
        Write the refresh rate to EEPROM
        :param frame_rate: the new frame rate for the sensor
        :param unit: 'Hz' or 'code'.
        """

        refresh_rate_code = refresh_rate
        if unit == 'Hz':
            refresh_rate_code = 2
            LUT = {64   : 7,
                   32   : 6, 
                   16   : 5, 
                    8   : 4, 
                    4   : 3, 
                    2   : 2, 
                    1   : 1, 
                    0.5 : 0, 
                  }
            if refresh_rate in LUT:
                refresh_rate_code = LUT[refresh_rate]

        ee_meas1 = self.hw.i2c_read (self.i2c_addr, 0x24E1)
        ee_meas2 = self.hw.i2c_read (self.i2c_addr, 0x24E2)

        ee_meas1 &= ~(0x07 << 8)
        ee_meas2 &= ~(0x07 << 8)

        ee_meas1 |= (refresh_rate_code & 0x07) << 8
        ee_meas2 |= (refresh_rate_code & 0x07) << 8

        self.write_ee(0x24E1, ee_meas1)
        self.write_ee(0x24E2, ee_meas2)


    def write_ee(self, address, data):
        """
          Writing to EEPROM is prohibited during application run; use only at end-of-line calibration.

        """
        old_data = self.hw.i2c_read (self.i2c_addr, address)
        if data != old_data: # if update required
            # erase the address when not yet zero
            if old_data != 0:
                self.hw.i2c_write (self.i2c_addr, 0x3005, 0x554C)
                self.hw.i2c_write (self.i2c_addr, address, 0x0000)
                self.hw.i2c_write (self.i2c_addr, 0x3005, 0x0006)

            # write the new data (when new data is different from zero)
            if data != 0:
                self.hw.i2c_write (self.i2c_addr, 0x3005, 0x554C)
                self.hw.i2c_write (self.i2c_addr, address, data)
                self.hw.i2c_write (self.i2c_addr, 0x3005, 0x0006)


    def measure_vdd(self):
        """
        Measure Vdd of the sensor

        @:return vdd
        """
        if callable(getattr(self.hw, 'measure_vdd', None)):
            return self.hw.measure_vdd()
        return None


    def get_hardware_id(self):
        """
        :return: bytes array representing the hardware id
        """
        return self.hw.get_hardware_id()


    def connect(self):
        """
        Do the necessary initialisation before measurements are taken

        procedure:
            poll until HW id received (timeout??)
            init SW I2C
            set vdd
            I2C:
                set refresh rate
                start conversion
            set evb refresh rate
        """
        self.hw.connect()
        self.reset()


    def disconnect(self):
        """
        """
        self.hw.disconnect()


    def i2c_read(self, addr, count=1, unpack_format='H'):
        results = self.hw.i2c_read(self.i2c_addr, addr, count, unpack_format)
        if count == 1:
            return results
        return list(results)


    def reset(self):
        # Soft reset via I2C command...
        self.hw.i2c_write (self.i2c_addr, 0x3005, 0x0006)
        self.startup = True


    def read_vddmonitor_data(self):
        raw_data = self.hw.i2c_read (self.i2c_addr, 0x4000, 3, 'h')
        # print (raw_data)
        return raw_data


    def read_measurement_data(self):
        raw_data = self.hw.i2c_read (self.i2c_addr, 0x4003, 6, 'h')
        self.clear_new_data(False)
        # print (raw_data)
        return raw_data


    def read_status(self):
        self.reg_status = self.hw.i2c_read (self.i2c_addr, 0x3FFF)
        self.reg_status_brownout = self.reg_status & 0x0100 != 0
        self.reg_status_cycle_position = (self.reg_status & 0x007C) >> 2
        self.reg_status_new_data = self.reg_status & 0x0001 != 0
        return self.reg_status


    def read_control(self):
        self.reg_control = self.hw.i2c_read (self.i2c_addr, 0x3001)
        self.reg_control_mode = (self.reg_status & 0x006) >> 1
        self.reg_control_soc = (self.reg_status & 0x008) >> 3
        self.reg_control_table_select = (self.reg_status & 0x01F0) >> 4
        return self.reg_control


    def read_ee_product_code(self):
        self.ee_product_code = self.hw.i2c_read (self.i2c_addr, 0x2409)
        self.ee_product_code_accuracy_range = (self.ee_product_code & 0x007) >> 0
        return self.ee_product_code


    def read_ee_pc_accuracy_range(self):
        self.read_ee_product_code()
        return self.ee_product_code_accuracy_range


    def wait_new_data(self, timeout_seconds=-1):
        timeout = False
        start_date_time = datetime.now()
        while not timeout:
          if timeout_seconds >= 0:
            delta_time = (datetime.now() - start_date_time).total_seconds()
            if delta_time > timeout_seconds:
                timeout = True # but give the new_data bit one more chance!
          self.read_status()
          if self.reg_status_new_data:
            if self.startup or self.wait_new_data_until_end_of_full_cycle:
              if self.reg_status_cycle_position != 2:
                continue # wait longer, untill we have a full measurement cycle; at first time after startup; or when we require a full cycle!
            self.startup = False
            return True
        return False


    def poll_new_data(self):
        self.read_status()
        if self.reg_status_new_data:
          return True
        return False


    def clear_new_data(self, use_cache=True):
        if not use_cache:
            self.read_status()
        new_status_value = self.reg_status & ~0x0001
        self.hw.i2c_write (self.i2c_addr, 0x3FFF, new_status_value)


    def set_brownout(self, use_cache=True):
        if not use_cache:
            self.read_status()
        new_status_value = self.reg_status | 0x0100
        self.hw.i2c_write (self.i2c_addr, 0x3FFF, new_status_value)


    def write_control_mode(self, mode=CONTINIOUS):
        self.read_control()
        new_control_value = self.reg_control & ~0x0006
        new_control_value |= ((mode & 0x03) << 1) 
        self.hw.i2c_write (self.i2c_addr, 0x3001, new_control_value)


    def write_control_soc(self, value=True):
        self.read_control()
        new_control_value = self.reg_control & ~0x0008
        if value:
            new_control_value |= 0x0008
        self.hw.i2c_write (self.i2c_addr, 0x3001, new_control_value)


    def do_compensation(self, raw_data):
        """
        Calculates the temperatures based on raw_data and calibration_data
        :param raw_data: the raw data from 'read_measurement_data'
        :return: the calculated TA/TO
        """
        if self.reload_calibration_data_on_brownout:
            if self.reg_status_brownout:
                self.read_calibration_data()

        Ea = self.calib_data['cal_Ea']   
        Eb = self.calib_data['cal_Eb']  
        Fa = self.calib_data['cal_Fa']    
        Ga = self.calib_data['cal_Ga']   
        Gb = self.calib_data['cal_Gb']   
        Fb = self.calib_data['cal_Fb']   
        Ha = self.calib_data['cal_Ha']   
        Hb = self.calib_data['cal_Hb']   
        Ka = self.calib_data['cal_Ka']   
    
        Xa = raw_data[5] + Gb * raw_data[2] / 4 / 3.0
        Xb = raw_data[5] + Ka * raw_data[2] / 4 / 3.0

        Ya = raw_data[2] / 4 / 3.0 / Xa * 2**19

        Xc = None
        if self.use_only_latest_IR_adc:
            if self.reg_status_cycle_position == 1:
                Xc = (raw_data[0] + raw_data[1])/2
            if self.reg_status_cycle_position == 2:
                Xc = (raw_data[3] + raw_data[4])/2
        else:
            Xc = (raw_data[0] + raw_data[1] + raw_data[3] + raw_data[4])/4

        Yb = Xc / 4 / 3.0 / Xb * 2**19
    
        if Ea == 0:
          return (-999,-999)
    
        TA_computed = (Ya - Eb) / Ea + 25
        TO_computed = 34
    
        # iterate 3 times:
        for i in range (3):
          Za = Ha * Fa * (1 + Ga * (TO_computed - 25) + Fb * (TA_computed - 25))
          TO_computed = (Yb/Za + (TA_computed+273.15)**4)**0.25 - 273.15 - Hb
    
        return (TA_computed, TO_computed)


    def read_temperature(self):
        raw_data = self.read_measurement_data()
        return self.do_compensation(raw_data)


    def read_chipid(self):
        self.chipid_words = self.hw.i2c_read (self.i2c_addr, 0x2405, 4)
        self.chipid = self.chipid_words[0] + self.chipid_words[1] * (2**16) + self.chipid_words[2] * (2**32)
        self.chipid_str = "{:04X}-{:04X}-{:04X}".format(self.chipid_words[2], self.chipid_words[1], self.chipid_words[0])
        return self.chipid


    def read_vddmonitor(self):
        raw_data = self.read_vddmonitor_data()
        if self.reload_calibration_data_on_brownout:
            if self.reg_status_brownout:
                self.read_calibration_data()
        cal_VddMonOffset = self.calib_data['cal_VddMonOffset']
        if cal_VddMonOffset < 10000:
            cal_VddMonOffset = 22841
        if cal_VddMonOffset == 22841:
            cal_VddMonOffset -= 150
        vddmon = (raw_data[0] + raw_data[1])/2
        vddmon -= cal_VddMonOffset
        vddmon /= 6920
        vddmon += 3.3
        return vddmon


    def force_read_vddmonitor(self):
        self.reset() # a reset will 'force' to run the initial steps in the table!
        self.clear_new_data()
        while True:
            self.read_status()
            if self.reg_status_new_data:
                break
        return self.read_vddmonitor()


def main():
    # demo to test the file.. get a single reading from EVB90632.
    # Should you want a more user friendly example, please have a look at Mlx90632_dump.py example.
    import time
    from MemFile import MemFile

        # evb_bin_file_name = evb_bin_file_name.format(id=self.chipid_str)

    # defaults
    max_readings = 10

    # dev = Mlx90632("I2C-1")
    # dev = Mlx90632("ftdi://ftdi:2232/1")
    dev = Mlx90632("mlx://evb:90632/1")

    dev.init()
    dev.read_chipid()
    # dev.write_ee_refresh_rate(2)

    print ("chipid = {}".format (dev.chipid))
    print ("chipid = {}".format (dev.chipid_str))

    # example to read entire EEPROM and write to file (hex- & bin-file)
    print ("\n\nreading EEPROM content to {}.hex/.bin".format(dev.chipid_str))
    m = MemFile()
    word_data = dev.i2c_read(0x2400, 256, 'H')
    m.add_16(0x2400, word_data)
    m.write_evb_bin_file(dev.chipid_str)
    m.write_hex_file(dev.chipid_str)
    print ("done.")


    # example read memory file and compare with eeprom content read
    print ('\n\nreading eeprom memory dump, and compare with actual content...')
    h = MemFile(dev.chipid_str + '.hex')
    # h = MemFile(dev.chipid_str + '.bin')
    print ("")
    print ("addr: data")
    print ("----  ----")
    word_data = dev.i2c_read(0x2400, 256, 'H')
    changed = False
    for p in h.get_address_data_pairs():
        data = word_data.pop(0)
        print ("{:04X}: {:04X} -- {:04X} -- {}".format (p[0], p[1], data, data==p[1]))
        if data != p[1]:
            changed = True
    if changed:
        print ("data differs!")
    else:
        print ("data matches!")

    print ('accuracy_range: {}'.format(dev.read_ee_pc_accuracy_range()))

    reading_count = 0
    previous_time = datetime.now()
    dev.reset()

    print ("\n\nReading {}x".format(max_readings))


    while reading_count < max_readings:
        raw_data = None
        try:
            if dev.wait_new_data(2):
                raw_data = dev.read_measurement_data()
                dev.reset()
                dev.set_brownout()

            # print (raw_data)
        except Exception as e:
            dev.clear_error()
            print(e)
            pass

        if raw_data is not None:
            ta, to = dev.do_compensation(raw_data)
            now_time = datetime.now()
            delta_time = now_time - previous_time
            previous_time = now_time

            print("TA = {:6.2f}  | TO = {:6.2f}  | VddMon = {:6.2f}  -- {}".format (ta, to, dev.read_vddmonitor(), str(delta_time)))
        
            reading_count += 1

    dev.disconnect()


if __name__ == '__main__':
    main()
