import string
from . import register
from .base import Algorithm


def _caesar_shift(s, n, decode=False):
    shift = (-n if decode else n)
    result = []
    for c in s:
        if c.isupper():
            result.append(chr((ord(c) - 65 + shift) % 26 + 65))
        elif c.islower():
            result.append(chr((ord(c) - 97 + shift) % 26 + 97))
        else:
            result.append(c)
    return "".join(result)


@register
class CaesarEncode(Algorithm):
    name = "Caesar (ROT3)"
    category = "ciphers"
    mode = "encode"
    def process(self, s): return _caesar_shift(s, 3)

@register
class CaesarDecode(Algorithm):
    name = "Caesar (ROT3)"
    category = "ciphers"
    mode = "decode"
    def process(self, s): return _caesar_shift(s, 3, decode=True)

@register
class Rot13(Algorithm):
    name = "ROT13"
    category = "ciphers"
    mode = "both"
    def process(self, s): return _caesar_shift(s, 13)

@register
class Rot18Encode(Algorithm):
    name = "ROT18"
    category = "ciphers"
    mode = "both"
    def process(self, s):
        result = []
        for c in s:
            if c.isupper():   result.append(chr((ord(c) - 65 + 13) % 26 + 65))
            elif c.islower(): result.append(chr((ord(c) - 97 + 13) % 26 + 97))
            elif c.isdigit(): result.append(str((int(c) + 5) % 10))
            else:             result.append(c)
        return "".join(result)

@register
class Rot47(Algorithm):
    name = "ROT47"
    category = "ciphers"
    mode = "both"
    def process(self, s):
        return "".join(chr((ord(c) - 33 + 47) % 94 + 33) if 33 <= ord(c) <= 126 else c for c in s)

@register
class AtbashEncode(Algorithm):
    name = "Atbash"
    category = "ciphers"
    mode = "both"
    def process(self, s):
        result = []
        for c in s:
            if c.isupper():   result.append(chr(90 - (ord(c) - 65)))
            elif c.islower(): result.append(chr(122 - (ord(c) - 97)))
            else:             result.append(c)
        return "".join(result)

@register
class AffineEncode(Algorithm):
    name = "Affine (a=5,b=8)"
    category = "ciphers"
    mode = "encode"
    def process(self, s):
        a, b = 5, 8
        result = []
        for c in s:
            if c.isupper():   result.append(chr((a * (ord(c) - 65) + b) % 26 + 65))
            elif c.islower(): result.append(chr((a * (ord(c) - 97) + b) % 26 + 97))
            else:             result.append(c)
        return "".join(result)

@register
class AffineDecode(Algorithm):
    name = "Affine (a=5,b=8)"
    category = "ciphers"
    mode = "decode"
    def process(self, s):
        a, b = 5, 8
        # modular inverse of a mod 26: a=5 → inv=21
        a_inv = pow(a, -1, 26)
        result = []
        for c in s:
            if c.isupper():   result.append(chr(a_inv * (ord(c) - 65 - b) % 26 + 65))
            elif c.islower(): result.append(chr(a_inv * (ord(c) - 97 - b) % 26 + 97))
            else:             result.append(c)
        return "".join(result)

@register
class VigenereEncode(Algorithm):
    name = "Vigenère (key=KEY)"
    category = "ciphers"
    mode = "encode"
    def process(self, s):
        key = "KEY"
        result = []
        ki = 0
        for c in s:
            if c.isalpha():
                shift = ord(key[ki % len(key)].upper()) - 65
                base = 65 if c.isupper() else 97
                result.append(chr((ord(c) - base + shift) % 26 + base))
                ki += 1
            else:
                result.append(c)
        return "".join(result)

@register
class VigenereDecode(Algorithm):
    name = "Vigenère (key=KEY)"
    category = "ciphers"
    mode = "decode"
    def process(self, s):
        key = "KEY"
        result = []
        ki = 0
        for c in s:
            if c.isalpha():
                shift = ord(key[ki % len(key)].upper()) - 65
                base = 65 if c.isupper() else 97
                result.append(chr((ord(c) - base - shift) % 26 + base))
                ki += 1
            else:
                result.append(c)
        return "".join(result)

@register
class BaconianEncode(Algorithm):
    name = "Baconian Cipher"
    category = "ciphers"
    mode = "encode"
    def process(self, s):
        table = {chr(65+i): format(i, '05b').replace('0','A').replace('1','B') for i in range(26)}
        return " ".join(table.get(c.upper(), c) for c in s)

@register
class BaconianDecode(Algorithm):
    name = "Baconian Cipher"
    category = "ciphers"
    mode = "decode"
    def process(self, s):
        table = {format(i,'05b').replace('0','A').replace('1','B'): chr(65+i) for i in range(26)}
        parts = s.upper().split()
        return "".join(table.get(p, p) for p in parts)

