INVALID_CHAR = "?"
def keycode2chara(keycode):
    c = INVALID_CHAR
    i = keycode

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

    return c

class FileWriter:
    def __init__(self):
        return

    def write(self, filename, content):
        """
        ���s�͎����I�ɕt������.
        @param content �������ޓ��e�̃V�[�P���X
        """
        _content = content[:]

        for i in range(len(_content)):
            # os.linesep ���Ɖ��s����}�������.
            # windows ����A�v���Ȃ̂� \n �ł�����.
            #_content[i] += os.linesep
            _content[i] += "\n"

        fileobj = open(filename, "w")
        ret = fileobj.writelines(_content)
        fileobj.close()

# --------------------------------

def print_keycode2chara_list():
    """
    SnippetManager �Ɏ������郊�X�g�����.
    ����ŏo�͂�����������ہX�R�s�y����.
    """
    s = ""
    for i in range(256):
        c = keycode2chara(i)
        s = s + "'" + c + "',"
    print s

def print_supported_keycode_list():
    """
    SnippetManager �Ɏ������郊�X�g�����.
    ����ŏo�͂�����������ہX�R�s�y����.
    """
    s = ""
    for i in range(256):
        c = keycode2chara(i)
        if c==INVALID_CHAR:
            continue
        s = s + str(i) + ","
    print s

def create_file4test():
    """
    ���͂������������͂���X�j�y�b�g�t�@�C���𐶐�.
    ������g���Ċe�����̓��͂��s���邩���蓮�Ŋm���߂�.
    """
    ls = []
    for i in range(256):
        c = keycode2chara(i)
        if c==INVALID_CHAR:
            continue
        c = c.replace("\\t", "\t").replace("\\\\", "\\")
        ls.append("===" + c + "===")
        ls.append(c+c)

    writer = FileWriter()
    writer.write("charatest.txt", ls)

print_keycode2chara_list()
print_supported_keycode_list()
create_file4test()