# lrc

## Component

`Lrc`: Representing a .lrc content

`LyricLine`: Representing a line of lyric(Time tag and Lyric included)

`TimeTag`: Representing a time tag(minute and second only like `19:23.970`)

`Tag`: Representing a tag

## Usage

```py
from lrc import *


lrc_file = 'test.lrc'

# Read .lrc content from a file
with open(lrc_file, encoding='utf-8') as f:
    lrc_str = f.read()

lrc = Lrc.loads(lrc_str) # Load the content from a string

# Example: Make specified line of lyric appearing earlier
# All the property are read-only in objects of `Lrc`, `Tag`, `TimeTag` and so on
lyrics: list[LyricLine] = []
for i, line in enumerate(lrc.lyrics):
    if i % 2 == 0:
        lyrics.append(line)
    else:
        # So you have to construct a new object
        lyrics.append(LyricLine(lyrics[-1].tag, line.lyric))

new_lrc = Lrc(lyrics, lrc.tags) # Like above
# Dump a lrc object to a string where tags are at the beginning, lyrics following.
#  Only one time tag at a line
new_lrc_str = new_lrc.dumps()

# Write the string of lrc to a new file
with open(f'test.new.lrc', 'w', encoding='utf-8') as f:
    f.write(new_lrc_str)
```
