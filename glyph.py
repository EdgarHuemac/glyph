#!/usr/bin/env python3
"""
Glyph — Terminal encoding & decoding swiss knife
Usage:  python glyph.py [-m encode|decode] [-c category] [-x algo1,algo2]
"""
import curses
import sys
import os

# Allow running as `python glyph.py` from the project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from glyph.cli import parse_args
from glyph.ui import GlyphUI


def main():
    config = parse_args()
    try:
        curses.wrapper(lambda stdscr: GlyphUI(stdscr, config).run())
    except KeyboardInterrupt:
        pass
    print("\nGlyph closed. Goodbye!")


if __name__ == "__main__":
    main()
