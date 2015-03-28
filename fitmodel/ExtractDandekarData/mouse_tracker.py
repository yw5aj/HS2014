# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 20:55:22 2013

@author: Yuxiang Wang
"""


import pyHook
import pythoncom
import ctypes


def main():
    hm = pyHook.HookManager()
    hm.MouseAllButtonsDown = OnMouseAllButtonsDownEvent
    hm.KeyDown = OnKeyDownEvent
    hm.HookMouse()
    hm.HookKeyboard()
    pythoncom.PumpMessages()
    hm.UnhookMouse()
    hm.UnhookKeyboard()


def OnMouseAllButtonsDownEvent(event):
    write2file(str(event.Position) + '\n')
    print('Position:',event.Position)
    ret_value = False
    return ret_value


def OnKeyDownEvent(event):
    write2file(chr(event.Ascii))
    if event.Ascii == 13: # if it's CR
        write2file('\n')
    print('Ascii:', event.Ascii, chr(event.Ascii))
    # End code if Esc pressed
    ret_value = False
    if event.Ascii == 27:
        ctypes.windll.user32.PostQuitMessage(0)
    return ret_value


def write2file(data):
    with open('record_coordinate.txt', 'a+') as f:
        f.write(data)


if __name__ == '__main__':
    main()

