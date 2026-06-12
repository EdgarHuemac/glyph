from . import register
from .base import Algorithm

ROMAN_VALS = [
    (1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),(90,'XC'),
    (50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')
]

EN_ONES = ['','one','two','three','four','five','six','seven','eight','nine',
           'ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen',
           'seventeen','eighteen','nineteen']
EN_TENS = ['','','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']

def _int_to_english(n):
    if n < 0: return 'negative ' + _int_to_english(-n)
    if n == 0: return 'zero'
    if n < 20: return EN_ONES[n]
    if n < 100: return EN_TENS[n//10] + ('-' + EN_ONES[n%10] if n%10 else '')
    if n < 1000: return EN_ONES[n//100] + ' hundred' + (' ' + _int_to_english(n%100) if n%100 else '')
    for v, name in [(1000000000,'billion'),(1000000,'million'),(1000,'thousand')]:
        if n >= v: return _int_to_english(n//v) + ' ' + name + (' ' + _int_to_english(n%v) if n%v else '')

KANJI_DIGITS = '〇一二三四五六七八九'
GREEK_DIGITS = {1:'α',2:'β',3:'γ',4:'δ',5:'ε',6:'ζ',7:'η',8:'θ',9:'ι',10:'κ',
                20:'λ',30:'μ',40:'ν',50:'ξ',60:'ο',70:'π',80:'ρ',90:'σ',100:'τ'}
HEBREW_DIGITS = {1:'א',2:'ב',3:'ג',4:'ד',5:'ה',6:'ו',7:'ז',8:'ח',9:'ט',10:'י',
                 20:'כ',30:'ל',40:'מ',50:'נ',60:'ס',70:'ע',80:'פ',90:'צ',100:'ק',
                 200:'ר',300:'ש',400:'ת'}
THAI_DIGITS = '๐๑๒๓๔๕๖๗๘๙'


@register
class NumToDecEncode(Algorithm):
    name = "Num to Dec"
    category = "numbers"
    mode = "encode"
    def process(self, s):
        return str(int(s))

@register
class NumFromDecDecode(Algorithm):
    name = "Num from Dec"
    category = "numbers"
    mode = "decode"
    def process(self, s): return str(int(s))

@register
class NumToBinEncode(Algorithm):
    name = "Num to Bin"
    category = "numbers"
    mode = "encode"
    def process(self, s): return bin(int(s))

@register
class NumFromBinDecode(Algorithm):
    name = "Num from Bin"
    category = "numbers"
    mode = "decode"
    def process(self, s): return str(int(s.replace('0b','').replace(' ',''), 2))

@register
class NumToOctEncode(Algorithm):
    name = "Num to Oct"
    category = "numbers"
    mode = "encode"
    def process(self, s): return oct(int(s))

@register
class NumFromOctDecode(Algorithm):
    name = "Num from Oct"
    category = "numbers"
    mode = "decode"
    def process(self, s): return str(int(s.replace('0o',''), 8))

@register
class NumToHexEncode(Algorithm):
    name = "Num to Hex"
    category = "numbers"
    mode = "encode"
    def process(self, s): return hex(int(s))

@register
class NumFromHexDecode(Algorithm):
    name = "Num from Hex"
    category = "numbers"
    mode = "decode"
    def process(self, s): return str(int(s.replace('0x',''), 16))

@register
class NumToRomanEncode(Algorithm):
    name = "Num to Roman"
    category = "numbers"
    mode = "encode"
    def process(self, s):
        n = int(s)
        result = ''
        for val, sym in ROMAN_VALS:
            while n >= val:
                result += sym
                n -= val
        return result

@register
class NumFromRomanDecode(Algorithm):
    name = "Num from Roman"
    category = "numbers"
    mode = "decode"
    def process(self, s):
        vals = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
        s = s.upper()
        total = 0
        for i, c in enumerate(s):
            if i+1 < len(s) and vals[c] < vals[s[i+1]]:
                total -= vals[c]
            else:
                total += vals[c]
        return str(total)

@register
class NumToEnglishEncode(Algorithm):
    name = "Num to English"
    category = "numbers"
    mode = "encode"
    def process(self, s): return _int_to_english(int(s))

@register
class NumToKanjiEncode(Algorithm):
    name = "Num to Kanji"
    category = "numbers"
    mode = "encode"
    def process(self, s): return "".join(KANJI_DIGITS[int(d)] for d in str(int(s)))

@register
class NumFromKanjiDecode(Algorithm):
    name = "Num from Kanji"
    category = "numbers"
    mode = "decode"
    def process(self, s): return str(int("".join(str(KANJI_DIGITS.index(c)) for c in s)))

@register
class NumToThaiEncode(Algorithm):
    name = "Num to Thai"
    category = "numbers"
    mode = "encode"
    def process(self, s): return "".join(THAI_DIGITS[int(d)] for d in str(s))

@register
class NumFromThaiDecode(Algorithm):
    name = "Num from Thai"
    category = "numbers"
    mode = "decode"
    def process(self, s): return "".join(str(THAI_DIGITS.index(c)) for c in s)

@register
class NumToNAryEncode(Algorithm):
    name = "Num to N-ary (base 36)"
    category = "numbers"
    mode = "encode"
    def process(self, s):
        n = int(s)
        digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if n == 0: return "0"
        result = ""
        while n:
            result = digits[n % 36] + result
            n //= 36
        return result
