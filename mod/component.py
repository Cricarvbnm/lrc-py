from typing import override


__all__ = ['Tag', 'TimeTag', 'LyricLine']


class Tag:
    def __init__(self, name: str, val: str):
        self._name = name
        self._val = val

    @property
    def name(self) -> str:
        return self._name

    @property
    def val(self) -> str:
        return self._val

    def toTuple(self):
        return self.name, self.val

    def __str__(self) -> str:
        return f'[{self.name}:{self.val}]'

    def __hash__(self) -> int:
        return hash((self.name, self.val))


class TimeTag(Tag):
    def __init__(self, minute: int, second: float):
        self._minute = minute
        self._second = second

    @property
    def minute(self):
        return self._minute

    @property
    def second(self):
        return self._second

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


class LyricLine:
    def __init__(self, time_tag: TimeTag, lyric: str):
        self._tag = time_tag
        self._lyric = lyric

    @property
    def tag(self):
        return self._tag

    @property
    def lyric(self):
        return self._lyric
