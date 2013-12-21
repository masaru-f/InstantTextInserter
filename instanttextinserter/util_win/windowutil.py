# encoding: shift-jis

import ctypes
import win32api
import win32con
import win32file
import win32gui
import win32process

def GetForegroundWindow():
    """
    Windows API �ɑ����� GetForegroundWindow.
    """
    return ctypes.windll.user32.GetForegroundWindow()

def WindowFromPoint():
    """
    �}�E�X�J�[�\���ʒu�ɂ���E�B���h�E�̃n���h�����擾.
    �擾����̂͐e�E�B���h�E�ł��邱�Ƃɒ���.
    """
    mx, my = win32api.GetCursorPos()
    return ctypes.windll.user32.GetAncestor(
        win32gui.WindowFromPoint((mx, my)),
        win32con.GA_ROOT
    )

def ActivateWindow(hwnd):
    """
    �w��E�B���h�E���A�N�e�B�u�ɂ���.
    """
    foreground_threadid, processid = \
        win32process.GetWindowThreadProcessId(
            GetForegroundWindow()
        )
    current_threadid = win32api.GetCurrentThreadId()

    # foreground �ȃX���b�h�ɃA�^�b�`����
    if foreground_threadid != current_threadid:
        try:
            # @note ���܂� error:87 ���N����̂ŋz��.
            # @todo error:87 �̌�������
            win32process.AttachThreadInput(
                current_threadid,
                foreground_threadid,
                True
            )
        except:
            pass

    try:
        # �E�B���h�E�n���h�����������ƃG���[�ɂȂ�(code:1400)�̂�
        # �����ŋz��.
        win32gui.SetForegroundWindow(hwnd)
    except:
        pass

    # �A�^�b�`���Ă���΃f�^�b�`����..
    if foreground_threadid != current_threadid:
        try:
            win32process.AttachThreadInput(
                current_threadid,
                foreground_threadid,
                False
            )
        except:
            pass

def GetProcessImageFileName(hprocess, max_path):
    """
    64bit�A�v���ɑΉ�����, �v���Z�X�̃t�@�C���p�X�擾.
    �v���Z�X�̃C���[�W�����擾��,
    �C���[�W���Ɋ܂܂��f�o�C�X�����h���C�u���^�[�ɒu�����Ă���.
    """

    # device name > drive letter �ϊ��e�[�u���̍쐬
    # 1. drive letter list
    ldstrings = win32api.GetLogicalDriveStrings().split("\\0")[0]
    drivelist = [elm.strip("\\") for elm in ldstrings.split("\0")]
    drivelist.remove("")
    # 2. device name list
    devicelist = [
        win32file.QueryDosDevice(elm).split("\0\0")[0]
        for elm in drivelist
    ]
    # 3. convertion table
    device2driveletter = {}
    for i in range(len(drivelist)):
        device2driveletter[devicelist[i]] = drivelist[i]

    imagefilename = (ctypes.c_char*Windowproperty.MAX_PATH)()
    len_imagefilename = ctypes.windll.psapi.GetProcessImageFileNameA(
        hprocess,
        imagefilename,
        max_path
    )

    # �擾���s. �C���[�W������, �擾�����Ɏ��s����.
    if len_imagefilename==0:
        return ""

    # �C���[�W���ɑ΂��Ċe�f�o�C�X���� replace �����݂�.
    # replace �ł��� = �Ή�����h���C�u���^�[�ɒu�����ꂽ.
    beforestr = imagefilename.value
    for i in range(len(drivelist)):
        devicename = devicelist[i]
        afterstr = beforestr.replace(
            devicename,
            device2driveletter[devicename]
        )
        if beforestr!=afterstr:
            return afterstr

    # �擾���s. �Ή�����h���C�u���^�[��������Ȃ�����.
    return ""

class Windowproperty:
    """
    �w��E�B���h�E�̏������擾����.
    �擾���s�͋z������(��̒l��Ԃ��悤�ɂ���).
    ������ API �����X�z�����Ă����ꍇ�͋z�������͓���ĂȂ�.
    """

    # �l�͓K��. ���ꂭ�炢����΂܂������ł���, �Ƃ������x.
    MAX_PATH = 2048

    def __init__(self, hwnd):
        self.hwnd = hwnd
        return

    def get_caption(self):
        return win32gui.GetWindowText(self.hwnd)

    def get_classname(self):
        try:
            return win32gui.GetClassName(self.hwnd)
        except Exception as e:
            pass
        return ""

    def get_hwnd(self):
        return self.hwnd

    def get_path(self):
        threadid, processid = \
            win32process.GetWindowThreadProcessId(self.hwnd)
        processhandle = win32api.OpenProcess(\
            win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, \
            0, \
            processid
        )
        if processhandle==0:
            return ""

        ret = ""
        try:
            # @note �߂�l�� unicode string �ł��邱�Ƃɒ���
            ret = win32process.GetModuleFileNameEx(processhandle, 0)
        except:
            # 64bit�A�v�����Ɛ������Ȃ��̂�
            # GetProcessImageFileName ������.
            return GetProcessImageFileName(
                processhandle.__int__(),
                Windowproperty.MAX_PATH
            )

        processhandle.close()
        return ret

    def get_windowpos(self):
        try:
            left, top, right, bottom = win32gui.GetWindowRect(
                self.hwnd
            )
            return [left, top]
        except Exception as e:
            pass
        return [0, 0]

    def get_windowsize(self):
        try:
            left, top, right, bottom = win32gui.GetWindowRect(
                self.hwnd
            )
            return [right-left, bottom-top]
        except Exception as e:
            pass
        return [0, 0]

if __name__ == '__main__':
    from time import sleep

    ActivateWindow(0)

    sleep(2)
    print "=== frompoint ==="
    wp_frompoint = Windowproperty(WindowFromPoint())
    print wp_frompoint.get_caption()
    print wp_frompoint.get_classname()
    print wp_frompoint.get_hwnd()
    print wp_frompoint.get_path()
    print "=== foreground ==="
    wp = Windowproperty(GetForegroundWindow())
    print wp.get_caption()
    print wp.get_classname()
    print wp.get_hwnd()
    print wp.get_path()
    s = wp.get_path()
    print isinstance(s, str)
    print isinstance(s, unicode)