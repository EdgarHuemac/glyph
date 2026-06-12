import re
import colorsys
from . import register
from .base import Algorithm

CSS_COLORS = {
    'red':'#FF0000','green':'#008000','blue':'#0000FF','white':'#FFFFFF','black':'#000000',
    'yellow':'#FFFF00','cyan':'#00FFFF','magenta':'#FF00FF','orange':'#FFA500','purple':'#800080',
    'pink':'#FFC0CB','lime':'#00FF00','navy':'#000080','teal':'#008080','silver':'#C0C0C0',
    'gray':'#808080','grey':'#808080','maroon':'#800000','olive':'#808000','aqua':'#00FFFF',
}


def _hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        hex_str = "".join(c*2 for c in hex_str)
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))


def _parse_color(s):
    """Return (r, g, b) as 0-255 ints from various formats."""
    s = s.strip()
    # Named color
    if s.lower() in CSS_COLORS:
        return _hex_to_rgb(CSS_COLORS[s.lower()])
    # Hex
    if s.startswith('#') or re.fullmatch(r'[0-9a-fA-F]{3,8}', s):
        return _hex_to_rgb(s)
    # rgb(r,g,b)
    m = re.match(r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', s, re.I)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    # hsl(h,s%,l%)
    m = re.match(r'hsl\s*\(\s*([\d.]+)\s*,\s*([\d.]+)%?\s*,\s*([\d.]+)%?\s*\)', s, re.I)
    if m:
        h, sl, l = float(m.group(1))/360, float(m.group(2))/100, float(m.group(3))/100
        r, g, b = colorsys.hls_to_rgb(h, l, sl)
        return int(r*255), int(g*255), int(b*255)
    raise ValueError(f"Cannot parse color: {s}")


@register
class ColorNameEncode(Algorithm):
    name = "Color Name"
    category = "colors"
    mode = "encode"
    def process(self, s):
        r, g, b = _parse_color(s)
        hex_val = f"#{r:02X}{g:02X}{b:02X}".lower()
        rev = {v.lower(): k for k, v in CSS_COLORS.items()}
        return rev.get(hex_val, f"#{r:02X}{g:02X}{b:02X} (no name)")

@register
class RGBHexEncode(Algorithm):
    name = "RGB Color (Hex)"
    category = "colors"
    mode = "encode"
    def process(self, s):
        r, g, b = _parse_color(s)
        return f"#{r:02X}{g:02X}{b:02X}"

@register
class RGBColorEncode(Algorithm):
    name = "RGB Color"
    category = "colors"
    mode = "encode"
    def process(self, s):
        r, g, b = _parse_color(s)
        return f"rgb({r}, {g}, {b})"

@register
class HSLColorEncode(Algorithm):
    name = "HSL Color"
    category = "colors"
    mode = "encode"
    def process(self, s):
        r, g, b = _parse_color(s)
        h, l, sl = colorsys.rgb_to_hls(r/255, g/255, b/255)
        return f"hsl({h*360:.1f}, {sl*100:.1f}%, {l*100:.1f}%)"

@register
class HWBColorEncode(Algorithm):
    name = "HWB Color"
    category = "colors"
    mode = "encode"
    def process(self, s):
        r, g, b = _parse_color(s)
        rf, gf, bf = r/255, g/255, b/255
        w = min(rf, gf, bf)
        bk = 1 - max(rf, gf, bf)
        h, l, sl = colorsys.rgb_to_hls(rf, gf, bf)
        return f"hwb({h*360:.1f} {w*100:.1f}% {bk*100:.1f}%)"

@register
class CMYKColorEncode(Algorithm):
    name = "CMYK Color"
    category = "colors"
    mode = "encode"
    def process(self, s):
        r, g, b = _parse_color(s)
        rf, gf, bf = r/255, g/255, b/255
        k = 1 - max(rf, gf, bf)
        if k == 1:
            return "cmyk(0%, 0%, 0%, 100%)"
        c = (1 - rf - k) / (1 - k)
        m = (1 - gf - k) / (1 - k)
        y = (1 - bf - k) / (1 - k)
        return f"cmyk({c*100:.1f}%, {m*100:.1f}%, {y*100:.1f}%, {k*100:.1f}%)"

@register
class XYZColorEncode(Algorithm):
    name = "XYZ Color"
    category = "colors"
    mode = "encode"
    def process(self, s):
        r, g, b = _parse_color(s)
        def lin(c):
            c /= 255
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        rl, gl, bl = lin(r), lin(g), lin(b)
        x = rl * 0.4124 + gl * 0.3576 + bl * 0.1805
        y = rl * 0.2126 + gl * 0.7152 + bl * 0.0722
        z = rl * 0.0193 + gl * 0.1192 + bl * 0.9505
        return f"xyz({x:.4f}, {y:.4f}, {z:.4f})"

@register
class LabColorEncode(Algorithm):
    name = "Lab Color"
    category = "colors"
    mode = "encode"
    def process(self, s):
        r, g, b = _parse_color(s)
        def lin(c):
            c /= 255
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        rl, gl, bl = lin(r), lin(g), lin(b)
        x = (rl * 0.4124 + gl * 0.3576 + bl * 0.1805) / 0.95047
        y = (rl * 0.2126 + gl * 0.7152 + bl * 0.0722) / 1.0
        z = (rl * 0.0193 + gl * 0.1192 + bl * 0.9505) / 1.08883
        def f(t): return t ** (1/3) if t > 0.008856 else 7.787 * t + 16/116
        L = 116 * f(y) - 16
        a = 500 * (f(x) - f(y))
        b2 = 200 * (f(y) - f(z))
        return f"lab({L:.2f}, {a:.2f}, {b2:.2f})"
