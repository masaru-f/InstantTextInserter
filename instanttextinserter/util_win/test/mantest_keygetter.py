# encoding: shift-jis

import time
import os

import util_win.keygetter as keygetter

"""
キー検出の手動テスト.
キーを押すと標準出力に何が押されたかが出る.

キーコードに対応するキー名を求めるために
keycode.py を直接読んで辞書を生成している.

@note WIN = LWIN <- こういう場合(右辺が数字以外)に検出できない.
      原因は辞書生成ルーチン.
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
