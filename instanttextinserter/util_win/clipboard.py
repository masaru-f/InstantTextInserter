# encoding: shift-jis

import ctypes
import win32clipboard
import win32con

class Clipboard:
    """
    扱えるのは CF_TEXT のみ.
    非スレッドセーフなのでマルチスレッドで使わないこと.
    static での実装はとりあえずで, 問題あるなら変える予定.
    """
    @staticmethod
    def get():
        """
        クリップボードの中身を返す.
        @retval 空文字列 取得に失敗 or 何も入ってない
        """
        if not(Clipboard._open()):
            return ""

        if not(Clipboard._is_available()):
            return ""

        ret = win32clipboard.GetClipboardData(win32con.CF_TEXT)
        Clipboard._close()
        return ret

    @staticmethod
    def set(s):
        """
        指定した文字列をクリップボードに格納する.
        クリップボードへのコピーはグローバルヒープを使う必要がある.
        """
        if not(isinstance(s, str)):
            return False

        # グローバルヒープ領域を確保
        hMem = ctypes.windll.kernel32.GlobalAlloc(
            win32con.GMEM_MOVEABLE,
            len(s)+1
        )
        if hMem==0:
            return False
        # 確保した領域をロック.
        pMemBlock = ctypes.windll.kernel32.GlobalLock(hMem)
        if pMemBlock==0:
            return False
        # 確保した領域にコピーするデータを書き込む.
        pBuffer = ctypes.windll.kernel32.lstrcpy(
            ctypes.c_char_p(pMemBlock),
            s
        )
        if pBuffer==0:
            ctypes.windll.kernel32.GlobalUnlock(hMem)
            return False
        ctypes.windll.kernel32.GlobalUnlock(hMem)

        # クリップボードを開く.
        if not(Clipboard._open()):
            return False
        # クリップボードに残っているデータを消す.
        # これをしないと上手くコピーされないことがある.
        win32clipboard.EmptyClipboard()

        # 確保した領域に書き込んだ内容をクリップボードに書き込む.
        ret = True
        try:
            win32clipboard.SetClipboardData(win32con.CF_TEXT, hMem)
        except:
            ret = False

        Clipboard._close()
        return ret

    @staticmethod
    def _open():
        """
        クリップボードを既に開いているかどうかを返す.
        開いてなければ開く.
        開かれていれば, 新たに開いちゃったのは閉じる.
        """
        ret = win32clipboard.OpenClipboard()
        if(ret==None):
            return True
        Clipboard._close()
        return False

    @staticmethod
    def _close():
        # 開いてない時に実行するとしくじるので吸収.
        try:
            win32clipboard.CloseClipboard()
        except:
            pass
        return

    @staticmethod
    def _is_available():
        ret = win32clipboard.IsClipboardFormatAvailable(win32con.CF_TEXT)
        if(ret!=0):
            return True
        Clipboard._close()
        return False

if __name__ == '__main__':
    print Clipboard.set("hogeほげげー")
    print Clipboard.get()
    pass

