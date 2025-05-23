from .mod.lrc import Lrc
from .mod.component import Tag, TimeTag, LyricLine


__all__ = ['Lrc', 'Tag', 'TimeTag', 'LyricLine']


def main():
    from objprint import op

    with open('resource/test.lrc', encoding='utf-8') as f:
        string = f.read()

    op(l := Lrc.loads(string))
    l[2:3][0].tag.minute = 3


if __name__ == '__main__':
    main()
