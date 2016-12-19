# coding:utf-8
'''
ScratchからBezelieを動かすサンプル
Copyright (c) 2016 Daisuke IMAI
This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
'''

import threading
import scratch
import bezerie

class Receiver(object):
    '''Scratchからの受信データの処理
    '''
    def __init__(self, bezelie):
        self.bezelie = bezelie

    def broadcast_handler(self, message):
        print('[receive] broadcast:', message)

    def sonsor_update_handler(self, **sensor_data):
        for name, value in sensor_data.items():
            print('[receive] sensor-update:', name, value)

if __name__ == '__main__':

    # Bezelieと接続しコントロールするためのインスタンス生成
    bez = bezelie.Control()
    bez.setTrim(head=7, back=2, stage=2)

    # Scratch接続のためのインスタンス生成
    rcv = Receiver(bez)
    rsc = scratch.RemoteSensorConnection(rcv.broadcast_handler, rcv.sonsor_update_handler)
