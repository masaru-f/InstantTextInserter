
"""
SnippetManager �� keycode2chara �����R�[�h.
�W���o�͂ɏo�Ă������̂��ہX�R�s�y���邾��.

"""

s = ""

INVALID_CHAR = "?"
for i in range(256):
    if i>=65 and i<=90:
        c = chr(i)
    elif i>=48 and i<=57:
        c = str(i-48)
    elif i>=96 and i<=105:
        c = str(i-96)
    elif i==9:
        c = "\\t"
    elif i==32:
        c = " "
    elif i==186: # chr ���Ă��Ή����镶�����o�Ă��Ȃ��̂Ŏd���Ȃ���...
        c = ":"
    elif i==187:
        c = ";"
    elif i==188:
        c = ","
    elif i==189:
        c = "-"
    elif i==190:
        c = "."
    elif i==191:
        c = "/"
    elif i==192:
        c = "@"
    elif i==219:
        c = "["
    elif i==220:
        c = "\\\\"
    elif i==221:
        c = "]"
    elif i==222:
        c = "^"
    elif i==226:
        c = "\\\\"
    else:
        c = INVALID_CHAR

    s = s + "'" + c + "',"

print s
