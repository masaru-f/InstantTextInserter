# encoding: shift-jis

import time

import win32api
import win32con

from keycode import *

class KeyGetter:
    def __init__(self):
        self._clear_flags()
        return

    def is_pushed(self, keycode):
        return self._getkey(keycode)

    def is_pushed_once(self, keycode):
        state = self._getkey(keycode)
        # 押されている
        if state:
            if self.pushingflags[keycode]==False:
                # 初めて押された
                self.pushingflags[keycode] = True
                return True
            # 押しっぱなし中
            return False
        # 押されていない.
        # 押しっぱなしフラグが立っているなら降ろす.
        if self.pushingflags[keycode]:
            self.pushingflags[keycode] = False
        return False

    def _clear_flags(self):
        self.pushingflags = []
        for i in range(VK_MAX):
            self.pushingflags.append(False)
        return

    def _getkey(self, keycode):
        state = win32api.GetAsyncKeyState(keycode)
        if state==0 or state==1:
            return False
        return True

class MushingGetter:
    def __init__(self):
        self.keygetter = KeyGetter()
        self._init_parameters()
        pass

    def is_pushed(self, keycode, mushingcount, interval_msec):
        """
        連打されたかどうかを返す.
        インターバル以内に指定回数押されたら連打とみなす.
        ゲームループ中から呼び出すことを想定.
        """
        if self.keygetter.is_pushed_once(keycode):
            # 押下された.
            self.curmushedcount += 1
            if self.curmushedcount==1:
                # 初回押下. カウントスタート
                self.curtime = time.clock()
                return False
            else:
                if self._is_passed_interval(interval_msec):
                    # 初回押下後時間切れ.
                    self._init_parameters()
                    return False
                if self.curmushedcount >= mushingcount:
                    # 指定回数に達した, つまり連打が押された.
                    self._init_parameters()
                    return True
                #初回押下後, 時間切れでない.
                return False
        else:
            # 押下されていない.
            if self.curmushedcount==0:
                # スタートしていない.
                return False
            elif self._is_passed_interval(interval_msec):
                # スタートしているが, 時間切れ.
                self._init_parameters()
            # スタートしているが, 時間切れでない.
            return False

    def _is_passed_interval(self, interval_msec):
        diff = interval_msec - (time.clock() - self.curtime)*1000
        if diff>0:
            return False
        return True

    def _init_parameters(self):
        self.curtime = 0
        self.curmushedcount = 0

if __name__ == '__main__':
    key = KeyGetter()
    mushing = MushingGetter()
    while True:
        '''
        if key.is_pushed(CH_A):
            print "a is pushing."
        elif key.is_pushed_once(CH_B):
            print "b is pushing once."
        elif key.is_pushed(CH_C):
            print "end."
            break
        '''
        if mushing.is_pushed(A, 2, 500):
            print "mushed!"
        if key.is_pushed(C):
            print "end."
            break
        time.sleep(0.05)