@register
class BeaufortEncode(Algorithm):
    name = "Beaufort (key=KEY)"
    category = "ciphers"
    mode = "encode"
    def process(self, s):
        key = "KEY"
        result = []
        ki = 0
        for c in s:
            if c.isalpha():
                shift = ord(key[ki % len(key)].upper()) - 65
                base = 65 if c.isupper() else 97
                result.append(chr((shift - (ord(c) - base)) % 26 + base))
                ki += 1
            else:
                result.append(c)
        return "".join(result)

@register
class BeaufortDecode(Algorithm):
    name = "Beaufort (key=KEY)"
    category = "ciphers"
    mode = "decode"
    def process(self, s):
        # Beaufort is self-reciprocal
        return BeaufortEncode().process(s)

@register
class ScytaleEncode(Algorithm):
    name = "Scytale (cols=4)"
    category = "ciphers"
    mode = "encode"
    def process(self, s):
        cols = 4
        rows = -(-len(s) // cols)
        s = s.ljust(rows * cols)
        return "".join(s[r * cols + c] for c in range(cols) for r in range(rows))

@register
class ScytaleDecode(Algorithm):
    name = "Scytale (cols=4)"
    category = "ciphers"
    mode = "decode"
    def process(self, s):
        cols = 4
        rows = -(-len(s) // cols)
        return "".join(s[c * rows + r] for r in range(rows) for c in range(cols)).rstrip()

@register
class RailFenceEncode(Algorithm):
    name = "Rail Fence (rails=3)"
    category = "ciphers"
    mode = "encode"
    def process(self, s):
        rails = 3
        fence = [[] for _ in range(rails)]
        rail, direction = 0, 1
        for c in s:
            fence[rail].append(c)
            if rail == 0: direction = 1
            elif rail == rails - 1: direction = -1
            rail += direction
        return "".join("".join(r) for r in fence)

@register
class RailFenceDecode(Algorithm):
    name = "Rail Fence (rails=3)"
    category = "ciphers"
    mode = "decode"
    def process(self, s):
        rails = 3
        n = len(s)
        pattern = []
        rail, direction = 0, 1
        for i in range(n):
            pattern.append(rail)
            if rail == 0: direction = 1
            elif rail == rails - 1: direction = -1
            rail += direction
        indices = sorted(range(n), key=lambda i: (pattern[i], i))
        result = [''] * n
        for pos, char in zip(indices, s):
            result[pos] = char
        return "".join(result)

@register
class PlayfairEncode(Algorithm):
    name = "Playfair (key=KEY)"
    category = "ciphers"
    mode = "encode"
    def _build_square(self, key):
        seen = set()
        sq = []
        for c in (key.upper() + "ABCDEFGHIKLMNOPQRSTUVWXYZ"):
            if c == "J": c = "I"
            if c not in seen and c.isalpha():
                seen.add(c)
                sq.append(c)
        return sq

    def _pos(self, sq, c):
        if c == "J": c = "I"
        i = sq.index(c)
        return divmod(i, 5)

    def process(self, s):
        sq = self._build_square("KEY")
        s = s.upper().replace("J", "I")
        pairs = []
        i = 0
        while i < len(s):
            a = s[i] if s[i].isalpha() else None
            if a is None: i += 1; continue
            b_idx = i + 1
            while b_idx < len(s) and not s[b_idx].isalpha(): b_idx += 1
            b = s[b_idx] if b_idx < len(s) else "X"
            if a == b: b = "X"; i += 1
            else: i = b_idx + 1
            pairs.append((a, b))
        result = []
        for a, b in pairs:
            ra, ca = self._pos(sq, a)
            rb, cb = self._pos(sq, b)
            if ra == rb:
                result += [sq[ra * 5 + (ca+1)%5], sq[rb * 5 + (cb+1)%5]]
            elif ca == cb:
                result += [sq[((ra+1)%5)*5 + ca], sq[((rb+1)%5)*5 + cb]]
            else:
                result += [sq[ra*5+cb], sq[rb*5+ca]]
        return "".join(result)

@register
class PlayfairDecode(Algorithm):
    name = "Playfair (key=KEY)"
    category = "ciphers"
    mode = "decode"
    def _build_square(self, key):
        seen = set()
        sq = []
        for c in (key.upper() + "ABCDEFGHIKLMNOPQRSTUVWXYZ"):
            if c == "J": c = "I"
            if c not in seen and c.isalpha():
                seen.add(c)
                sq.append(c)
        return sq

    def _pos(self, sq, c):
        i = sq.index(c)
        return divmod(i, 5)

    def process(self, s):
        sq = self._build_square("KEY")
        s = s.upper()
        result = []
        for i in range(0, len(s)-1, 2):
            a, b = s[i], s[i+1]
            ra, ca = self._pos(sq, a)
            rb, cb = self._pos(sq, b)
            if ra == rb:
                result += [sq[ra*5 + (ca-1)%5], sq[rb*5 + (cb-1)%5]]
            elif ca == cb:
                result += [sq[((ra-1)%5)*5+ca], sq[((rb-1)%5)*5+cb]]
            else:
                result += [sq[ra*5+cb], sq[rb*5+ca]]
        return "".join(result)
