from mlx90632.mlx90632 import Mlx90632

dev = Mlx90632('mlx://evb:90632/1')              # establish communication between EVB90632 and PC
dev.init()                                       # read EEPROM and pre-compute calibration parameters.
dev.wait_new_data()                              # wait until there is new data.
raw_data = dev.read_measurement_data()           # read new measurement data.
ta, to = dev.do_compensation(raw_data)           # compute the temperature.
print ("TA: {} -- TO: {} DegC".format (ta, to))  # print the results
