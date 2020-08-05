import serial
import struct
#import numpy 
#import string
#import binascii
import time

class InspireHandR:
    def __init__(self):
        #串口设置
        self.ser=serial.Serial('/dev/ttyUSB0',115200)
        self.ser.isOpen()
        self.hand_id = 1
        power1 = 400
        power2 = 400
        power3 = 400
        power4 = 400
        power5 = 400
        power6 = 800
        self.setpower(power1,power2,power3,power4,power5,power6)


        speed1 = 1000
        speed2 = 1000
        speed3 = 1000
        speed4 = 1000
        speed5 = 1000
        speed6 = 1000
        self.setspeed(speed1,speed2,speed3,speed4,speed5,speed6) 

        self.f1_init_pos = 400    #小指初始位置
        self.f2_init_pos = 400    #无名指初始位置
        self.f3_init_pos = 400    #中指初始位置
        self.f4_init_pos = 400    #食指指初始位置
        self.f5_init_pos = 1200    #拇指初始位置
        self.f6_init_pos = 700    #拇指转向掌心初始位置

        # 手部张开，测试用
        # self.f1_init_pos = 0    #小指初始位置
        # self.f2_init_pos = 0    #无名指初始位置
        # self.f3_init_pos = 0    #中指初始位置
        # self.f4_init_pos = 0    #食指指初始位置
        # self.f5_init_pos = 0    #拇指初始位置
        # self.f6_init_pos = 0    #拇指转向掌心初始位置

        self.reset()

    #把数据分成高字节和低字节
    def data2bytes(self,data):
        rdata = [0xff]*2
        if data == -1:
            rdata[0] = 0xff
            rdata[1] = 0xff
        else:
            rdata[0] = data&0xff
            rdata[1] = (data>>8)&(0xff)
        return rdata

    #把十六进制或十进制的数转成bytes
    def num2str(self,num):
        str = hex(num)
        str = str[2:4]
        if(len(str) == 1):
            str = '0'+ str
        str = bytes.fromhex(str)     
        #print(str)
        return str

    #求校验和
    def checknum(self,data,leng):
        result = 0
        for i in range(2,leng):

            result += data[i]
        result = result&0xff
        #print(result)
        return result

    def setpos(self,pos1,pos2,pos3,pos4,pos5,pos6):
        global hand_id
        if pos1 <-1 or pos1 >2000:
            print('数据超出正确范围：-1-2000')
            return
        if pos2 <-1 or pos2 >2000:
            print('数据超出正确范围：-1-2000')
            return
        if pos3 <-1 or pos3 >2000:
            print('数据超出正确范围：-1-2000')
            return
        if pos4 <-1 or pos4 >2000:
            print('数据超出正确范围：-1-2000')
            return
        if pos5 <-1 or pos5 >2000:
            print('数据超出正确范围：-1-2000')
            return
        if pos6 <-1 or pos6 >2000:
            print('数据超出正确范围：-1-2000')
            return
        
        datanum = 0x0F
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #写操作
        b[4] = 0x12
        
        #地址
        b[5] = 0xC2
        b[6] = 0x05
        
        #数据
        b[7] = self.data2bytes(pos1)[0]
        b[8] = self.data2bytes(pos1)[1]
        
        b[9] = self.data2bytes(pos2)[0]
        b[10] = self.data2bytes(pos2)[1]
        
        b[11] = self.data2bytes(pos3)[0]
        b[12] = self.data2bytes(pos3)[1]
        
        b[13] = self.data2bytes(pos4)[0]
        b[14] = self.data2bytes(pos4)[1]
        
        b[15] = self.data2bytes(pos5)[0]
        b[16] = self.data2bytes(pos5)[1]
        
        b[17] = self.data2bytes(pos6)[0]
        b[18] = self.data2bytes(pos6)[1]
        
        #校验和
        b[19] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        #print('发送的数据：',putdata)
        
        # print('发送的数据：')
        # for i in range(1,datanum+6):
        #     print(hex(putdata[i-1]))
            
        getdata= self.ser.read(9)
        #print('返回的数据：',getdata)
        # print('返回的数据：')
        # for i in range(1,10):
            # print(hex(getdata[i-1]))
        return

    #设置角度
    # angle1 = 0  #小拇指伸直1000，弯曲0
    # angle2 = 0  #无名指伸直1000弯曲0
    # angle3 = 0  #中指伸直1000，弯曲0
    # angle4 = 0  #食指伸直1000，弯曲0
    # angle5 = 1000 #大拇指伸直1000，弯曲0
    # angle6 = 1000 #大拇指转向掌心 0
    # setangle(angle1,angle2,angle3,angle4,angle5,angle6) 

    def setangle(self,angle1,angle2,angle3,angle4,angle5,angle6):
        if angle1 <-1 or angle1 >1000:
            print('数据超出正确范围：-1-1000')
            return
        if angle2 <-1 or angle2 >1000:
            print('数据超出正确范围：-1-1000')
            return
        if angle3 <-1 or angle3 >1000:
            print('数据超出正确范围：-1-1000')
            return
        if angle4 <-1 or angle4 >1000:
            print('数据超出正确范围：-1-1000')
            return
        if angle5 <-1 or angle5 >1000:
            print('数据超出正确范围：-1-1000')
            return
        if angle6 <-1 or angle6 >1000:
            print('数据超出正确范围：-1-1000')
            return
        
        datanum = 0x0F
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #写操作
        b[4] = 0x12
        
        #地址
        b[5] = 0xCE
        b[6] = 0x05
        
        #数据
        b[7] = self.data2bytes(angle1)[0]
        b[8] = self.data2bytes(angle1)[1]
        
        b[9] = self.data2bytes(angle2)[0]
        b[10] = self.data2bytes(angle2)[1]
        
        b[11] = self.data2bytes(angle3)[0]
        b[12] = self.data2bytes(angle3)[1]
        
        b[13] = self.data2bytes(angle4)[0]
        b[14] = self.data2bytes(angle4)[1]
        
        b[15] = self.data2bytes(angle5)[0]
        b[16] = self.data2bytes(angle5)[1]
        
        b[17] = self.data2bytes(angle6)[0]
        b[18] = self.data2bytes(angle6)[1]
        
        #校验和
        b[19] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('发送的数据：')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))
        
        getdata= self.ser.read(9)
        print('返回的数据：')
        for i in range(1,10):
            print(hex(getdata[i-1]))


    #设置力控阈值
    def setpower(self,power1,power2,power3,power4,power5,power6):
        if power1 <0 or power1 >1000:
            print('数据超出正确范围：0-1000')
            return
        if power2 <0 or power2 >1000:
            print('数据超出正确范围：0-1000')
            return
        if power3 <0 or power3 >1000:
            print('数据超出正确范围：0-1000')
            return
        if power4 <0 or power4 >1000:
            print('数据超出正确范围：0-1000')
            return
        if power5 <0 or power5 >1000:
            print('数据超出正确范围：0-1000')
            return
        if power6 <0 or power6 >1000:
            print('数据超出正确范围：0-1000')
            return
        
        datanum = 0x0F
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #写操作
        b[4] = 0x12
        
        #地址
        b[5] = 0xDA
        b[6] = 0x05
        
        #数据
        b[7] = self.data2bytes(power1)[0]
        b[8] = self.data2bytes(power1)[1]
        
        b[9] = self.data2bytes(power2)[0]
        b[10] = self.data2bytes(power2)[1]
        
        b[11] = self.data2bytes(power3)[0]
        b[12] = self.data2bytes(power3)[1]
        
        b[13] = self.data2bytes(power4)[0]
        b[14] = self.data2bytes(power4)[1]
        
        b[15] = self.data2bytes(power5)[0]
        b[16] = self.data2bytes(power5)[1]
        
        b[17] = self.data2bytes(power6)[0]
        b[18] = self.data2bytes(power6)[1]
        
        #校验和
        b[19] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('发送的数据：')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))
        
        getdata= self.ser.read(9)
        print('返回的数据：')
        for i in range(1,10):
            print(hex(getdata[i-1]))


    #设置速度
    def setspeed(self,speed1,speed2,speed3,speed4,speed5,speed6):
        if speed1 <0 or speed1 >1000:
            print('数据超出正确范围：0-1000')
            return
        if speed2 <0 or speed2 >1000:
            print('数据超出正确范围：0-1000')
            return
        if speed3 <0 or speed3 >1000:
            print('数据超出正确范围：0-1000')
            return
        if speed4 <0 or speed4 >1000:
            print('数据超出正确范围：0-1000')
            return
        if speed5 <0 or speed5 >1000:
            print('数据超出正确范围：0-1000')
            return
        if speed6 <0 or speed6 >1000:
            print('数据超出正确范围：0-1000')
            return
        
        datanum = 0x0F
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #写操作
        b[4] = 0x12
        
        #地址
        b[5] = 0xF2
        b[6] = 0x05
        
        #数据
        b[7] = self.data2bytes(speed1)[0]
        b[8] = self.data2bytes(speed1)[1]
        
        b[9] = self.data2bytes(speed2)[0]
        b[10] = self.data2bytes(speed2)[1]
        
        b[11] = self.data2bytes(speed3)[0]
        b[12] = self.data2bytes(speed3)[1]
        
        b[13] = self.data2bytes(speed4)[0]
        b[14] = self.data2bytes(speed4)[1]
        
        b[15] = self.data2bytes(speed5)[0]
        b[16] = self.data2bytes(speed5)[1]
        
        b[17] = self.data2bytes(speed6)[0]
        b[18] = self.data2bytes(speed6)[1]
        
        #校验和
        b[19] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('发送的数据：')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))
            
        getdata= self.ser.read(9)
        print('返回的数据：')
        for i in range(1,10):
            print(hex(getdata[i-1]))

    #读取驱动器实际的位置值
    def get_setpos(self):        
        datanum = 0x04
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #读操作
        b[4] = 0x11
        
        #地址
        b[5] = 0xC2
        b[6] = 0x05
        
        #读取寄存器的长度
        b[7] = 0x0C
        
        #校验和
        b[8] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        #print('发送的数据：',putdata)
        print('发送的数据：')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))
            
        getdata= self.ser.read(20)
        print('返回的数据：')
        for i in range(1,21):
            print(hex(getdata[i-1]))
        
        setpos = [0]*6
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                setpos[i-1] = -1
            else:
                setpos[i-1] = getdata[i*2+5] + (getdata[i*2+6]<<8)
        return setpos

    #读取设置角度
    def get_setangle(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #读操作
        b[4] = 0x11
        
        #地址
        b[5] = 0xCE
        b[6] = 0x05
        
        #读取寄存器的长度
        b[7] = 0x0C
        
        #校验和
        b[8] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('发送的数据：')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))
        
        getdata= self.ser.read(20)
        print('返回的数据：')
        for i in range(1,21):
            print(hex(getdata[i-1]))
        
        
        setangle = [0]*6
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                setangle[i-1] = -1
            else:
                setangle[i-1] = getdata[i*2+5] + (getdata[i*2+6]<<8)
        return setangle
    

    #读取驱动器设置的力控阈值
    def get_setpower(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #读操作
        b[4] = 0x11
        
        #地址
        b[5] = 0xDA
        b[6] = 0x05
        
        #读取寄存器的长度
        b[7] = 0x0C
        
        #校验和
        b[8] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('发送的数据：')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))
        
        getdata= self.ser.read(20)
        print('返回的数据：')
        for i in range(1,21):
            print(hex(getdata[i-1]))
        
        setpower = [0]*6
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                setpower[i-1] = -1
            else:
                setpower[i-1] = getdata[i*2+5] + (getdata[i*2+6]<<8)
        return setpower

    #读取驱动器实际的位置值
    def get_actpos(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #读操作
        b[4] = 0x11
        
        #地址
        b[5] = 0xFE
        b[6] = 0x05
        
        #读取寄存器的长度
        b[7] = 0x0C
        
        #校验和
        b[8] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('发送的数据：')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))
        
        getdata= self.ser.read(20)
        print('返回的数据：')
        for i in range(1,21):
            print(hex(getdata[i-1]))
        
        actpos = [0]*6
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                actpos[i-1] = -1
            else:
                actpos[i-1] = getdata[i*2+5] + (getdata[i*2+6]<<8)
        return actpos

    #读取实际的角度值
    def get_actangle(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #读操作
        b[4] = 0x11
        
        #地址
        b[5] = 0x0A
        b[6] = 0x06
        
        #读取寄存器的长度
        b[7] = 0x0C
        
        #校验和
        b[8] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        # print('发送的数据：')
        # for i in range(1,datanum+6):
        #     print(hex(putdata[i-1]))
        
        getdata= self.ser.read(20)
        # print('返回的数据：')
        # for i in range(1,21):
        #     print(hex(getdata[i-1]))
        
        actangle = [0]*6
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                actangle[i-1] = -1
            else:
                actangle[i-1] = getdata[i*2+5] + (getdata[i*2+6]<<8)
        return actangle

    #读取实际的受力
    def get_actforce(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #读操作
        b[4] = 0x11
        
        #地址
        b[5] = 0x2E
        b[6] = 0x06
        
        #读取寄存器的长度
        b[7] = 0x0C
        
        #校验和
        b[8] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        # print('发送的数据：')
        # for i in range(1,datanum+6):
        #     print(hex(putdata[i-1]))
        
        getdata= self.ser.read(20)
        # print('返回的数据：')
        # for i in range(1,21):
        #     print(hex(getdata[i-1]))
        
        actforce = [0]*6
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                actforce[i-1] = -1
            else:
                actforce[i-1] = getdata[i*2+5] + (getdata[i*2+6]<<8)
        
        # 串口收到的为又两个字节组成的无符号十六进制数，十进制的表示范围为0～65536，而实际数据为有符号的数据，表示力的不同方向，范围为-32768~32767，
        # 因此需要对收到的数据进行处理，得到实际力传感器的数据：当读数大于32767时，次数减去65536即可。
        for i in range(len(actforce)):
            if actforce[i] > 32767:
                actforce[i] = actforce[i] - 65536
        return actforce

    #读取电流
    def get_current(self):        
        datanum = 0x04
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #读操作
        b[4] = 0x11
        
        #地址
        b[5] = 0x3A
        b[6] = 0x06
        
        #读取寄存器的长度
        b[7] = 0x0C
        
        #校验和
        b[8] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('发送的数据：')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))
        
        getdata= self.ser.read(20)
        print('返回的数据：')
        for i in range(1,21):
            print(hex(getdata[i-1]))
        
        current = [0]*6
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                current[i-1] = -1
            else:
                current[i-1] = getdata[i*2+5] + (getdata[i*2+6]<<8)
        return current

    #读取故障信息
    def get_error(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #读操作
        b[4] = 0x11
        
        #地址
        b[5] = 0x46
        b[6] = 0x06
        
        #读取寄存器的长度
        b[7] = 0x06
        
        #校验和
        b[8] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('发送的数据：')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))
        
        getdata= self.ser.read(14)
        print('返回的数据：')
        for i in range(1,15):
            print(hex(getdata[i-1]))
        
        error = [0]*6
        for i in range(1,7):
            error[i-1] = getdata[i+6]
        return error

    #读取状态信息
    def get_status(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #读操作
        b[4] = 0x11
        
        #地址
        b[5] = 0x4C
        b[6] = 0x06
        
        #读取寄存器的长度
        b[7] = 0x06
        
        #校验和
        b[8] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
            self.ser.write(putdata)
        print('发送的数据：')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))
        
        getdata= self.ser.read(14)
        print('返回的数据：')
        for i in range(1,15):
            print(hex(getdata[i-1]))
        
        status = [0]*6
        for i in range(1,7):
            status[i-1] = getdata[i+6]
        return status
        

    #读取温度信息
    def get_temp(self):    
        datanum = 0x04
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #读操作
        b[4] = 0x11
        
        #地址
        b[5] = 0x52
        b[6] = 0x06
        
        #读取寄存器的长度
        b[7] = 0x06
        
        #校验和
        b[8] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('发送的数据：')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))
        
        getdata= self.ser.read(14)
        print('返回的数据：')
        for i in range(1,15):
            print(hex(getdata[i-1]))
        
        temp = [0]*6
        for i in range(1,7):
            temp[i-1] = getdata[i+6]
        return temp


    #清除错误
    def set_clear_error(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #写操作
        b[4] = 0x12
        
        #地址
        b[5] = 0xEC
        b[6] = 0x03
        
        #数据
        b[7] = 0x01
        
        #校验和
        b[8] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('发送的数据：')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))
        
        getdata= self.ser.read(9)
        print('返回的数据：')
        for i in range(1,10):
            print(hex(getdata[i-1]))


    #保存参数到FLASH
    def set_save_flash(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #写操作
        b[4] = 0x12
        
        #地址
        b[5] = 0xED
        b[6] = 0x03
        
        #数据
        b[7] = 0x01
        
        #校验和
        b[8] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('发送的数据：')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))
        
        getdata= self.ser.read(18)
        print('返回的数据：')
        for i in range(1,19):
            print(hex(getdata[i-1]))

    #力传感器校准
    def gesture_force_clb(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #写操作
        b[4] = 0x12
        
        #地址
        b[5] = 0xF1
        b[6] = 0x03
        
        #数据
        b[7] = 0x01
        
        #校验和
        b[8] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('发送的数据：')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))
        
        getdata= self.ser.read(18)
        print('返回的数据：')
        for i in range(1,19):
            print(hex(getdata[i-1]))
    #设置上电速度
    def setdefaultspeed(self,speed1,speed2,speed3,speed4,speed5,speed6):
        if speed1 <0 or speed1 >1000:
            print('数据超出正确范围：0-1000')
            return
        if speed2 <0 or speed2 >1000:
            return
        if speed3 <0 or speed3 >1000:
            return
        if speed4 <0 or speed4 >1000:
            return
        if speed5 <0 or speed5 >1000:
            return
        if speed6 <0 or speed6 >1000:
            return
        
        datanum = 0x0F
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #写操作
        b[4] = 0x12
        
        #地址
        b[5] = 0x08
        b[6] = 0x04
        
        #数据
        b[7] = self.data2bytes(speed1)[0]
        b[8] = self.data2bytes(speed1)[1]
        
        b[9] = self.data2bytes(speed2)[0]
        b[10] = self.data2bytes(speed2)[1]
        
        b[11] = self.data2bytes(speed3)[0]
        b[12] = self.data2bytes(speed3)[1]
        
        b[13] = self.data2bytes(speed4)[0]
        b[14] = self.data2bytes(speed4)[1]
        
        b[15] = self.data2bytes(speed5)[0]
        b[16] = self.data2bytes(speed5)[1]
        
        b[17] = self.data2bytes(speed6)[0]
        b[18] = self.data2bytes(speed6)[1]
        
        #校验和
        b[19] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        
        print('发送的数据：')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))
            
        getdata= self.ser.read(9)
        print('返回的数据：')
        for i in range(1,10):
            print(hex(getdata[i-1]))
    
    #设置上电力控阈值
    def setdefaultpower(self,power1,power2,power3,power4,power5,power6):
        if power1 <0 or power1 >1000:
            print('数据超出正确范围：0-1000')
            return
        if power2 <0 or power2 >1000:
            return
        if power3 <0 or power3 >1000:
            return
        if power4 <0 or power4 >1000:
            return
        if power5 <0 or power5 >1000:
            return
        if power6 <0 or power6 >1000:
            return
        
        datanum = 0x0F
        b = [0]*(datanum + 5)
        #包头
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id号
        b[2] = self.hand_id

        #数据个数
        b[3] = datanum
        
        #写操作
        b[4] = 0x12
        
        #地址
        b[5] = 0x14
        b[6] = 0x04
        
        #数据
        b[7] = self.data2bytes(power1)[0]
        b[8] = self.data2bytes(power1)[1]
        
        b[9] = self.data2bytes(power2)[0]
        b[10] = self.data2bytes(power2)[1]
        
        b[11] = self.data2bytes(power3)[0]
        b[12] = self.data2bytes(power3)[1]
        
        b[13] = self.data2bytes(power4)[0]
        b[14] = self.data2bytes(power4)[1]
        
        b[15] = self.data2bytes(power5)[0]
        b[16] = self.data2bytes(power5)[1]
        
        b[17] = self.data2bytes(power6)[0]
        b[18] = self.data2bytes(power6)[1]
        
        #校验和
        b[19] = self.checknum(b,datanum+4)
        
        #向串口发送数据
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('发送的数据：')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))
            
        getdata= self.ser.read(9)
        print('返回的数据：')
        for i in range(1,10):
            print(hex(getdata[i-1]))

    def soft_setpos(self,pos1,pos2,pos3,pos4,pos5,pos6):
        value0 = 0
        temp_value = [0,0,0,0,0,0]
        is_static = [0,0,0,0,0,0]
        static_value = [0,0,0,0,0,0]
        pos_value = [pos1,pos2,pos3,pos4,pos5,pos6] 
        n = 5
        diffpos = pos1 - self.f1_init_pos
        tic = time.time()
        for ii in range(5):
            #  self.setpos(pos1,pos2,pos3,pos4,pos5,pos6)
            #  print('==========================')
            actforce = self.get_actforce()
            print('actforce: ',actforce )
            for i,f in enumerate(actforce[0:5]):
                if is_static[i]:
                    continue 
                if f >1000:
                    continue
                if i ==5:#大拇指
                    if f >100: #如果手指受力大于100，就维持之前的位置 
                        is_static[i] = 1 #标记为静态手指，手指保持该位置不再动
                        static_value[i] = temp_value[i] #上一步的第i个手指位置
                else:
                    if f >50: #如果手指受力大于100，就维持之前的位置 
                        is_static[i] = 1 #标记为静态手指，手指保持该位置不再动
                        static_value[i] = temp_value[i] #上一步的第i个手指位置
            temp_value = pos_value.copy()
            for i in range(6):
                if is_static[i]:
                    pos_value[i] = static_value[i]
            pos1 = pos_value[0] #小拇指伸直0，弯曲2000
            pos2 = pos_value[1] #无名指伸直0，弯曲2000
            pos3 = pos_value[2] #中指伸直0，弯曲2000
            pos4 = pos_value[3] #食指伸直0，弯曲2000
            pos5 = pos_value[4] #大拇指伸直0，弯曲2000
            pos6 = pos_value[5] #大拇指转向掌心 2000
            self.setpos(pos1,pos2,pos3,pos4,pos5,pos6)
            toc = time.time()
            print('ii: %d,toc=%f'%(ii,toc - tic))


    def reset(self):
        pos1 = self.f1_init_pos #小拇指伸直0，弯曲2000
        pos2 = self.f2_init_pos #无名指伸直0，弯曲2000
        pos3 = self.f3_init_pos #中指伸直0，弯曲2000
        pos4 = self.f4_init_pos #食指伸直0，弯曲2000
        pos5 = self.f5_init_pos #大拇指伸直0，弯曲2000
        pos6 = self.f6_init_pos #大拇指转向掌心 2000
        self.setpos(pos1,pos2,pos3,pos4,pos5,pos6) 
        return

    def reset_0(self):
        pos1 = 0 #小拇指伸直0，弯曲2000
        pos2 = 0 #无名指伸直0，弯曲2000
        pos3 = 0 #中指伸直0，弯曲2000
        pos4 = 0 #食指伸直0，弯曲2000
        pos5 = 0#大拇指伸直0，弯曲2000
        pos6 = 0 #大拇指转向掌心 2000
        self.setpos(pos1,pos2,pos3,pos4,pos5,pos6) 
        return


