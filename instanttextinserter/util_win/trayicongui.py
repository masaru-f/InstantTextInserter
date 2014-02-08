# encoding: shift-jis

#import ctypes # for hotkey prototype
import win32gui
import win32con
import win32api

# log�g�p�����̍폜(util��log���g�������Ȃ�)
import util.log as log

import util_win.trayicon as trayicon

"""
[�g����]
- MainWindow �N���X���g���� GUI ���\�z����.
- �E�B���h�E�n���h�����~�����ꍇ�� Hwnd �V���O���g���N���X���g��.
"""

class MainLoop:
    """
    GUI ���[�v�̊J�n�ƒ�~���s��.
    MainWindow ����Ăяo�����Ƃ�z��.
    """
    def __init__(self):
        self._can_running = True

    def start(self):
        log.info("mainloop start...")
        while self._can_running:
            b, msg = win32gui.GetMessage(0, 0, 0)
            if not(msg):
                break
            win32gui.TranslateMessage(msg)
            win32gui.DispatchMessage(msg)
        log.info("mainloop stop.")

    def stop(self, hwnd):
        """
        @param hwnd �I�����b�Z�[�W�̑��M��E�B���h�E�n���h��
        """
        self._can_running = False

        # PostQuitMessage ���Ƒ��X���b�h����̎��s���ɏI���ł��Ȃ�.
        # ���̂���, ������ hwnd �𖾎��I�Ɏw��ł��� PostMessage ���g�p.
        #win32api.PostQuitMessage(0)
        win32api.PostMessage(
            hwnd,
            win32con.WM_QUIT
        )

def _incrementer():
    """
    MainWindow �p�̃C���N�������g�J�E���^.
    �{���̓J�v�Z����������������, �C���N�������g�J�E���^��
    �O���[�o���X�R�[�v�ɒu���Ȃ��Ɠ����Ȃ����ߎd���Ȃ������ɔz�u.
    """
    _incrementer.count += 1
    return _incrementer.count
_incrementer.count = 0

class Hwnd:
    """
    �E�B���h�E�n���h�����i�[�����V���O���g���N���X.
    ���p�҂͂�����g���ăE�B���h�E�n���h�����擾����.

    set ����̂� MainWindow �̂�.
    setter ��������Ⴄ�Ɨ��p�ґ����猩�����Ⴄ����,
    set ����ۂ͒��ڃ����o�ϐ���������悤�ɂ���.
    """
    def __init__(self):
        self._hwnd = None

    def get(self):
        return self._hwnd
# �V���O���g���C���X�^���X
hwndinst = Hwnd()

