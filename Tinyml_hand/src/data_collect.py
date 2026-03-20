import utime
from machine import Timer, I2C
from usr.mpu6500 import MPU6500, SF_DEG_S, SF_M_S2

# MPU6500 module was adjusted from:
# https://github.com/tuupola/micropython-mpu9250

# set up I2C serial communication protocol for Quectel
i2c = I2C(I2C.I2C1, I2C.STANDARD_MODE)

# create MPU6500 instance 
mpu6500 = MPU6500(i2c, accel_sf=SF_M_S2, gyro_sf=SF_DEG_S)

# read sensor function
def read_sensor(timer):
    accel = mpu6500.acceleration()
    gyro = mpu6500.gyro()
    print(utime.ticks_ms(), accel[0], accel[1], accel[2], gyro[0], gyro[1], gyro[2])

# hardware timer setup
timer = Timer(0)
timer.start(period=20, mode=Timer.PERIODIC, callback=read_sensor)
