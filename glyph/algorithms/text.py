import re
from . import register
from .base import Algorithm


def _words(s):
    return re.findall(r"[a-zA-Z0-9]+", s)


@register
class UpperCamelCase(Algorithm):
    name = "UpperCamelCase"
    category = "text_case"
    mode = "encode"
    def process(self, s):
        return "".join(w.capitalize() for w in _words(s))

@register
class LowerCamelCase(Algorithm):
    name = "lowerCamelCase"
    category = "text_case"
    mode = "encode"
    def process(self, s):
        words = _words(s)
        return words[0].lower() + "".join(w.capitalize() for w in words[1:]) if words else ""

@register
class UpperSnakeCase(Algorithm):
    name = "UPPER_SNAKE_CASE"
    category = "text_case"
    mode = "encode"
    def process(self, s): return "_".join(w.upper() for w in _words(s))

@register
class LowerSnakeCase(Algorithm):
    name = "lower_snake_case"
    category = "text_case"
    mode = "encode"
    def process(self, s): return "_".join(w.lower() for w in _words(s))

@register
class UpperKebabCase(Algorithm):
    name = "UPPER-KEBAB-CASE"
    category = "text_case"
    mode = "encode"
    def process(self, s): return "-".join(w.upper() for w in _words(s))

@register
class LowerKebabCase(Algorithm):
    name = "lower-kebab-case"
    category = "text_case"
    mode = "encode"
    def process(self, s): return "-".join(w.lower() for w in _words(s))

@register
class DotCase(Algorithm):
    name = "dot.case"
    category = "text_case"
    mode = "encode"
    def process(self, s): return ".".join(w.lower() for w in _words(s))

@register
class PathCase(Algorithm):
    name = "path/case"
    category = "text_case"
    mode = "encode"
    def process(self, s): return "/".join(w.lower() for w in _words(s))

@register
class ConstantCase(Algorithm):
    name = "CONSTANT_CASE"
    category = "text_case"
    mode = "encode"
    def process(self, s): return "_".join(w.upper() for w in _words(s))

@register
class UpperCase(Algorithm):
    name = "UPPER CASE"
    category = "text_case"
    mode = "encode"
    def process(self, s): return s.upper()

@register
class LowerCase(Algorithm):
    name = "lower case"
    category = "text_case"
    mode = "encode"
    def process(self, s): return s.lower()

@register
class SwapCase(Algorithm):
    name = "Swap Case"
    category = "text_case"
    mode = "encode"
    def process(self, s): return s.swapcase()

@register
class Capitalize(Algorithm):
    name = "Capitalize"
    category = "text_case"
    mode = "encode"
    def process(self, s): return s.capitalize()

@register
class AlternatingCaps(Algorithm):
    name = "aLtErNaTiNg CaPs"
    category = "text_case"
    mode = "encode"
    def process(self, s):
        return "".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(s))

@register
class Reverse(Algorithm):
    name = "Reverse"
    category = "text_case"
    mode = "encode"
    def process(self, s): return s[::-1]

@register
class HalfWidth(Algorithm):
    name = "Half Width"
    category = "text_case"
    mode = "encode"
    def process(self, s):
        import unicodedata
        return unicodedata.normalize("NFKC", s)

@register
class FullWidth(Algorithm):
    name = "Full Width"
    category = "text_case"
    mode = "encode"
    def process(self, s):
        result = []
        for c in s:
            o = ord(c)
            if 0x21 <= o <= 0x7E:
                result.append(chr(o - 0x21 + 0xFF01))
            elif c == " ":
                result.append("\u3000")
            else:
                result.append(c)
        return "".join(result)

# ── text_utils ────────────────────────────────────────────────────────────────

@register
class LineSort(Algorithm):
    name = "Line Sort"
    category = "text_utils"
    mode = "encode"
    def process(self, s): return "\n".join(sorted(s.splitlines()))

@register
class LineUnique(Algorithm):
    name = "Line Unique"
    category = "text_utils"
    mode = "encode"
    def process(self, s):
        seen = set()
        result = []
        for line in s.splitlines():
            if line not in seen:
                seen.add(line)
                result.append(line)
        return "\n".join(result)

@register
class LineReverse(Algorithm):
    name = "Line Reverse"
    category = "text_utils"
    mode = "encode"
    def process(self, s): return "\n".join(reversed(s.splitlines()))

@register
class WordCount(Algorithm):
    name = "Word Count"
    category = "text_utils"
    mode = "encode"
    def process(self, s): return str(len(s.split()))

@register
class CharCount(Algorithm):
    name = "Character Count"
    category = "text_utils"
    mode = "encode"
    def process(self, s): return str(len(s))

@register
class WhitespaceCollapse(Algorithm):
    name = "Whitespace Collapse"
    category = "text_utils"
    mode = "encode"
    def process(self, s): return re.sub(r"\s+", " ", s).strip()
