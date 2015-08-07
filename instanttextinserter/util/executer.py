# encoding: shift-jis

import subprocess
import os

class Executer:
    def __init__(self):
        return

    def execute(self, command):
        """
        指定したプログラムを起動する.
        ノンブロッキング.

        以下は Windows での話.
        - 引数無しオープンの場合は PATH の通ったファイルでもOK.
        - 引数有りオープンの場合は明示的なパス指定が必要.

        @param command 実行ファイルパス[, 引数] のリスト
        @retval True   起動に成功
        @retval False  起動に失敗
        """
        if len(command)==0:
            return False

        if len(command)==1:
            # windows だと空のコマンドラインを与えると,
            # なぜか MyDocument? が開かれて意味不明なのでエラーにしとく.
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
    PyScripter から実行すると, 以前立ち上げていたファイルが
    再度実行時に閉じられてしまう現象が起こることに注意.
    """
    executer = Executer()

    #ok ファイル
    executer.execute(["c:\\windows\\notepad.exe"])

    #ok パスの通ったファイル
    executer.execute(["iexplore.exe"])

    #ok フォルダ
    executer.execute(["c:\\program files"])

    #ok 関連付けられてないファイル
    executer.execute(["C:\Windows\System32\drivers\etc\hosts"])

    #ok プログラムに引数を与える
    executer.execute([
        "c:\\windows\\notepad.exe",
        "hoge.txt"
    ])

    #NG パスの通ったプログラムに引数を与える
    ret = executer.execute([
        "iexplore.exe",
        "http://www.google.com/"
    ])
    if ret:
        raise Exception("should be come here.")

    '''
    # 以下も開けるが毎回開くとうざいのでいったんコメントアウト.
    print executer.execute(["python"])
    print executer.execute(
        ["C:\\Program Files (x86)\\Hidemaru\\Hidemaru.exe",
        "C:\\Program Files\\nodejs\\node_etw_provider.man"]
    )
    '''
