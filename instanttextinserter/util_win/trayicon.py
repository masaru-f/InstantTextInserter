# encoding: shift-jis

import win32api
import win32gui
import win32con
import pywintypes

class TrayIcon:
    def __init__(self, hwnd, callback_message, hovertext):
        """
        @param hwnd ���L�҃E�B���h�E�̃n���h��
        @param callback_message �C�x���g�������ɏ��L�҂ɓ����郁�b�Z�[�W
        """
        self.hwnd = hwnd
        self.callback_message = callback_message
        self.hovertext = hovertext

        self.hicon = None

        self._create()

    def _create(self):
        # param1 �� NULL(0) ���w�肷���
        # ���݂̃v���Z�X���쐬���邽�߂Ɏg��ꂽ�t�@�C���̃p�X���擾.
        self_filename = win32api.GetModuleFileName(0)

        self.hicon = win32gui.ExtractIconEx(self_filename, 0, 1)[0][0]

        # param2 �͈����A�C�R���̎��ʎq.
        # �����A�C�R���� 1 �Ȃ̂œK���ɂ���.
        notifyicondata = (
            self.hwnd,
            0,
            win32gui.NIF_MESSAGE | win32gui.NIF_ICON | win32gui.NIF_TIP,
            self.callback_message,
            self.hicon,
            self.hovertext
        )
        win32gui.Shell_NotifyIcon(
            win32gui.NIM_ADD,
            notifyicondata
        )

    def destroy(self):
        notifyicondata = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, notifyicondata)

        win32gui.DestroyIcon(self.hicon)
