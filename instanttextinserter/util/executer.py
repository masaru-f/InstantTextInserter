# encoding: shift-jis

import subprocess
import os

class Executer:
    def __init__(self):
        return

    def execute(self, command):
        """
        �w�肵���v���O�������N������.
        �m���u���b�L���O.

        �ȉ��� Windows �ł̘b.
        - ���������I�[�v���̏ꍇ�� PATH �̒ʂ����t�@�C���ł�OK.
        - �����L��I�[�v���̏ꍇ�͖����I�ȃp�X�w�肪�K�v.

        @param command ���s�t�@�C���p�X[, ����] �̃��X�g
        @retval True   �N���ɐ���
        @retval False  �N���Ɏ��s
        """
        if len(command)==0:
            return False

        if len(command)==1:
            # windows ���Ƌ�̃R�}���h���C����^�����,
            # �Ȃ��� MyDocument? ���J����ĈӖ��s���Ȃ̂ŃG���[�ɂ��Ƃ�.
            if len(command[0])==0:
                return False

            try:
                os.startfile(command[0])
                return True
            except:
                return False

        if len(command)==2:
            try:
                subprocess.Popen(command)
                return True
            except:
                return False

        return False

if __name__ == '__main__':
    """
    PyScripter ������s�����, �ȑO�����グ�Ă����t�@�C����
    �ēx���s���ɕ����Ă��܂����ۂ��N���邱�Ƃɒ���.
    """
    executer = Executer()

    #ok �t�@�C��
    executer.execute(["c:\\windows\\notepad.exe"])

    #ok �p�X�̒ʂ����t�@�C��
    executer.execute(["iexplore.exe"])

    #ok �t�H���_
    executer.execute(["c:\\program files"])

    #ok �֘A�t�����ĂȂ��t�@�C��
    executer.execute(["C:\Windows\System32\drivers\etc\hosts"])

    #ok �v���O�����Ɉ�����^����
    executer.execute([
        "c:\\windows\\notepad.exe",
        "hoge.txt"
    ])

    #NG �p�X�̒ʂ����v���O�����Ɉ�����^����
    ret = executer.execute([
        "iexplore.exe",
        "http://www.google.com/"
    ])
    if ret:
        raise Exception("should be come here.")

    '''
    # �ȉ����J���邪����J���Ƃ������̂ł�������R�����g�A�E�g.
    print executer.execute(["python"])
    print executer.execute(
        ["C:\\Program Files (x86)\\Hidemaru\\Hidemaru.exe",
        "C:\\Program Files\\nodejs\\node_etw_provider.man"]
    )
    '''
