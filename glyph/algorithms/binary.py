import base64
import binascii
from . import register
from .base import Algorithm

# ── helpers ──────────────────────────────────────────────────────────────────

BASE58_ALPHABET = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BASE62_ALPHABET = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
Z85_ALPHABET    = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"
BASE91_TABLE    = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~"'


def _int_to_base(n: int, alphabet: bytes) -> str:
    base = len(alphabet)
    if n == 0:
        return chr(alphabet[0])
    result = []
    while n:
        result.append(chr(alphabet[n % base]))
        n //= base
    return "".join(reversed(result))


def _base_to_int(s: str, alphabet: bytes) -> int:
    base = len(alphabet)
    decode_map = {chr(c): i for i, c in enumerate(alphabet)}
    n = 0
    for ch in s:
        n = n * base + decode_map[ch]
    return n


def _encode_arbitrary(data: bytes, alphabet: bytes) -> str:
    base = len(alphabet)
    n = int.from_bytes(data, "big")
    result = _int_to_base(n, alphabet) if n else chr(alphabet[0])
    # preserve leading zero bytes
    pad = sum(1 for b in data if b == 0)
    return chr(alphabet[0]) * pad + result


def _decode_arbitrary(s: str, alphabet: bytes) -> bytes:
    base = len(alphabet)
    decode_map = {chr(c): i for i, c in enumerate(alphabet)}
    n = 0
    for ch in s:
        n = n * base + decode_map[ch]
    result = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    pad = sum(1 for ch in s if ch == chr(alphabet[0]))
    return b"\x00" * pad + result


