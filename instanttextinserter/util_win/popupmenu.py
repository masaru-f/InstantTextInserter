# encoding: shift-jis

import win32api
import win32con
import win32gui

import util.stack as stack

import util_win.windowutil as windowutil

"""
[使い方]
1. Creator でメニューを構築する.
1. 自ウィンドウを作って, ウィンドウハンドルを取得しておく.
2. 構築した MenuData とウィンドウハンドルを Tracker に渡す.

"""

class MenuData:
    """
    MenuTracker に渡すデータ構造.
    @param menuhandle 作成したメニューのハンドル
    @param contents i 番目に"MenuID i+1 に対応した中身"が入ったリスト
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
    メニューを表示する.
    ウィンドウハンドルが必要.
    """
    def __init__(self, hwnd):
        self._hwnd = hwnd

    def track(self, menudata, posx=0, posy=0):
        """
        @exception MenuTrackError Trackingをキャンセルしたor失敗した
        """
        menuhandle = menudata.get_menuhandle()
        contents = menudata.get_contents()

        # 自ウィンドウをアクティブにする.
        # これをしないとメニューを表示できなかったり,
        # 表示したメニューを閉じれなかったりするため.
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
    Creator用.
    メニューのアペンド先を表す.
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
    Creator用.
    メニューのアペンド先を管理する.
    """
    def __init__(self):
        self.targets = stack.Stack()

    def push(self, target, name):
        self.targets.push(Target(target, name))

    def pop(self):
        """
        @exception IndexError スタックが空
        """
        return self.targets.pop()

    def is_empty(self):
        return self.targets.is_empty()

class Creator:
    """
    メニューを作成する.
    不要になったら destroy で破棄しなければならない.

    メニュー:   完成された一つのユニット.
    ユニット:   一つのメニューの実体. ユニットとアイテムから成る.
    アイテム:   メニュー上の一項目を表す.
    ハンドル:   ユニットの識別子.
    ターゲット: アイテムのアペンド先ユニット.
    ブレーク:   アイテムの表示位置を一列ずらすこと.

    1アイテムは content と id を持つ.
    ある id から, その id に対応した content を一意に取り出せる.

    @todo サブメニューをブレークできるようにする.
          サブメニュー作成タイミングが end 時だから今はムリ.
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
            # DestroyMenu は親を渡せば再帰的に解放してくれるが,
            # 親子関係が構築されている保証はないので,
            # 念のため全部解放してまわる.
            # 既に解放されているとエラーになるため無視する.
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
        # 親ユニットのハンドルを取ってくる
        target = None
        try:
            target = self._targetstack.pop()
        except IndexError:
            return

        # 現ユニット → 親ユニット に連結
        option = win32con.MF_POPUP
        option |= self._get_option()
        win32gui.AppendMenu(target.get_target(), \
                            option,\
                            self._curtarget, \
                            target.get_name())

        # 親ユニットをターゲットにする
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
        @exception ValueError メニューが上手く作れていない
        """
        # メニューが上手く作れてなければエラー
        if not(self._targetstack.is_empty()):
            self.destroy()
            raise ValueError("the structure of the menu is invalid.")

        return MenuData(
            self._curtarget,
            self._contents
        )

    def _create_unit(self, name):
        if self._curtarget:
            # 現ターゲットは直後に作る新・現ターゲットの親になる.
            # push する名前は新・現ターゲットの名前.
            # (実際に新・現ターゲットを作るのは pop 時だから.)
            # @todo 現と新・現が混在してるのでもっとわかりやすく
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
    簡単なテスト.
    適当に作ったメニューが表示できることと
    プログラムを終了できることを確認.
    """
    import trayicongui

    def on_rightclick():
        creator = Creator()
        creator.append("item1", "this is item1!")
        creator.append("item2", "this is あいてむ2")
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
