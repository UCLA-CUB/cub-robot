import smbus as s
b = s.SMBus(1)

def mapval(v, il, ih, ol, oh):
    return ol + ((v - il)/(ih - il)) * (oh - ol)

class CameraController(object):
    REG_CTL_ADDR = 0x00
    REG_CTL_MAGIC_NUMBER = (0b101 << 5)
    REG_POS_ADDR = 0x02
    REG_TOTAL_LEN = 14
    I2C_CHECKSUM_MAGIC = (0xAA)

    def __init__(self, smbus, addr):
        self.smbus = smbus
        self.addr = addr
        self.max_retry = 10

        curdata = self.readall()

        self.baseband = curdata[6] + (curdata[7] << 8)
        self.maxband = curdata[8] + (curdata[9] << 8)

    def readall(self):
        saved_exception = None
        tries = 0

        while(tries < self.max_retry):
            tries += 1
            ret = self.smbus.read_i2c_block_data(self.addr, 0x00, self.REG_TOTAL_LEN + 1)
            chk = ret[-1]
            ret = ret[:-1]
            if(chk == reduce(lambda a,b : a^b, ret, self.I2C_CHECKSUM_MAGIC)):
                return ret

        raise Exception("exceeded maximum retries.") if not saved_exception else saved_exception
        

    def commit(self):
        self.sbus.write_byte_data(self.addr, self.REG_CTL_ADDR, self.REG_CTL_MAGIC_NUMBER)

    def __write_retry(self, reg, data):
        saved_exception = None
        tries = 0

        while(tries < self.max_retry):
            tries += 1
            try:
                self.smbus.write_i2c_block_data(self.addr, reg, data)
                if(data == self.smbus.read_i2c_block_data(self.addr, reg, len(data))):
                    return
            except Exception as e:
                saved_exception = e

        raise Exception("Exceeded maximum retries.") if not saved_exception else saved_exception

    def setPos(self, pitch, yaw):
        i_pitch = int(mapval(pitch, 0.0, 1.0, 1.0 * self.baseband, 1.0 * self.maxband))
        i_yaw = int(mapval(yaw, 0.0, 1.0, 1.0 * self.baseband, 1.0 * self.maxband))
        posdata = [i_pitch & 0xFF, (i_pitch >> 8) & 0xFF, i_yaw & 0xFF, (i_yaw >> 8) & 0xFF]

        print "(%f,%f) --> (%d,%d), %s" % (pitch,yaw,i_pitch,i_yaw,posdata)

        self.__write_retry(self.REG_POS_ADDR, posdata)
       

cc = CameraController(b, 0x40)
