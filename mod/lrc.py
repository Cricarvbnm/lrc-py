from .component import *

import re
from typing import Iterable, Sequence, SupportsIndex, cast, overload


__all__ = ['Lrc']


class _Line:
    _line_pattern = re.compile(
        r'^((?:\[.+?:.+?\])+)(.*)', re.MULTILINE | re.IGNORECASE)

    _tag_pattern = re.compile(r'\[.+?:.+?\]')

    _tag_inside_pattern = re.compile(r'\[(.+?):(.+?)\]')

    def __init__(self, lyric: str, *tags: ABCTag):
        self.lyric = lyric
        self.tags = tags

    @classmethod
    def makeLines(cls, string: str) -> Sequence["_Line"]:
        m: list[tuple[str, str]] = re.findall(cls._line_pattern, string)
        if not m:
            raise ValueError("Not a string of lrc")

        lines: list[_Line] = list()
        for group in m:
            lyric = group[1]
            tags = cls._splitTags(group[0])

            if type(tags[0]) == TimeTag:
                lines.append(_Line(lyric, *tags))
            else:
                lines.append(_Line(lyric, *tags))

        return lines

    @classmethod
    def _splitTags(cls, tags_string: str):
        tag_strings: list[str] = re.findall(cls._tag_pattern, tags_string)
        if not tag_strings:
            raise ValueError("Not a string of tags")

        tags: list[ABCTag] = []
        for tag_str in tag_strings:
            tag_inside_match = cls._tag_inside_pattern.match(tag_str)
            if not tag_inside_match:
                raise ValueError("Not a string of tag")

            tags.append(Tag(*tag_inside_match.groups()))

        for i in range(len(tags)):
            tag = tags[i]
            if cls._isInteger(tag.name):
                tags[i] = TimeTag(int(tag.name), float(tag.val))

        return tags

    @staticmethod
    def _isInteger(string: str):
        try:
            int(string)
        except ValueError:
            return False
        return True


class Lrc:
    def __init__(self, lyrics: list[LyricLine], tags: list[Tag] | None = None):
        self._lyrics: list[LyricLine] = lyrics
        self._tags: list[Tag] = tags if tags else list()

    @classmethod
    def loads(cls, string: str):
        lines = _Line.makeLines(string)

        lyrics: list[LyricLine] = []
        tags: list[Tag] = []
        for line in lines:
            first_tag = line.tags[0]

            if type(first_tag) == TimeTag:
                for tag in line.tags:
                    lyrics.append(
                        LyricLine(cast(TimeTag, tag), line.lyric))
            else:
                tags.append(cast(Tag, first_tag))

        return Lrc(lyrics, tags)

    def dumps(self):
        lrc_str = ''

        for tag in self.tags:
            lrc_str += f'{tag!s}\n'

        for line in self.lyrics:
            lrc_str += f'{line.tag}{line.lyric}\n'

        return lrc_str

    @property
    def lyrics(self):
        return self._lyrics

    @property
    def tags(self):
        return self._tags

    @overload
    def __getitem__(self, i: slice) -> list[LyricLine]: ...

    @overload
    def __getitem__(self, i: SupportsIndex) -> LyricLine: ...

    def __getitem__(self, i):
        return self.lyrics[i]

    @overload
    def __setitem__(self, i: SupportsIndex, val: LyricLine): ...

    @overload
    def __setitem__(self, i: slice, val: Iterable[LyricLine]): ...

    def __setitem__(self, i, val):
        self._lyrics[i] = val

    def __delitem__(self, key: SupportsIndex | slice):
        del self._lyrics[key]