class MainWindow:
    """
    ��\���E�B���h�E + �g���C�A�C�R�����쐬����.
    @note �I������ destroy ���Ăт����Ȃ���΂Ȃ�Ȃ�.
    """

    # ���[�U��`���b�Z�[�W.
    # WM_APP ���� 1 �����₵�Ē�`.
    WM_BASE = win32con.WM_APP
    WM_TRAYICON_EVENT = WM_BASE + _incrementer()

    def __init__(self, classname="window", tooltip=""):
        """
        @param classname �E�B���h�E�N���X��
        """
        self._can_destroy = True

        self._hwnd = None
        self._classname = classname
        self._classatom = None
        self._hinst = None

        self._trayicon = None
        self._tooltip = tooltip

        self._mainloop = MainLoop()

        self._callback_on_destroy = None
        self._callback_on_hotkey = None
        self._callback_on_left_click = None
        self._callback_on_right_click = None
        self._callback_on_middle_click = None

        self._message_map = {
            win32con.WM_DESTROY          : self._on_destroy,
            MainWindow.WM_TRAYICON_EVENT : self._on_tray,
            win32con.WM_HOTKEY           : self._on_hotkey,
        }

    def __enter__(self):
        return self

    def __exit__(self, type, value, trackback):
        self.destroy()

    def set_callback_on_destroy(self, callback):
        """
        �E�B���h�E�j�����Ɏ��s����R�[���o�b�N�֐���o�^����.
        """
        self._callback_on_destroy = callback

    def set_callback_on_hotkey(self, callback):
        self._callback_on_hotkey = callback

    def set_callback_on_left_click(self, callback):
        self._callback_on_left_click = callback

    def set_callback_on_right_click(self, callback):
        self._callback_on_right_click = callback

    def set_callback_on_middle_click(self, callback):
        self._callback_on_middle_click = callback

    def create(self):
        """
        �E�B���h�E���쐬����.
        """
        if self._hwnd:
            return self._hwnd

        log.debug("before registering window class...")
        wc = win32gui.WNDCLASS()
        self._hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = self._classname
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = self._message_map
        self._classatom = win32gui.RegisterClass(wc)
        log.debug("after registering window class.")

        log.debug("before creating window...")
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        windowpos = (0, 0)
        windowsize = (1, 1)
        self._hwnd = win32gui.CreateWindow(
            self._classatom,
            self._classname,
            style,
            windowpos[0],
            windowpos[1],
            windowsize[0],
            windowsize[1],
            0,
            0,
            self._hinst,
            None,
        )
        hwndinst._hwnd = self._hwnd # ���p�ҎQ�Ɛ�ɂ������.
        log.debug("after creating window.")

        log.debug("before updating window...")
        win32gui.UpdateWindow(self._hwnd)
        log.debug("after updating window.")

        log.debug("before showing window...")
        win32gui.ShowWindow(self._hwnd, win32con.SW_HIDE)
        log.debug("after showing window.")

        self._trayicon = trayicon.TrayIcon(
            self._hwnd,
            MainWindow.WM_TRAYICON_EVENT,
            self._tooltip
        )

    def start(self):
        """
        GUI���[�v�ɓ���.
        create() �ƕ����Ă���̂�, create() ���
        �Ăяo�����ŃE�B���h�E�n���h�����~�����P�[�X�ɑΉ����邽��.
        """
        if not(self._hwnd):
            log.debug("cannot start. main window is not created.")
            return

        self._mainloop.start() # blocking.

    def stop(self):
        """
        GUI ���[�v���甲����.
        @note �E�B���h�E���쐬�����X���b�h�ƕʂ̃X���b�h����Ăяo���Ă��悢.
        """
        log.debug("mainwindow stop!")
        self._mainloop.stop(self._hwnd)

    def destroy(self):
        """
        GUI�̔j����, �j�����R�[���o�b�N�̎��s.
        @note �E�B���h�E���쐬�����X���b�h�Ɠ����X���b�h����Ăяo������.
        """
        if not(self._can_destroy):
            return
        self._can_destroy = False

        self.stop()

        if callable(self._callback_on_destroy):
            self._callback_on_destroy()

        try:
            self._trayicon.destroy()
            log.info("destroyed trayicon.")
        except Exception as e:
            log.error(
                "destroying trayicon failed." +
                str(type(e)) + "/" + str(e)
            )

        try:
            win32gui.DestroyWindow(self._hwnd)
            log.info("destroyed window.")
        except Exception as e:
            log.error(
                "destroying window failed." +
                str(type(e)) + "/" + str(e)
            )

        try:
            win32gui.UnregisterClass(self._classatom, self._hinst)
            log.info("unregistered class.")
        except Exception as e:
            log.error(
                "unregistered class failed." +
                str(type(e)) + "/" + str(e)
            )

    def _on_hotkey(self, hwnd, message, wparam, lparam):
        if callable(self._callback_on_hotkey):
            # @todo ������K���ɊԈ���. index, modifier, keycode ���炢.
            print "from trayicongui, " + str(self)
            self._callback_on_hotkey(hwnd, message, wparam, lparam)

    def _on_destroy(self, hwnd, message, wparam, lparam):
        self.destroy()

    def _on_tray(self, hwnd, message, wparam, lparam):
        """
        [memo]
        wparam: �}�E�X�C�x���g�����������^�X�N�o�[�A�C�R����ID.
        lparam: ���������C�x���g�Ɋ֘A���郁�b�Z�[�W�R�[�h.
        """
        if lparam==win32con.WM_RBUTTONUP:
            log.debug("right clicked.")
            if callable(self._callback_on_right_click):
                self._callback_on_right_click()
        elif lparam==win32con.WM_LBUTTONUP:
            log.debug("left clicked.")
            if callable(self._callback_on_left_click):
                self._callback_on_left_click()
        elif lparam==win32con.WM_MBUTTONUP:
            log.debug("middle clicked.")
            if callable(self._callback_on_middle_click):
                self._callback_on_middle_click()


if __name__ == '__main__':
    """
    �ȒP�ȓ���m�F.
    �E�B���h�E������� 3 �b��ɏI������.
    """
    import threading
    import time

    def stopthreadbody(mainwindowinst):
        time.sleep(3)
        mainwindowinst.stop()
        #mainwindowinst.destroy()

    with MainWindow(classname="hogewndclass") as mainwindow:
        stopthread = threading.Thread(
            None,
            stopthreadbody,
            "thread name",
            (mainwindow,),
            {},
        )
        stopthread.start()

        mainwindow.create()
        mainwindow.stop()

        stopthread.join()

