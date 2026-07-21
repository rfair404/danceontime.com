#!/usr/bin/env python
"""
Composite the Dance On Time wordmark + tagline onto a generated illustration
(e.g. a Facebook/Instagram cover with open space on one side).

Wordmark rule (fixed brand style): "Dance" and "Time" in ink #2f2f41,
"On" in red #e5261f -- only the middle word is red. Georgia-Bold (Playfair
substitute), with a short red rule beneath. See docs/brand-image-generation-guide.md.

Usage:
    python scripts/add-title.py --base cover_base.png --out cover.png
    python scripts/add-title.py --base b.png --out c.png \
        --tagline "Social & Wedding Dance" "Lessons  ·  DJ  ·  Dance Floors" \
        "Madison, GA  ·  danceontime.com"
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFont

INK = (47, 47, 65)      # #2f2f41
RED = (229, 38, 31)     # #e5261f
STEEL = (92, 90, 90)    # #5c5a5a
GB = r"C:\Windows\Fonts\georgiab.ttf"   # Georgia Bold  (Playfair substitute)
G = r"C:\Windows\Fonts\georgia.ttf"     # Georgia

# The wordmark, split into coloured segments. ONLY "On" is red.
WORDMARK = [("Dance ", INK), ("On ", RED), ("Time", INK)]

DEFAULT_TAGLINES = [
    "Social & Wedding Dance",
    "Lessons  ·  DJ  ·  Dance Floors",
    "Madison, GA  ·  danceontime.com",
]


def draw_wordmark(base, x0=135, top=330, maxw=660):
    """Draw the Dance On Time wordmark + red rule at (x0, top); return the y
    just below the rule so taglines can follow."""
    d = ImageDraw.Draw(base)
    full = "".join(seg for seg, _ in WORDMARK)

    size = 128
    while size > 40:
        f = ImageFont.truetype(GB, size)
        if d.textbbox((0, 0), full, font=f)[2] <= maxw:
            break
        size -= 2
    f = ImageFont.truetype(GB, size)

    x = x0
    for seg, color in WORDMARK:
        d.text((x, top), seg, font=f, fill=color)
        x += d.textbbox((0, 0), seg, font=f)[2]

    bottom = top + d.textbbox((0, 0), full, font=f)[3]
    rule_y = bottom + 26
    d.rectangle([x0, rule_y, x0 + 250, rule_y + 8], fill=RED)
    return rule_y + 8


def main():
    ap = argparse.ArgumentParser(description="Overlay the Dance On Time wordmark + tagline.")
    ap.add_argument("--base", required=True, help="Base illustration (with open space for text).")
    ap.add_argument("--out", required=True, help="Output path.")
    ap.add_argument("--tagline", nargs="*", default=DEFAULT_TAGLINES,
                    help="Tagline lines under the wordmark (first line larger).")
    ap.add_argument("--x", type=int, default=135, help="Left margin for the text block.")
    ap.add_argument("--top", type=int, default=330, help="Top y for the wordmark.")
    ap.add_argument("--maxw", type=int, default=660, help="Max wordmark width (px).")
    args = ap.parse_args()

    base = Image.open(args.base).convert("RGB")
    d = ImageDraw.Draw(base)
    y = draw_wordmark(base, x0=args.x, top=args.top, maxw=args.maxw)

    y += 40
    for i, line in enumerate(args.tagline):
        size = 46 if i == 0 else (34 if i == 1 else 30)
        f = ImageFont.truetype(G, size)
        d.text((args.x, y), line, font=f, fill=STEEL)
        y += size + (20 if i == 0 else 18)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    base.save(args.out)
    print("Saved", args.out, base.size)


if __name__ == "__main__":
    main()
