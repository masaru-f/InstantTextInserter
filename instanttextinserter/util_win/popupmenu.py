# encoding: shift-jis

import win32api
import win32con
import win32gui

import util.stack as stack

import util_win.windowutil as windowutil

"""
[�g����]
1. Creator �Ń��j���[���\�z����.
1. ���E�B���h�E�������, �E�B���h�E�n���h�����擾���Ă���.
2. �\�z���� MenuData �ƃE�B���h�E�n���h���� Tracker �ɓn��.

"""

class MenuData:
    """
    MenuTracker �ɓn���f�[�^�\��.
    @param menuhandle �쐬�������j���[�̃n���h��
    @param contents i �Ԗڂ�"MenuID i+1 �ɑΉ��������g"�����������X�g
    """
    def __init__(self, menuhandle ,contents):
        self._menuhandle = menuhandle
        self._contents = contents

    def get_menuhandle(self):
        return self._menuhandle

    def get_contents(self):
        return self._contents

class MenuTrackError(Exception):
    def __init__(self, msg):
        self._msg = msg
        return
    def __str__(self):
        return self._msg

class Tracker:
    """
    ���j���[��\������.
    �E�B���h�E�n���h�����K�v.
    """
    def __init__(self, hwnd):
        self._hwnd = hwnd

    def track(self, menudata, posx=0, posy=0):
        """
        @exception MenuTrackError Tracking���L�����Z������or���s����
        """
        menuhandle = menudata.get_menuhandle()
        contents = menudata.get_contents()

        # ���E�B���h�E���A�N�e�B�u�ɂ���.
        # ��������Ȃ��ƃ��j���[��\���ł��Ȃ�������,
        # �\���������j���[�����Ȃ������肷�邽��.
        windowutil.ActivateWindow(self._hwnd)

        selected_id = win32gui.TrackPopupMenu(\
                                menuhandle,\
                                win32con.TPM_RETURNCMD, \
                                posx, \
                                posy, \
                                0, \
                                self._hwnd, \
                                None \
        )

        if selected_id==0:
            raise MenuTrackError(
                "Tracking was canceled or failed. " +
                "hwnd:" + str(self._hwnd) + " " +
                "GetLastError:" + str(win32api.GetLastError())
            )
        return contents[selected_id-1]

class Target:
    """
    Creator�p.
    ���j���[�̃A�y���h���\��.
    """
    def __init__(self, target, name):
        self.target = target
        self.name = name

    def get_target(self):
        return self.target

    def get_name(self):
        return self.name

class TargetStack:
    """
    Creator�p.
    ���j���[�̃A�y���h����Ǘ�����.
    """
    def __init__(self):
        self.targets = stack.Stack()

    def push(self, target, name):
        self.targets.push(Target(target, name))

    def pop(self):
        """
        @exception IndexError �X�^�b�N����
        """
        return self.targets.pop()

    def is_empty(self):
        return self.targets.is_empty()

