import html
import urllib.parse
import re
from . import register
from .base import Algorithm


@register
class HtmlEscapeBasicEncode(Algorithm):
    name = "HTML Escape (Basic)"
    category = "web_escape"
    mode = "encode"
    def process(self, s):
        return html.escape(s, quote=False)

@register
class HtmlEscapeFullEncode(Algorithm):
    name = "HTML Escape (Full)"
    category = "web_escape"
    mode = "encode"
    def process(self, s):
        return "".join(f"&#{ord(c)};" if ord(c) > 127 else html.escape(c) for c in s)

@register
class HtmlEscapeDecode(Algorithm):
    name = "HTML Escape"
    category = "web_escape"
    mode = "decode"
    def process(self, s):
        return html.unescape(s)

@register
class UrlEncodeEncode(Algorithm):
    name = "URL Encoding"
    category = "web_escape"
    mode = "encode"
    def process(self, s):
        return urllib.parse.quote(s, safe="")

@register
class UrlEncodeDecode(Algorithm):
    name = "URL Decoding"
    category = "web_escape"
    mode = "decode"
    def process(self, s):
        return urllib.parse.unquote(s)

@register
class UriComponentEncode(Algorithm):
    name = "URI Component Encoding"
    category = "web_escape"
    mode = "encode"
    def process(self, s):
        return urllib.parse.quote(s, safe="!~*'()")

@register
class UriComponentDecode(Algorithm):
    name = "URI Component Encoding"
    category = "web_escape"
    mode = "decode"
    def process(self, s):
        return urllib.parse.unquote(s)

@register
class PunycodeEncode(Algorithm):
    name = "Punycode IDN"
    category = "web_escape"
    mode = "encode"
    def process(self, s):
        return s.encode("idna").decode("ascii")

@register
class PunycodeDecode(Algorithm):
    name = "Punycode IDN"
    category = "web_escape"
    mode = "decode"
    def process(self, s):
        return s.encode("ascii").decode("idna")

@register
class QuotedPrintableEncode(Algorithm):
    name = "Quoted-printable"
    category = "web_escape"
    mode = "encode"
    def process(self, s):
        import quopri
        return quopri.encodestring(s.encode()).decode()

@register
class QuotedPrintableDecode(Algorithm):
    name = "Quoted-printable"
    category = "web_escape"
    mode = "decode"
    def process(self, s):
        import quopri
        return quopri.decodestring(s.encode()).decode("utf-8", errors="replace")

@register
class JsEscapeEncode(Algorithm):
    name = "Javascript Escape"
    category = "web_escape"
    mode = "encode"
    def process(self, s):
        result = []
        for c in s:
            o = ord(c)
            if o > 127:
                result.append(f"\\u{o:04x}")
            elif c in ('"', "'", "\\", "\n", "\r", "\t"):
                escapes = {'"': '\\"', "'": "\\'", "\\": "\\\\", "\n": "\\n", "\r": "\\r", "\t": "\\t"}
                result.append(escapes[c])
            else:
                result.append(c)
        return "".join(result)

@register
class JsEscapeDecode(Algorithm):
    name = "Javascript Escape"
    category = "web_escape"
    mode = "decode"
    def process(self, s):
        s = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), s)
        s = s.replace("\\n", "\n").replace("\\r", "\r").replace("\\t", "\t")
        s = s.replace('\\"', '"').replace("\\'", "'").replace("\\\\", "\\")
        return s
