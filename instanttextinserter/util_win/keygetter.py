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
        # ������Ă���
        if state:
            if self.pushingflags[keycode]==False:
                # ���߂ĉ����ꂽ
                self.pushingflags[keycode] = True
                return True
            # �������ςȂ���
            return False
        # ������Ă��Ȃ�.
        # �������ςȂ��t���O�������Ă���Ȃ�~�낷.
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
        �A�ł��ꂽ���ǂ�����Ԃ�.
        �C���^�[�o���ȓ��Ɏw��񐔉����ꂽ��A�łƂ݂Ȃ�.
        �Q�[�����[�v������Ăяo�����Ƃ�z��.
        """
        if self.keygetter.is_pushed_once(keycode):
            # �������ꂽ.
            self.curmushedcount += 1
            if self.curmushedcount==1:
                # ���񉟉�. �J�E���g�X�^�[�g
                self.curtime = time.clock()
                return False
            else:
                if self._is_passed_interval(interval_msec):
                    # ���񉟉��㎞�Ԑ؂�.
                    self._init_parameters()
                    return False
                if self.curmushedcount >= mushingcount:
                    # �w��񐔂ɒB����, �܂�A�ł������ꂽ.
                    self._init_parameters()
                    return True
                #���񉟉���, ���Ԑ؂�łȂ�.
                return False
        else:
            # ��������Ă��Ȃ�.
            if self.curmushedcount==0:
                # �X�^�[�g���Ă��Ȃ�.
                return False
            elif self._is_passed_interval(interval_msec):
                # �X�^�[�g���Ă��邪, ���Ԑ؂�.
                self._init_parameters()
            # �X�^�[�g���Ă��邪, ���Ԑ؂�łȂ�.
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
