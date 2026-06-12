import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        prog="glyph",
        description="Glyph — a terminal encoding/decoding swiss knife",
    )
    parser.add_argument(
        "-m", "--mode",
        choices=["encode", "decode"],
        default=None,
        help="Filter to only encode or decode algorithms",
    )
    parser.add_argument(
        "-c", "--category",
        default=None,
        help="Show only algorithms from this category (e.g. ciphers, binary_text)",
    )
    parser.add_argument(
        "-x", "--exclude",
        default=None,
        help="Comma-separated algorithm names to hide",
    )
    return parser.parse_args()
