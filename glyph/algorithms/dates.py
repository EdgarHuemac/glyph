from datetime import datetime, timezone
from email.utils import formatdate
from . import register
from .base import Algorithm


def _parse_dt(s):
    """Try to parse datetime from string or treat as unix timestamp."""
    s = s.strip()
    try:
        return datetime.fromtimestamp(float(s), tz=timezone.utc)
    except (ValueError, OSError):
        pass
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    return datetime.now(tz=timezone.utc)


@register
class UnixTimeEncode(Algorithm):
    name = "UNIX Time [sec]"
    category = "dates"
    mode = "encode"
    def process(self, s):
        return str(int(_parse_dt(s).timestamp()))

@register
class UnixTimeDecode(Algorithm):
    name = "UNIX Time [sec]"
    category = "dates"
    mode = "decode"
    def process(self, s):
        return datetime.fromtimestamp(float(s), tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

@register
class ISO8601DateEncode(Algorithm):
    name = "ISO8601 Date"
    category = "dates"
    mode = "encode"
    def process(self, s):
        return _parse_dt(s).strftime("%Y-%m-%d")

@register
class ISO8601DateTimeEncode(Algorithm):
    name = "ISO8601 Date (Extended)"
    category = "dates"
    mode = "encode"
    def process(self, s):
        return _parse_dt(s).strftime("%Y-%m-%dT%H:%M:%SZ")

@register
class ISO8601WeekEncode(Algorithm):
    name = "ISO8601 Date (Week)"
    category = "dates"
    mode = "encode"
    def process(self, s):
        dt = _parse_dt(s)
        return dt.strftime("%G-W%V-%u")

@register
class ISO8601OrdinalEncode(Algorithm):
    name = "ISO8601 Date (Ordinal)"
    category = "dates"
    mode = "encode"
    def process(self, s):
        dt = _parse_dt(s)
        return dt.strftime("%Y-%j")

@register
class RFC2822DateEncode(Algorithm):
    name = "RFC2822 Date"
    category = "dates"
    mode = "encode"
    def process(self, s):
        dt = _parse_dt(s)
        return formatdate(dt.timestamp(), usegmt=True)

@register
class CTimeDateEncode(Algorithm):
    name = "ctime Date"
    category = "dates"
    mode = "encode"
    def process(self, s):
        return _parse_dt(s).strftime("%a %b %e %H:%M:%S %Y")

@register
class HTTPDateEncode(Algorithm):
    name = "HTTP-Date"
    category = "dates"
    mode = "encode"
    def process(self, s):
        dt = _parse_dt(s)
        return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")

@register
class W3CDTFEncode(Algorithm):
    name = "W3C-DTF Date"
    category = "dates"
    mode = "encode"
    def process(self, s):
        return _parse_dt(s).strftime("%Y-%m-%dT%H:%M:%S+00:00")
