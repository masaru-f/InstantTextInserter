
"""
SnippetManager の keycode2chara を作るコード.
標準出力に出てきたものを丸々コピペするだけ.

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
    elif i==186: # chr しても対応する文字が出てこないので仕方なく列挙...
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
