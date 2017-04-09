import bits
import time

class MotorController(object):
    def __init__(self, bus, addr):
        self.bus = bus
        self.addr = addr

        self.motors = [Motor(self, c) for c in range(8)]

    def __write_i2c_block(self, addr, data):
	print "Writing (%s, %s, %s)" % (addr, data[0], data[1:])
        self.bus.write_i2c_block_data(addr, data[0], data[1:])
    
    def write_servo(self, servo, value):
        write_val = int(value * 500)
        try:
            self.__write_i2c_block(self.addr, [(bits.make_field(servo, 5, 3)
                | bits.get_field(write_val, 8, 4)),
                bits.get_field(write_val, 0, 8)])
        except IOError as e:
            return False
        return True

class Motor(object):
    def __init__(self, motor_controller, channel):
        self.mc = motor_controller
        self.channel = channel
        self.value = 0

    def write(self, value):
        succ = self.mc.write_servo(self.channel, value)

        if(succ):
            self.value = value

        return succ

    def retry_write(self, value, interval = 0.05):
        for i in range(20):
            while(not self.write(value)):
                time.sleep(interval)

    def read(self, value):
        return self.value
