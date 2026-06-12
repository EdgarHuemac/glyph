import unicodedata
from . import register
from .base import Algorithm

MORSE = {
    'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---',
    'K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-',
    'U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..',
    '0':'-----','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....',
    '6':'-....','7':'--...','8':'---..','9':'----.',
    '.':'.-.-.-',',':'--..--','?':'..--..','!':'-.-.--','/':'-..-.','(':'-.--.',')':'-.--.-',
    '&':'.-...',':':'---...',';':'-.-.-.','=':'-...-','+':'.-.-.','_':'..--.-',
    '"':'.-..-.','$':'...-..-','@':'.--.-.', ' ': '/'
}
MORSE_REV = {v: k for k, v in MORSE.items()}

BRAILLE = {
    'a':'⠁','b':'⠃','c':'⠉','d':'⠙','e':'⠑','f':'⠋','g':'⠛','h':'⠓','i':'⠊','j':'⠚',
    'k':'⠅','l':'⠇','m':'⠍','n':'⠝','o':'⠕','p':'⠏','q':'⠟','r':'⠗','s':'⠎','t':'⠞',
    'u':'⠥','v':'⠧','w':'⠺','x':'⠭','y':'⠽','z':'⠵',
    '1':'⠂','2':'⠆','3':'⠒','4':'⠲','5':'⠢','6':'⠖','7':'⠶','8':'⠦','9':'⠔','0':'⠴',
    ' ':'⠀',',':'⠠','.':"⠨",'?':'⠬','!':'⠰'
}
BRAILLE_REV = {v: k for k, v in BRAILLE.items()}

TAP_CODE = {c: f"{(i)//5+1}.{(i)%5+1}" for i, c in enumerate("ABCDEFGHIKLMNOPQRSTUVWXYZ")}
TAP_CODE_REV = {v: k for k, v in TAP_CODE.items()}

PIGPEN = {
    'A':'⌐','B':'¬','C':'½','D':'¼','E':'¡','F':'«','G':'»','H':'░','I':'▒',
    'J':'▓','K':'│','L':'┤','M':'╡','N':'╢','O':'╖','P':'╕','Q':'╣','R':'║',
    'S':'╗','T':'╝','U':'╜','V':'╛','W':'┐','X':'└','Y':'┴','Z':'┬'
}
PIGPEN_REV = {v: k for k, v in PIGPEN.items()}


@register
class UnicodeEscapeEncode(Algorithm):
    name = "Unicode Escape"
    category = "unicode_repr"
    mode = "encode"
    def process(self, s):
        return "".join(f"\\u{ord(c):04x}" if ord(c) > 127 else c for c in s)

@register
class UnicodeEscapeDecode(Algorithm):
    name = "Unicode Escape"
    category = "unicode_repr"
    mode = "decode"
    def process(self, s):
        return s.encode().decode("unicode_escape")

@register
class StringLiteralEncode(Algorithm):
    name = "String Literal"
    category = "unicode_repr"
    mode = "encode"
    def process(self, s):
        return repr(s)

@register
class StringLiteralDecode(Algorithm):
    name = "String Literal"
    category = "unicode_repr"
    mode = "decode"
    def process(self, s):
        return eval(s)

@register
class MorseEncode(Algorithm):
    name = "Morse Code"
    category = "unicode_repr"
    mode = "encode"
    def process(self, s):
        return " ".join(MORSE.get(c.upper(), "?") for c in s)

@register
class MorseDecode(Algorithm):
    name = "Morse Code"
    category = "unicode_repr"
    mode = "decode"
    def process(self, s):
        return "".join(MORSE_REV.get(p, "?") for p in s.split())

@register
class BrailleEncode(Algorithm):
    name = "Braille"
    category = "unicode_repr"
    mode = "encode"
    def process(self, s):
        return "".join(BRAILLE.get(c.lower(), c) for c in s)

@register
class BrailleDecode(Algorithm):
    name = "Braille"
    category = "unicode_repr"
    mode = "decode"
    def process(self, s):
        return "".join(BRAILLE_REV.get(c, c) for c in s)

@register
class TapCodeEncode(Algorithm):
    name = "Tap Code"
    category = "unicode_repr"
    mode = "encode"
    def process(self, s):
        return " ".join(TAP_CODE.get(c.upper().replace("J","I"), "?") for c in s if c.isalpha() or c == " ")

@register
class TapCodeDecode(Algorithm):
    name = "Tap Code"
    category = "unicode_repr"
    mode = "decode"
    def process(self, s):
        return "".join(TAP_CODE_REV.get(p, "?") for p in s.split())

@register
class PigpenEncode(Algorithm):
    name = "Pigpen Cipher"
    category = "unicode_repr"
    mode = "encode"
    def process(self, s):
        return "".join(PIGPEN.get(c.upper(), c) for c in s)

@register
class PigpenDecode(Algorithm):
    name = "Pigpen Cipher"
    category = "unicode_repr"
    mode = "decode"
    def process(self, s):
        return "".join(PIGPEN_REV.get(c, c) for c in s)

# ── Unicode normalization ─────────────────────────────────────────────────────

@register
class UnicodeNFC(Algorithm):
    name = "Unicode NFC"
    category = "unicode_norm"
    mode = "both"
    def process(self, s): return unicodedata.normalize("NFC", s)

@register
class UnicodeNFD(Algorithm):
    name = "Unicode NFD"
    category = "unicode_norm"
    mode = "both"
    def process(self, s): return unicodedata.normalize("NFD", s)

@register
class UnicodeNFKC(Algorithm):
    name = "Unicode NFKC"
    category = "unicode_norm"
    mode = "both"
    def process(self, s): return unicodedata.normalize("NFKC", s)

@register
class UnicodeNFKD(Algorithm):
    name = "Unicode NFKD"
    category = "unicode_norm"
    mode = "both"
    def process(self, s): return unicodedata.normalize("NFKD", s)

@register
class UnicodeFoldCase(Algorithm):
    name = "Unicode Fold Case"
    category = "unicode_norm"
    mode = "encode"
    def process(self, s): return s.casefold()

@register
class UnicodeStyledText(Algorithm):
    name = "Unicode Styled Text"
    category = "unicode_norm"
    mode = "encode"
    BOLD_OFFSET = 0x1D400 - ord('A')
    def process(self, s):
        result = []
        for c in s:
            if 'A' <= c <= 'Z':
                result.append(chr(ord(c) + self.BOLD_OFFSET))
            elif 'a' <= c <= 'z':
                result.append(chr(ord(c) + self.BOLD_OFFSET + 26))
            else:
                result.append(c)
        return "".join(result)
