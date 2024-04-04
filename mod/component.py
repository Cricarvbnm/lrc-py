from typing import override
from abc import ABCMeta, abstractmethod


__all__ = ['Tag', 'TimeTag', 'LyricLine', 'ABCTag']


class ABCTag(metaclass=ABCMeta):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def val(self) -> str: ...

    @abstractmethod
    def toTuple(self) -> tuple: ...

    @abstractmethod
    def __str__(self) -> str:
        return f'[{self.name}:{self.val}]'

    @abstractmethod
    def __hash__(self) -> int:
        return hash((self.name, self.val))


class Tag(ABCTag):
    def __init__(self, name: str, val: str):
        self._name = name
        self._val = val

    @property
    @override
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, val: str):
        self._name = val

    @property
    @override
    def val(self) -> str:
        return self._val

    @val.setter
    def val(self, val: str):
        self._val = val

    @override
    def toTuple(self):
        return self.name, self.val

    @override
    def __str__(self):
        return super().__str__()

    @override
    def __hash__(self) -> int:
        return super().__hash__()


class TimeTag(ABCTag):
    def __init__(self, minute: int, second: float):
        self._minute = minute
        self._second = second

    @property
    def minute(self):
        return self._minute

    @minute.setter
    def minute(self, val: int):
        self._minute = val

    @property
    def second(self):
        return self._second

    @second.setter
    def second(self, val: float):
        self._second = val

    @property
    @override
    def name(self):
        return f'{self.minute:02}'

    @property
    @override
    def val(self):
        int_part = int(self.second)
        float_part = int((self.second - int_part) * 1000)
        return f'{int_part:02}.{float_part:<03d}'

    @override
    def toTuple(self):
        return self.minute, self.second

    @override
    def __hash__(self):
        return hash((self.minute, self.second))

    @override
    def __str__(self) -> str:
        return super().__str__()


class LyricLine:
    def __init__(self, time_tag: TimeTag, lyric: str):
        self._tag = time_tag
        self._lyric = lyric

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, val: TimeTag):
        self._tag = val

    @property
    def lyric(self):
        return self._lyric

    @lyric.setter
    def lyric(self, val: str):
        self._lyric = val
