# coding:utf-8
'''
ScratchからBezelieを動かすサンプル
Copyright (c) 2016 Daisuke IMAI
This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
'''

import sys
import time
import threading
import scratch
import bezelie

class Receiver(object):
    '''Scratchからの受信データの処理
    '''
    def __init__(self, bezelie):
        self.bezelie = bezelie

    def broadcast_handler(self, message):
        print('[receive] broadcast:', message)
        command_data = message.split(':')
        if len(command_data) > 2:
            if command_data[0] == u'move':
                if len(command_data) == 3:
                    if command_data[1] == u'head':
                        try:
                            self.bezelie.moveHead(int(command_data[2]))
                        except:
                            pass
                    if command_data[1] == u'back':
                        try:
                            self.bezelie.moveBack(int(command_data[2]))
                        except:
                            pass
                    if command_data[1] == u'stage':
                        try:
                            self.bezelie.moveStage(int(command_data[2]))
                        except:
                            pass
            if command_data[0] == u'talk':
                # talk関連コマンドを入れればtalkも可能に
                pass
            if command_data[0] == u'led':
                # led関連コマンドを入れればledも可能に
                pass

    def sonsor_update_handler(self, **sensor_data):
        for name, value in sensor_data.items():
            print('[receive] sensor-update:', name, value)
            command_data = name.split(':')
            if len(command_data) > 2:
                if command_data[0] == 'bezelie':
                    if command_data[1] == u'head':
                        self.bezelie.moveHead(value)
                    if command_data[1] == u'back':
                        self.bezelie.moveBack(value)
                    if command_data[1] == u'stage':
                        self.bezelie.moveStage(value)

if __name__ == '__main__':

    scratchhost = '127.0.0.1'

    # 引数処理
    param = sys.argv
    if len(param) > 1:
        # 引数がついていればScratchの接続先として利用
        scratchhost = param[1]

    # Bezelieと接続しコントロールするためのインスタンス生成
    bez = bezelie.Control()
    bez.setTrim(head=7, back=2, stage=2)

    # Scratch接続のためのインスタンス生成
    rcv = Receiver(bez)
    rsc = scratch.RemoteSensorConnection(rcv.broadcast_handler, rcv.sonsor_update_handler)
    rsc.connect(host=scratchhost)

    while(True):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print " Interrupted by Keyboard"
            rsc.disconnect()
            exit()
