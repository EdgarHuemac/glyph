import hashlib
import struct
from . import register
from .base import Algorithm


def _crc32(data: bytes) -> int:
    import zlib
    return zlib.crc32(data) & 0xFFFFFFFF


def _adler32(data: bytes) -> int:
    import zlib
    return zlib.adler32(data) & 0xFFFFFFFF


@register
class MD5Hash(Algorithm):
    name = "MD5"
    category = "hashes"
    mode = "encode"
    def process(self, s): return hashlib.md5(s.encode()).hexdigest()

@register
class SHA1Hash(Algorithm):
    name = "SHA-1"
    category = "hashes"
    mode = "encode"
    def process(self, s): return hashlib.sha1(s.encode()).hexdigest()

@register
class SHA256Hash(Algorithm):
    name = "SHA-256"
    category = "hashes"
    mode = "encode"
    def process(self, s): return hashlib.sha256(s.encode()).hexdigest()

@register
class SHA384Hash(Algorithm):
    name = "SHA-384"
    category = "hashes"
    mode = "encode"
    def process(self, s): return hashlib.sha384(s.encode()).hexdigest()

@register
class SHA512Hash(Algorithm):
    name = "SHA-512"
    category = "hashes"
    mode = "encode"
    def process(self, s): return hashlib.sha512(s.encode()).hexdigest()

@register
class SHA3_256Hash(Algorithm):
    name = "SHA3-256"
    category = "hashes"
    mode = "encode"
    def process(self, s): return hashlib.sha3_256(s.encode()).hexdigest()

@register
class SHA3_512Hash(Algorithm):
    name = "SHA3-512"
    category = "hashes"
    mode = "encode"
    def process(self, s): return hashlib.sha3_512(s.encode()).hexdigest()

@register
class BLAKE2bHash(Algorithm):
    name = "BLAKE2b"
    category = "hashes"
    mode = "encode"
    def process(self, s): return hashlib.blake2b(s.encode()).hexdigest()

@register
class BLAKE2sHash(Algorithm):
    name = "BLAKE2s"
    category = "hashes"
    mode = "encode"
    def process(self, s): return hashlib.blake2s(s.encode()).hexdigest()

@register
class CRC32Hash(Algorithm):
    name = "CRC32"
    category = "hashes"
    mode = "encode"
    def process(self, s): return f"{_crc32(s.encode()):08x}"

@register
class Adler32Hash(Algorithm):
    name = "Adler-32"
    category = "hashes"
    mode = "encode"
    def process(self, s): return f"{_adler32(s.encode()):08x}"
