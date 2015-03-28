# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 20:55:22 2013

@author: Yuxiang Wang
"""


import ctypes
import time

User32dll = ctypes.windll.User32

def main():
    pass


class POINT(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_ulong),
        ('y', ctypes.c_ulong),
        ]


def timer_tick():
    point = POINT()
    User32dll.GetCursorPos(ctypes.byref(point))
    print(point.x, point.y)


if __name__ == '__main__':
    for i in range(10):
        timer_tick()
        time.sleep(1)
        



