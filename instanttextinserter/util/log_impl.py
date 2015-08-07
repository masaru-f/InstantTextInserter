# encoding: shift-jis

import datetimestring

"""
ログ利用方法)
log.py を同ディレクトリに作り, log_impl.py をインポート.
ログインスタンスを生成し, 適宜設定なども併せて記述.
ログ利用者は, log.py をインポートして利用する.
"""


def _incrementer():
    ret = _incrementer.count
    _incrementer.count += 1
    return ret
_incrementer.count = 0

class LEVEL:
    """
    重大なレベルを後に定義する(大きな値にする)こと.
    """
    lower_limit = _incrementer() # 下限値, 利用者は使わないこと.
    debug = _incrementer()
    info = _incrementer()
    warning = _incrementer()
    error = _incrementer()
    critical = _incrementer()
    upper_limit = _incrementer() # 上限値, 利用者は使わないこと.

    default = info
    minlevel = debug
    maxlevel = critical

class Log:
    def __init__(self):
        self._datetime = datetimestring.Datetime()
        self._levelstring_dict = {
            LEVEL.debug: "[D]",
            LEVEL.info: "[I]",
            LEVEL.warning: "[W]",
            LEVEL.error: "[E]",
            LEVEL.critical: "[C]"
        }

        self._filteringlv = LEVEL.default

    def debug(self, message):
        self.write(LEVEL.debug, message)

    def info(self, message):
        self.write(LEVEL.info, message)

    def warning(self, message):
        self.write(LEVEL.warning, message)

    def error(self, message):
        self.write(LEVEL.error, message)

    def critical(self, message):
        self.write(LEVEL.critical, message)

    def set_filteringlv(self, lv):
        self._assert_level(lv)

        self._filteringlv = lv

    def write(self, lv, message):
        self._assert_level(lv)

        if self._is_filtered(lv):
            return

        realmessage = self._levelstring_dict[lv] + \
                      self._get_datetime() + " " + \
                      str(message)
        print realmessage

    def _assert_level(self, lv):
        if lv<=LEVEL.lower_limit or lv>=LEVEL.upper_limit:
            raise ValueError("the range of the level is invalid.")

    def _is_filtered(self, lv):
        if lv>=self._filteringlv:
            return False
        return True

    def _get_datetime(self):
        yy = self._datetime.yy()
        yyyy = self._datetime.yyyy()
        momo = self._datetime.momo()
        dd = self._datetime.dd()
        youbi_j = self._datetime.youbi_j()
        youbi_e = self._datetime.youbi_e()
        hh = self._datetime.hh()
        mimi = self._datetime.mimi()
        ss = self._datetime.ss()
        return yy+"-"+momo+"-"+dd+" "+youbi_e+" "+hh+":"+mimi+":"+ss
