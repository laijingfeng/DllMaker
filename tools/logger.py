#!/usr/bin/python
# encoding=utf-8
# version: 2016-12-25 19:56:54

import sys, os, ctypes, shutil
from datetime import datetime

class Logger(object):
    LEVEL_ERROR = 3
    LEVEL_WARN  = 2
    LEVEL_INFO  = 1

    COLOR_BLACK = 0 # black.
    COLOR_DARKBLUE = 1 # dark blue.
    COLOR_DARKGREEN = 2 # dark green.
    COLOR_DARKSKYBLUE = 3 # dark skyblue.
    COLOR_DARKRED = 4 # dark red.
    COLOR_DARKPINK = 5 # dark pink.
    COLOR_DARKYELLOW = 6 # dark yellow.
    COLOR_DARKWHITE = 7 # dark white.
    COLOR_DARKGRAY = 8 # dark gray.
    COLOR_BLUE = 9 # blue.
    COLOR_GREEN = 10 # green.
    COLOR_SKYBLUE = 11 # skyblue.
    COLOR_RED = 12 # red.
    COLOR_PINK = 13 # pink.
    COLOR_YELLOW = 14 # yellow.
    COLOR_WHITE = 15 # white.

    foregroundColor = [0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f]
    backgroundColor = [0x00,0x10,0x20,0x30,0x40,0x50,0x60,0x70,0x80,0x90,0xa0,0xb0,0xc0,0xd0,0xe0,0xf0]

    def __init__(self, level = LEVEL_INFO, file_name = 'logger'):
        self.__level__ = level #最低打印等级
        self.__out_file__ = 1
        #文件名可以设置，方便多个模块的日志区分
        self.__file_name__ = file_name

    def __set_cmd_color__(self, color):
        std_out_handle = ctypes.windll.kernel32.GetStdHandle(-11)
        Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(std_out_handle, color)
        return Bool

    def __set_cmd_default_color__(self):
        self.__set_cmd_color__(self.foregroundColor[self.COLOR_WHITE] | self.backgroundColor[self.COLOR_BLACK])
    
    def __log__(self, level, content, foreColor = COLOR_WHITE, backColor = COLOR_BLACK):
        
        self.__set_cmd_color__(self.foregroundColor[foreColor] | self.backgroundColor[backColor])
        print '{}|{}|{}'.format(datetime.now().strftime('%Y-%m-%d %I:%M:%S'), level, content)
        self.__set_cmd_default_color__()
        
        if self.__out_file__ == 1:
            with open('{}.log'.format(self.__file_name__),'a') as f:
                f.write('{}|{}|{}\n'.format(datetime.now().strftime('%Y-%m-%d %I:%M:%S'), level, content))

    def set_level(self, level):
        self.__level__ = level

    def reset(self):
        if os.path.exists(self.__file_name__ + '.log'):
            shutil.copy(self.__file_name__ + '.log', self.__file_name__ + '-prev.log')
            os.remove(self.__file_name__ + '.log')
        self.__log__('SYS', 'reset log')
        # 增加一句系统LOG，避免LOG为空，监听文件没了，同时也好看有响应

    def info(self, content, foreColor = COLOR_WHITE, backColor = COLOR_BLACK):
        if self.__level__ <= self.LEVEL_INFO:
            self.__log__('INFO', content, foreColor, backColor)

    def warn(self, content, foreColor = COLOR_YELLOW, backColor = COLOR_BLACK):
        if self.__level__ <= self.LEVEL_WARN:
            self.__log__('WARN', content, foreColor, backColor)

    def error(self, content, foreColor = COLOR_RED, backColor = COLOR_BLACK):
        if self.__level__ <= self.LEVEL_ERROR:
            self.__log__('ERROR', content, foreColor, backColor)