class Creator:
    """
    ���j���[���쐬����.
    �s�v�ɂȂ����� destroy �Ŕj�����Ȃ���΂Ȃ�Ȃ�.

    ���j���[:   �������ꂽ��̃��j�b�g.
    ���j�b�g:   ��̃��j���[�̎���. ���j�b�g�ƃA�C�e�����琬��.
    �A�C�e��:   ���j���[��̈ꍀ�ڂ�\��.
    �n���h��:   ���j�b�g�̎��ʎq.
    �^�[�Q�b�g: �A�C�e���̃A�y���h�惆�j�b�g.
    �u���[�N:   �A�C�e���̕\���ʒu����񂸂炷����.

    1�A�C�e���� content �� id ������.
    ���� id ����, ���� id �ɑΉ����� content ����ӂɎ��o����.

    @todo �T�u���j���[���u���[�N�ł���悤�ɂ���.
          �T�u���j���[�쐬�^�C�~���O�� end �������獡�̓���.
    """
    def __init__(self):
        self._handlelist = []
        self._targetstack = TargetStack()
        self._curtarget = None

        self._id = 1
        self._contents = []

        self._is_next_break = False
        self._is_next_grayout = False

        self._create_unit("rootmenu")

    def destroy(self):
        for i in range(len(self._handlelist)):
            # DestroyMenu �͐e��n���΍ċA�I�ɉ�����Ă���邪,
            # �e�q�֌W���\�z����Ă���ۏ؂͂Ȃ��̂�,
            # �O�̂��ߑS��������Ă܂��.
            # ���ɉ������Ă���ƃG���[�ɂȂ邽�ߖ�������.
            try:
                win32gui.DestroyMenu(self._handlelist[i])
            except:
                pass
        self._handlelist = []

    def append(self, name, content):
        option = win32con.MF_STRING
        option |= self._get_option()

        win32gui.AppendMenu(self._curtarget, \
                            option,\
                            self._id, \
                            name)
        self._add_content(content)

    def submenu_begin(self, name):
        self._create_unit(name)

    def submenu_end(self):
        # �e���j�b�g�̃n���h��������Ă���
        target = None
        try:
            target = self._targetstack.pop()
        except IndexError:
            return

        # �����j�b�g �� �e���j�b�g �ɘA��
        option = win32con.MF_POPUP
        option |= self._get_option()
        win32gui.AppendMenu(target.get_target(), \
                            option,\
                            self._curtarget, \
                            target.get_name())

        # �e���j�b�g���^�[�Q�b�g�ɂ���
        self._curtarget = target.get_target()

    def append_separator(self):
        win32gui.AppendMenu(self._curtarget, \
                            win32con.MF_SEPARATOR | self._get_option(),\
                            0, \
                            "")

    def break_next(self):
        self._is_next_break = True

    def grayout_next(self):
        self._is_next_grayout = True

    def get_menudata(self):
        """
        @exception ValueError ���j���[����肭���Ă��Ȃ�
        """
        # ���j���[����肭���ĂȂ���΃G���[
        if not(self._targetstack.is_empty()):
            self.destroy()
            raise ValueError("the structure of the menu is invalid.")

        return MenuData(
            self._curtarget,
            self._contents
        )

    def _create_unit(self, name):
        if self._curtarget:
            # ���^�[�Q�b�g�͒���ɍ��V�E���^�[�Q�b�g�̐e�ɂȂ�.
            # push ���閼�O�͐V�E���^�[�Q�b�g�̖��O.
            # (���ۂɐV�E���^�[�Q�b�g�����̂� pop ��������.)
            # @todo ���ƐV�E�������݂��Ă�̂ł����Ƃ킩��₷��
            self._targetstack.push(self._curtarget, name)

        self._curtarget = win32gui.CreatePopupMenu()
        self._handlelist.append(self._curtarget)

    def _add_content(self, content):
        self._contents.append(content)
        self._id += 1

    def _get_option(self):
        option = 0
        if self._is_next_break:
            option |= win32con.MF_MENUBREAK
            self._is_next_break = False
        if self._is_next_grayout:
            option |= win32con.MF_GRAYED
            self._is_next_grayout = False
        return option

if __name__ == '__main__':
    """
    �ȒP�ȃe�X�g.
    �K���ɍ�������j���[���\���ł��邱�Ƃ�
    �v���O�������I���ł��邱�Ƃ��m�F.
    """
    import trayicongui

    def on_rightclick():
        creator = Creator()
        creator.append("item1", "this is item1!")
        creator.append("item2", "this is �����Ă�2")
        creator.append_separator()
        creator.grayout_next()
        creator.append("grayout item", "grayout!")

        tracker = Tracker(trayicongui.hwndinst.get())
        content = ""
        try:
            content = tracker.track(creator.get_menudata(), 0, 0)
            print "content:" + str(content)
        except MenuTrackError as e:
            print str(e)

        creator.destroy()

    with trayicongui.MainWindow(classname="hogewndclass") as mainwindow:

        def on_leftclick():
            mainwindow.stop()

        mainwindow.set_callback_on_left_click(on_leftclick)
        mainwindow.set_callback_on_right_click(on_rightclick)
        mainwindow.create_and_start()
