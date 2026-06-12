# glyph

A terminal encoding & decoding swiss knife. 

Glyph is intended for developers, security researchers, and CTF players who frequently need to encode, decode, hash, or transform text without leaving the terminal.

It's essentially a offline, keyboard-driven alternative to web tools like DenCode or CyberChef, but designed to be more complete and scalable. Useful for anyone who works in environments where opening a browser is slow, inconvenient, or not an option (like SSH sessions or air-gapped machines).

<img width="1200" height="630" alt="glyph" src="https://github.com/user-attachments/assets/ba8e6e74-be09-4376-8290-c2ac591b126b" />


## Quick (very quick...) start

```bash
python glyph.py
```

Type anything. Results from all 139 algorithms update **instantly** on every keystroke.

## CLI flags

| Flag | Description | Example |
|------|-------------|---------|
| `-m encode` | Show only encode algorithms | `python glyph.py -m encode` |
| `-m decode` | Show only decode algorithms | `python glyph.py -m decode` |
| `-c <category>` | Filter to one category | `python glyph.py -c ciphers` |
| `-x <names>` | Exclude specific algorithms | `python glyph.py -x "MD5,CRC32"` |

## Key bindings

| Key | Action |
|-----|--------|
| `↑ / ↓` | Navigate results |
| `PgUp / PgDn` | Fast scroll |
| `Enter` | Copy selected result into input (chain transforms!) |
| `Ctrl+U` | Clear input |
| `Ctrl+C` | Quit |

## Categories

| Badge | Category | Algorithms |
|-------|----------|------------|
| `BIN` | binary_text | Base64, Base58, Base91, Hex, Binary, Z85… |
| `WEB` | web_escape | URL, HTML, JS Escape, Punycode… |
| `CPH` | ciphers | Caesar, ROT13, Vigenère, Atbash, Playfair… |
| `NUM` | numbers | Dec/Bin/Oct/Hex, Roman, Kanji, Thai… |
| `UNI` | unicode_repr | Morse, Braille, Tap Code, Pigpen… |
| `NRM` | unicode_norm | NFC, NFD, NFKC, NFKD, Fold Case… |
| `TXT` | text_case | camelCase, snake_case, UPPER, Reverse… |
| `UTL` | text_utils | Line Sort, Word Count, Whitespace Collapse… |
| `DTE` | dates | UNIX, ISO8601, RFC2822, HTTP-Date… |
| `CLR` | colors | RGB, HSL, HWB, CMYK, XYZ, Lab… |
| `HSH` | hashes | MD5, SHA-256/512, BLAKE2, CRC32… |

## Chaining transforms

Press **Enter** on any result to push it into the input field. This lets you chain:
```
"Hello" → Base64 → "SGVsbG8=" → [Enter] → ROT13 → "FTyybY="
```

## Adding algorithms

Drop a new file in `glyph/algorithms/` and decorate your class:

```python
from . import register
from .base import Algorithm

@register
class MyAlgo(Algorithm):
    name = "My Algorithm"
    category = "binary_text"   # existing or new category
    mode = "encode"            # "encode", "decode", or "both"

    def process(self, input_string: str) -> str:
        return input_string[::-1]  # example: reverse
```

That easy. Zero changes to the UI or any other file.

## Requirements

Python 3.10+ with standard library only. On Windows, also install:
```
pip install windows-curses
```
