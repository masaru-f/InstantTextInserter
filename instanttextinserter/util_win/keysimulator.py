# encoding: shift-jis

import win32api

import keycode

class KeySimulator:
    def __init__(self):
        pass

    def ctrl_v(self):
        self._keydown(keycode.CTRL)
        self._keydown(keycode.V)
        self._keyup(keycode.CTRL)
        self._keyup(keycode.V)

    def left(self):
        self._press(keycode.LEFT)

    def backspace(self):
        self._press(keycode.BACKSPACE)

    def _press(self, keycode):
        self._keydown(keycode)
        self._keyup(keycode)

    def _keydown(self, keycode):
        win32api.keybd_event(keycode, 0, 0)

    def _keyup(self, keycode):
        win32api.keybd_event(keycode, 0, 2)

if __name__ == '__main__':
    from time import sleep

    simulator = KeySimulator()
    sleep(3)

    simulator.ctrl_v()
    for i in range(5):
        simulator.left()
