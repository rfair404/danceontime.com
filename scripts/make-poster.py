#!/usr/bin/env python
"""
Build a print-ready 8.5x11 Dance On Time lesson poster (2550x3300 @ 300 DPI).

Pairs a brand illustration (from generate-brand-image.py) with the class
details, laid out for framing. Re-run it whenever the schedule changes.

Usage:
    python scripts/make-poster.py --art poster_art.png \
        --headline "West Coast Swing" --when "1st, 3rd & 5th Tuesday" \
        --time "7:00 - 8:30 PM" --price "$10 per person" \
        --venue "The Variety Works" --city "Madison, Georgia" \
        --out marketing/lesson-poster.png --pdf

Any --time left unset renders a visible TIME TBD placeholder so the gap is
obvious in a proof rather than silently shipping.
"""
import argparse, os, sys
from PIL import Image, ImageChops, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brand import (INK, RED, STEEL, WHITE, GEORGIA, GEORGIA_BOLD,
                   GEORGIA_ITALIC, WORDMARK)

DPI = 300
W, H = int(8.5 * DPI), int(11 * DPI)   # 2550 x 3300
MARGIN = 200                            # ~0.67in, clears a frame lip


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(d, text, f):
    return d.textbbox((0, 0), text, font=f)[2]


def th(d, text, f):
    return d.textbbox((0, 0), text, font=f)[3]


def center(d, y, text, f, fill):
    d.text(((W - tw(d, text, f)) // 2, y), text, font=f, fill=fill)
    return y + th(d, text, f)


def center_tracked(d, y, text, f, fill, track=14):
    """Centred text with extra letter-spacing, for the small caps kicker."""
    widths = [tw(d, c, f) for c in text]
    total = sum(widths) + track * (len(text) - 1)
    x = (W - total) // 2
    for c, cw in zip(text, widths):
        d.text((x, y), c, font=f, fill=fill)
        x += cw + track
    return y + th(d, text, f)


def center_wordmark(d, y, size):
    f = font(GEORGIA_BOLD, size)
    total = sum(tw(d, seg, f) for seg, _ in WORDMARK)
    x = (W - total) // 2
    for seg, color in WORDMARK:
        d.text((x, y), seg, font=f, fill=color)
        x += tw(d, seg, f)
    return y + th(d, "Dance On Time", f)


def rule(d, y, width=360, height=7, color=RED):
    d.rectangle([(W - width) // 2, y, (W + width) // 2, y + height], fill=color)
    return y + height


def trim(im, thresh=248):
    """Crop the illustration's surrounding whitespace so it sits tight."""
    g = im.convert("L")
    bbox = g.point(lambda p: 255 if p < thresh else 0).getbbox()
    return im.crop(bbox) if bbox else im


def normalize_white(im, thresh=246):
    """Lift the illustration's near-white background to pure white.

    Generated art comes back at ~253 rather than 255, which prints as a faint
    gray panel against the page. Only pixels whose darkest channel is already
    near-white are touched, so line art and reds are untouched.
    """
    r, g, b = im.split()
    darkest = ImageChops.darker(ImageChops.darker(r, g), b)
    im.paste(WHITE, mask=darkest.point(lambda p: 255 if p >= thresh else 0))
    return im


def feather(im, pad):
    """Fade the illustration's edges into the page.

    Without this the faint floorboard lines stop dead at the crop boundary and
    read as a visible rectangle around the art.
    """
    if pad <= 0:
        return im
    w, h = im.size
    alpha = Image.new("L", (w, h), 255)
    dr = ImageDraw.Draw(alpha)
    for i in range(pad):
        dr.rectangle([i, i, w - 1 - i, h - 1 - i], outline=int(255 * i / pad))
    return Image.composite(im, Image.new("RGB", (w, h), WHITE), alpha)


def main():
    ap = argparse.ArgumentParser(description="Build an 8.5x11 lesson poster.")
    ap.add_argument("--art", required=True, help="Brand illustration to place.")
    ap.add_argument("--out", required=True)
    ap.add_argument("--kicker", default="GROUP DANCE LESSONS")
    ap.add_argument("--headline", default="West Coast Swing")
    ap.add_argument("--when", required=True, help='e.g. "1st, 3rd & 5th Tuesday"')
    ap.add_argument("--time", default=None, help='e.g. "7:00 - 8:30 PM"')
    ap.add_argument("--price", default="$10 per person")
    ap.add_argument("--venue", default="The Variety Works")
    ap.add_argument("--city", default="Madison, Georgia")
    ap.add_argument("--note", default="No partner needed  ·  Beginners welcome")
    ap.add_argument("--phone", default="(706) 431-8290")
    ap.add_argument("--url", default="danceontime.com")
    ap.add_argument("--feather", type=int, default=60,
                    help="Px of edge fade blending the art into the page (0 = off).")
    ap.add_argument("--pdf", action="store_true", help="Also write a print PDF.")
    args = ap.parse_args()

    canvas = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(canvas)

    # ---- top block -------------------------------------------------
    y = MARGIN
    y = center_wordmark(d, y, 104) + 34
    y = rule(d, y) + 58
    y = center_tracked(d, y, args.kicker, font(GEORGIA, 50), STEEL) + 34
    y = center(d, y, args.headline, font(GEORGIA_BOLD, 156), INK)
    top_end = y + 40

    # ---- bottom block (measured, then anchored to the bottom) -------
    time_text = args.time or "TIME TBD"
    time_fill = INK if args.time else RED
    lines = [
        (args.when,   font(GEORGIA_BOLD, 92),   INK,   26),
        (time_text,   font(GEORGIA, 74),        time_fill, 30),
        (args.price,  font(GEORGIA_BOLD, 74),   RED,   48),
        (args.venue,  font(GEORGIA_BOLD, 72),   INK,   16),
        (args.city,   font(GEORGIA, 54),        STEEL, 44),
        (args.note,   font(GEORGIA_ITALIC, 50), STEEL, 40),
    ]
    footer_f = font(GEORGIA_BOLD, 60)
    footer = f"{args.phone}   ·   {args.url}"

    block_h = sum(th(d, t, f) + gap for t, f, _, gap in lines)
    block_h += 7 + 40 + th(d, footer, footer_f)          # rule + gap + footer
    bottom_start = H - MARGIN - block_h

    # ---- illustration fills the space between ----------------------
    art = trim(normalize_white(Image.open(args.art).convert("RGB")))
    avail_h = bottom_start - top_end - 60
    avail_w = W - 2 * MARGIN
    scale = min(avail_w / art.width, avail_h / art.height)
    art = art.resize((max(1, round(art.width * scale)),
                      max(1, round(art.height * scale))), Image.LANCZOS)
    art = feather(art, args.feather)
    canvas.paste(art, ((W - art.width) // 2,
                       top_end + (avail_h - art.height) // 2))

    # ---- draw the bottom block -------------------------------------
    y = bottom_start
    for text, f, fill, gap in lines:
        y = center(d, y, text, f, fill) + gap
    y = rule(d, y, width=300, height=7) + 40
    center(d, y, footer, footer_f, INK)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    canvas.save(args.out, dpi=(DPI, DPI))
    print(f"Saved {args.out}  {canvas.size} @ {DPI}dpi")
    if args.pdf:
        pdf = os.path.splitext(args.out)[0] + ".pdf"
        canvas.save(pdf, "PDF", resolution=DPI)
        print(f"Saved {pdf}")


if __name__ == "__main__":
    main()
