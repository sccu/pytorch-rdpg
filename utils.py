"""
author: jeonjang@ebay.com

"""
from collections import defaultdict
from collections import Counter
import numbers
import datetime


class Holder(object):
    """Utility class for holding information.
    Examples:
    >>> info = Holder(lr=0.1, weight=0.7)
    >>> print(info.lr)
    0.1
    >>> info = Holder()
    >>> info.lr = 0.1
    >>> print(info.lr)
    0.1
    """
    def __init__(self, **kwargs):
        super().__init__()
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __add__(self, other):
        assert isinstance(other, Holder), f"'other' instance is required to be the Holder type. but actually {type(other)}."
        assert self.__dict__.keys().isdisjoint(
            other.__dict__), f"'other' has some attributes using same names with 'self'."
        self.__dict__.update(other.__dict__)
        return self

    def __repr__(self):
        return str(self.__dict__)


class Aggregator(object):
    def __init__(self, method="mean"):
        assert method in ["mean", "sum"], method
        self._method = method
        self._accumulator = defaultdict(lambda: 0.0)
        self._counter = Counter()
        self.start_time = datetime.datetime.now()

    def __call__(self, **kwargs):
        for k, v in kwargs.items():
            self.add(k, v)

    def add(self, key, value, count=1):
        assert isinstance(value, numbers.Number), type(value)
        assert isinstance(count, int) and count >= 0, count
        self._accumulator[key] += value * count
        self._counter[key] += count

        if key in self._counter and key.isidentifier():
            setattr(Aggregator, key, property(lambda s: s.aggregate(key)))

    def aggregate(self, key, method=None):
        assert method in [None, "mean", "sum"], method
        return getattr(self, method or self._method)(key)

    def mean(self, key):
        return float(self._accumulator[key] / (self._counter[key] or 1))

    def sum(self, key):
        return self._accumulator[key]

    def count(self, key):
        return self._counter[key]

    def speed(self, key=None):
        if key is None:
            key = list(self._counter.keys())[0]
        return float(self._counter[key] / ((datetime.datetime.now() - self.start_time).total_seconds() or 1.0))

    def time(self, key=None):
        return (datetime.datetime.now() - self.start_time).total_seconds() / (self._counter[key] or 1)

    def clear(self):
        self._accumulator.clear()
        self._counter.clear()
        self.start_time = datetime.datetime.now()

    reset = clear


if __name__ == "__main__":
    agg = Aggregator()

    # example 1
    agg.add("loss", 1.2)
    agg.add("accuracy", 0.95)
    # example 2
    agg(loss=1.0, accuracy=0.97)
    # get the aggregated value.
    print(agg.test)
    assert agg.loss == 1.1 and agg.accuracy == 0.96
