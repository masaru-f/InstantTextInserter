# encoding: shift-jis

import time
import os

import util_win.keygetter as keygetter

"""
�L�[���o�̎蓮�e�X�g.
�L�[�������ƕW���o�͂ɉ��������ꂽ�����o��.

�L�[�R�[�h�ɑΉ�����L�[�������߂邽�߂�
keycode.py �𒼐ړǂ�Ŏ����𐶐����Ă���.

@note WIN = LWIN <- ���������ꍇ(�E�ӂ������ȊO)�Ɍ��o�ł��Ȃ�.
      �����͎����������[�`��.
"""

filename = os.path.join(os.path.pardir, "keycode.py")
fileobj = open(filename, "r")
contents = fileobj.readlines()
fileobj.close()

dic = {}
for line in contents:
    line = line[:len(line)-1]
    if line=="":
        continue
    ls = line.split(" # ")
    ls = ls[0] # remove part of comments
    ls = ls.split(" = ")
    if len(ls)<=1:
        continue
    name, code = ls[0], ls[1]
    dic[code] = name

key = keygetter.KeyGetter()
canbreak = False
while True:
    for i in range(keygetter.VK_MAX):
        if key.is_pushed_once(i):
            name = "unknown"
            try:
                name = dic[str(i)]
            except KeyError:
                pass
            print "pushed " + name
            if i==keygetter.ESC:
                print "BREAKED!"
                canbreak = True
    if canbreak:
        break
    time.sleep(0.05)