def _base91_encode(data: bytes) -> str:
    b = 0
    n = 0
    o = []
    for byte in data:
        b |= byte << n
        n += 8
        if n > 13:
            v = b & 8191
            if v > 88:
                b >>= 13
                n -= 13
            else:
                v = b & 16383
                b >>= 14
                n -= 14
            o.append(chr(BASE91_TABLE[v % 91]))
            o.append(chr(BASE91_TABLE[v // 91]))
    if n:
        o.append(chr(BASE91_TABLE[b % 91]))
        if n > 7 or b > 90:
            o.append(chr(BASE91_TABLE[b // 91]))
    return "".join(o)


def _base91_decode(s: str) -> bytes:
    decode_map = {chr(c): i for i, c in enumerate(BASE91_TABLE)}
    v = -1
    b = 0
    n = 0
    o = bytearray()
    for ch in s:
        c = decode_map.get(ch, -1)
        if c == -1:
            continue
        if v < 0:
            v = c
        else:
            v += c * 91
            b |= v << n
            n += 13 if (v & 8191) > 88 else 14
            v = -1
            while n > 7:
                o.append(b & 255)
                b >>= 8
                n -= 8
    if v > -1:
        o.append((b | v << n) & 255)
    return bytes(o)


# ── algorithms ────────────────────────────────────────────────────────────────

@register
class BinaryStringEncode(Algorithm):
    name = "Binary String"
    category = "binary_text"
    mode = "encode"
    def process(self, s):
        return " ".join(f"{ord(c):08b}" for c in s)

@register
class BinaryStringDecode(Algorithm):
    name = "Binary String"
    category = "binary_text"
    mode = "decode"
    def process(self, s):
        parts = s.split()
        return "".join(chr(int(p, 2)) for p in parts if p)

@register
class HexStringEncode(Algorithm):
    name = "Hexadecimal String"
    category = "binary_text"
    mode = "encode"
    def process(self, s):
        return s.encode().hex()

@register
class HexStringDecode(Algorithm):
    name = "Hexadecimal String"
    category = "binary_text"
    mode = "decode"
    def process(self, s):
        return bytes.fromhex(s.replace(" ", "").replace("0x", "")).decode("utf-8", errors="replace")

@register
class Base32Encode(Algorithm):
    name = "Base32"
    category = "binary_text"
    mode = "encode"
    def process(self, s):
        return base64.b32encode(s.encode()).decode()

@register
class Base32Decode(Algorithm):
    name = "Base32"
    category = "binary_text"
    mode = "decode"
    def process(self, s):
        pad = (8 - len(s) % 8) % 8
        return base64.b32decode(s.upper() + "=" * pad).decode("utf-8", errors="replace")

@register
class Base45Encode(Algorithm):
    name = "Base45"
    category = "binary_text"
    mode = "encode"
    def process(self, s):
        ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
        data = s.encode()
        res = []
        for i in range(0, len(data) - 1, 2):
            n = data[i] * 256 + data[i + 1]
            c, n = divmod(n, 45 * 45)
            b, a = divmod(n, 45)
            res += [ALPHA[a], ALPHA[b], ALPHA[c]]
        if len(data) % 2:
            b, a = divmod(data[-1], 45)
            res += [ALPHA[a], ALPHA[b]]
        return "".join(res)

@register
class Base45Decode(Algorithm):
    name = "Base45"
    category = "binary_text"
    mode = "decode"
    def process(self, s):
        ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
        dec = {c: i for i, c in enumerate(ALPHA)}
        res = []
        s = s.upper()
        for i in range(0, len(s) - 2, 3):
            n = dec[s[i]] + dec[s[i+1]] * 45 + dec[s[i+2]] * 45 * 45
            res += divmod(n, 256)
        if len(s) % 3 == 2:
            n = dec[s[-2]] + dec[s[-1]] * 45
            res.append(n)
        return bytes(res).decode("utf-8", errors="replace")

@register
class Base64Encode(Algorithm):
    name = "Base64"
    category = "binary_text"
    mode = "encode"
    def process(self, s):
        return base64.b64encode(s.encode()).decode()

@register
class Base64Decode(Algorithm):
    name = "Base64"
    category = "binary_text"
    mode = "decode"
    def process(self, s):
        pad = (4 - len(s) % 4) % 4
        return base64.b64decode(s + "=" * pad).decode("utf-8", errors="replace")

@register
class Ascii85Encode(Algorithm):
    name = "Ascii85"
    category = "binary_text"
    mode = "encode"
    def process(self, s):
        return base64.a85encode(s.encode()).decode()

@register
class Ascii85Decode(Algorithm):
    name = "Ascii85"
    category = "binary_text"
    mode = "decode"
    def process(self, s):
        return base64.a85decode(s).decode("utf-8", errors="replace")

@register
class Base58Encode(Algorithm):
    name = "Base58"
    category = "binary_text"
    mode = "encode"
    def process(self, s):
        return _encode_arbitrary(s.encode(), BASE58_ALPHABET)

@register
class Base58Decode(Algorithm):
    name = "Base58"
    category = "binary_text"
    mode = "decode"
    def process(self, s):
        return _decode_arbitrary(s, BASE58_ALPHABET).decode("utf-8", errors="replace")

@register
class Base62Encode(Algorithm):
    name = "Base62"
    category = "binary_text"
    mode = "encode"
    def process(self, s):
        return _encode_arbitrary(s.encode(), BASE62_ALPHABET)

@register
class Base62Decode(Algorithm):
    name = "Base62"
    category = "binary_text"
    mode = "decode"
    def process(self, s):
        return _decode_arbitrary(s, BASE62_ALPHABET).decode("utf-8", errors="replace")

@register
class Base91Encode(Algorithm):
    name = "Base91"
    category = "binary_text"
    mode = "encode"
    def process(self, s):
        return _base91_encode(s.encode())

@register
class Base91Decode(Algorithm):
    name = "Base91"
    category = "binary_text"
    mode = "decode"
    def process(self, s):
        return _base91_decode(s).decode("utf-8", errors="replace")

@register
class Z85Encode(Algorithm):
    name = "Z85"
    category = "binary_text"
    mode = "encode"
    def process(self, s):
        data = s.encode()
        pad = (4 - len(data) % 4) % 4
        data += b"\x00" * pad
        return base64.b85encode(data).decode()

@register
class Z85Decode(Algorithm):
    name = "Z85"
    category = "binary_text"
    mode = "decode"
    def process(self, s):
        return base64.b85decode(s).decode("utf-8", errors="replace").rstrip("\x00")
