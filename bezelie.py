# -*- coding: utf-8 -*-
# Bezelie Python Module for Raspberry Pi
import RPi.GPIO as GPIO
from time import sleep
import smbus
import math
import scratch

bus = smbus.SMBus(1)

class Control(object):

    def __init__(self, address_pca9685=0x40, dutyMax=490, dutyMin=110, dutyCenter=300, steps=1):

        self.headNow = dutyCenter
        self.backNow = dutyCenter
        self.stageNow = dutyCenter

    # Definitions
    def initPCA9685(self):
        bus.write_byte_data(self.address_pca9685, 0x00, 0x00)
        freq = 0.9 * 50
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        prescale = int(math.floor(prescaleval + 0.5))
        oldmode = bus.read_byte_data(address_pca9685, 0x00)
        newmode = (oldmode & 0x7F) | 0x10
        bus.write_byte_data(address_pca9685, 0x00, newmode)
        bus.write_byte_data(address_pca9685, 0xFE, prescale)
        bus.write_byte_data(address_pca9685, 0x00, oldmode)
        sleep(0.005)
        bus.write_byte_data(address_pca9685, 0x00, oldmode | 0xa1)

    def setTrim(self):

    def setPCA9685Duty(self, channel, on, off):
        channelpos = 0x6 + 4*channel
        try:
            bus.write_i2c_block_data(address_pca9685, channelpos, [on&0xFF, on>>8, off&0xFF, off>>8])
        except IOError:
            pass

    def moveServo (self, id, degree, trim, max, min, speed, now):
        dst = (dutyMin - dutyMax) * (degree + trim + 90) / 180 + dutyMax
        if speed == 0:
            setPCA9685Duty(id, 0, dst)
            sleep(0.001 * math.fabs(dst - now))
            now = dst
        if dst > max:
            dst = max
        if dst < min:
            dst = min
        while (now != dst):
            if now < dst:
                now += steps
                if now > dst:
                    now = dst
            else:
                now -= steps
                if now < dst:
                    now = dst
            setPCA9685Duty(id, 0, now)
            sleep(0.004 * steps *(speed))
        return (now)

    def moveCenter (self):
        moveHead (0)
        moveBack (0)
        moveStage (0)

    def moveHead (self, degree, speed=1):
        trim = 0       # Head servo adjustment
        max = 490     # Downward limit
        min = 110     # Upward limit
        self.headNow = moveServo (2, degree, trim, max, min, speed, self.headNow)

    def moveBack (self, degree, speed=1):
        trim = 0       # Back servo adjustment
        max = 490     # AntiClockwise limit
        min = 110     # Clockwise limit
        self.backNow = moveServo (1, degree, trim, max, min, speed, self.backNow)

    def moveStage (self, degree, speed=1):
        trim = 0      # Stage servo adjustment
        max = 490    # AntiClockWise limit
        min = 110    # Clocwise limit
        self.stageNow = moveServo (0, degree, adj, max, min, speed, self.stageNow)