if __name__ == "__main__":
    hand = InspireHandR()
    power1 = 400
    power2 = 400
    power3 = 400
    power4 = 400
    power5 = 400
    power6 = 800
    hand.setpower(power1,power2,power3,power4,power5,power6)

    speed1 = 1000
    speed2 = 1000
    speed3 = 1000
    speed4 = 1000
    speed5 = 1000
    speed6 = 500
    hand.setspeed(speed1,speed2,speed3,speed4,speed5,speed6) 
    temp_value = [0,0,0,0,0,0]
    is_static = [0,0,0,0,0,0]
    static_value = [0,0,0,0,0,0]
    tforce = 100

    while 1:
        value0 = 0
        temp_value = [0,0,0,0,0,0]
        is_static = [0,0,0,0,0,0]
        static_value = [0,0,0,0,0,0]

        for i in range(200):
            value = 10*i
            pos_value = [value]*6  #6个手指下一步的理论位置
            actforce = hand.get_actforce()
            for i,f in enumerate(actforce[0:5]):
                if is_static[i]:
                    continue 
                if f >1000:
                    continue
                if i ==4:#大拇指
                    if f >100: #如果手指受力大于100，就维持之前的位置 
                        is_static[i] = 1 #标记为静态手指，手指保持该位置不再动
                        static_value[i] = temp_value[i] #上一步的第i个手指位置
                else:
                    if f >100: #如果手指受力大于100，就维持之前的位置 
                        is_static[i] = 1 #标记为静态手指，手指保持该位置不再动
                        static_value[i] = temp_value[i] #上一步的第i个手指位置


            pos_value[5] =  pos_value[5] + 1000
            if pos_value[4] >2000: pos_value[4]  =2000
            if pos_value[5] >2000: pos_value[5]  =2000
            temp_value = pos_value.copy()
            
            for i in range(6):
                if is_static[i]:
                    pos_value[i] = static_value[i]

            pos1 = pos_value[0] #小拇指伸直0，弯曲2000
            pos2 = pos_value[1] #无名指伸直0，弯曲2000
            pos3 = pos_value[2] #中指伸直0，弯曲2000
            pos4 = pos_value[3] #食指伸直0，弯曲2000
            pos5 = pos_value[4] #大拇指伸直0，弯曲2000
            pos6 = pos_value[5] #大拇指转向掌心 2000
            hand.setpos(pos1,pos2,pos3,pos4,pos5,pos6)
            print('444444444444444444444444444')
            print('pos:',pos1,pos2,pos3,pos4,pos5,pos6)
            print("actforce：", actforce)
            print('5555555555555555')
            curr_pos = hand.get_actpos()
            print('currpos',curr_pos)
            time.sleep(0.005)
        
        time.sleep(2)
        hand.reset()
        time.sleep(2)