import time
import resource

def positive_integer(n):
    n = int(n)
    if n < 1:
        raise ValueError(n)
    return n

def thresholds(value, thresholds, default=None):
    for result, limit in thresholds:
        if value < limit:
            return result
    return default

class Elapsed(object):
    __slots__ = ["_lap", "start"]
    def source(self):
        raise NotImplementedError("you should subclass this class")
    def __init__(self):
        self.start = self.source()
        self._lap = self.start
    def __getstate__(self):
        return {"start": self.start, "_lap": self._lap}
    def __setstate__(self, d):
        self.start, self._lap = d['start'], d['_lap']
    @property
    def elapsed(self):
        return self.source() - self.start
    @property
    def lap(self):
        previous_lap = self._lap
        self._lap = self.source()
        return self._lap - previous_lap

class Timer(Elapsed):
    source = lambda self: time.time()
class CPUTime(Elapsed):
    def source(self):
        resources = resource.getrusage(resource.RUSAGE_SELF)
        return resources.ru_utime + resources.ru_stime
