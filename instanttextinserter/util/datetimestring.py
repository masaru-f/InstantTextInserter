# encoding: shift-jis

import time

class Datetime:
    """
    現在の日付時刻を string で取得.
    """
    def __init__(self):
        self._localtime = None
        self._youbitable_j = ["日","月","火","水","木","金","土"]
        self._youbitable_e = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]

    def yy(self):
        self._now()
        return time.strftime("%y", self._localtime)

    def yyyy(self):
        self._now()
        return time.strftime("%Y", self._localtime)

    def momo(self):
        self._now()
        return time.strftime("%m", self._localtime)

    def dd(self):
        self._now()
        return time.strftime("%d", self._localtime)

    def youbi_j(self):
        self._now()
        idx = int(time.strftime("%w", self._localtime))
        return self._youbitable_j[idx]

    def youbi_e(self):
        self._now()
        idx = int(time.strftime("%w", self._localtime))
        return self._youbitable_e[idx]

    def hh(self):
        self._now()
        return time.strftime("%H", self._localtime)

    def mimi(self):
        self._now()
        return time.strftime("%M", self._localtime)

    def ss(self):
        self._now()
        return time.strftime("%S", self._localtime)

    def _now(self):
        self._localtime = time.localtime()

if __name__ == "__main__":
    datetime = Datetime()

    yy = datetime.yy()
    yyyy = datetime.yyyy()
    momo = datetime.momo()
    dd = datetime.dd()
    youbi_j = datetime.youbi_j()
    youbi_e = datetime.youbi_e()
    hh = datetime.hh()
    mimi = datetime.mimi()
    ss = datetime.ss()

    print yy+"/"+momo+"/"+dd+"("+youbi_j+") "+hh+":"+mimi+":"+ss
    print yyyy+"/"+momo+"/"+dd+"("+youbi_e+") "+hh+":"+mimi+":"+ss


