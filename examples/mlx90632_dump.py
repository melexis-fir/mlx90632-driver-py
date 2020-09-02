from mlx90632.mlx90632 import Mlx90632
from datetime import datetime


def main():
  dev = Mlx90632("I2C-1")
  # dev = Mlx90632("ftdi://ftdi:2232/1")
  # dev = Mlx90632("mlx://evb:90632/1")
  dev.init()
  dev.read_chipid()
  print ("chipid = {}".format (dev.chipid))
  print ("chipid = {}".format (dev.chipid_str))

  max_readings = 10
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
