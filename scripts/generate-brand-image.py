#!/usr/bin/env python
"""
Generate a brand-consistent Dance On Time illustration with the Google Gemini
image API ("nano banana"), conditioned on the canonical reference PNGs.

Usage (from the repo root):
    python scripts/generate-brand-image.py \
        --subject "a Bachata couple in a close embrace, slow sensual side-to-side sway" \
        --out images/illustrations/bachata.png

Key (never commit it) is read from, in order:
    1) --key-file PATH
    2) $GEMINI_API_KEY environment variable

See docs/brand-image-generation-guide.md for the full guide, prompt template,
subject recipes, sizes, and troubleshooting.
"""
import argparse, base64, io, json, os, sys, urllib.request, urllib.error
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = "gemini-2.5-flash-image"

# The three canonical illustrations = the ONLY style reference that matters.
DEFAULT_REFS = [
    "images/illustrations/country-swing.png",
    "images/illustrations/bride-groom.png",
    "images/illustrations/dance-party.png",
]

# Fixed brand rules, distilled from docs/illustration-style-guide.md. These are
# prepended to every generation; the caller supplies only the --subject.
STYLE_RULES = (
    "STYLE RULES (match the three reference images EXACTLY): warm near-black tapered ink line "
    "(thicker outer contour, thin interior folds), confident and smooth, no sketchy multi-strokes; "
    "pure white background; skin is left WHITE with an outline, NEVER a flesh tone; soft warm-gray "
    "shading only for fold/volume and a soft light-gray floor-shadow ellipse under each figure - every "
    "shadow is NEUTRAL GRAY, never warm, beige, tan, cream or sepia. "
    "EXACTLY ONE saturated color in the entire image: red #e5261f, and it is used sparingly. "
    "ONLY ONE PERSON in the whole image wears an all-red dress: the single hero/lead woman (her "
    "flaring knee-length red dress, and only she may have red hair). VARY the red dress SILHOUETTE to "
    "suit the dance instead of defaulting to the same polka-dot swing dress every time - e.g. a "
    "polka-dot swing dress with petticoat, a sleek disco wrap, a fringed Latin dress, a full ballroom "
    "gown, a slit sheath, an A-line midi - varying neckline, sleeve and hem too. Every OTHER figure is grayscale "
    "- additional/background women wear white, light-gray or black dresses (NEVER red) with at most "
    "one tiny red accent (a belt, hair ribbon, or small flower); every man is fully grayscale (white "
    "or light-gray shirt, gray trousers, black belt, black shoes, black hair) with at most a small red "
    "tie or bowtie. Small red accents on a few figures are fine, but there must be exactly ONE full red "
    "dress in the image - never multiple women in red. ABSOLUTELY NO blue, green, yellow, brown, or any "
    "other hue anywhere; no gradients-as-style, no neon. "
    "When several people appear, they are ALL adults aged roughly 25-65 (no children, no elderly) with "
    "the SAME neutral white skin (outline only, NO skin-tone shading and no dark skin) - make them read "
    "as distinct individuals through SUBTLE variety ONLY: different hairstyles, hair colour (black or "
    "grey), outfit cut, build/height and dance style, NEVER through skin tone or extreme age. "
    "Keep a roughly BALANCED ~50/50 mix of men and women across the whole cast - never all one gender. "
    "EVERY dancer is PARTNERED in a man-and-woman couple - there must be NO solo, single or unpartnered "
    "dancer anywhere, including in the background, so the total number of dancers is always EVEN and "
    "every person visibly has a partner. Each couple is in a clean CONNECTED frame where the joined "
    "hands actually meet in a proper handhold and the embracing hand lands on the partner - NO tangled, "
    "floating or weirdly overlapping hands. "
    "Natural adult proportions ~7.5 heads tall (never chibi, never big-head); faces in a gentle 3/4 "
    "profile toward each other with tiny simple features, a small nose, a small warm closed smile, and "
    "a few freckle dots on the cheek (freckles are a signature - include them); articulated hands with "
    "real fingers in a genuine handhold; real footwear - default to elegant heels "
    "for women and dress shoes for men; reserve cowboy boots/hats ONLY for explicitly country/western "
    "themes; a couple of small tapered motion swooshes beside the moving skirt/limb. "
    "Faint pale-gray (#e8e8e8) thin-line room props BEHIND the figures: a snake plant lower-left, a "
    "small framed landscape picture upper-right, tiny wall brackets, and a few horizontal floorboard "
    "lines - props never compete with the figures. Figures large and centered, feet in the lower third, "
    "comfortable headroom."
)

PROMPT_TEMPLATE = (
    "Create a NEW clean hand-inked line-art illustration of {subject}, in the EXACT same art style, "
    "palette, line quality and proportions as the three reference images provided. {style_rules} "
    "Output a single {aspect} illustration that looks like it belongs in the same set as the references."
)


def load_key(key_file):
    if key_file:
        return open(key_file, encoding="utf-8").read().strip()
    env = os.environ.get("GEMINI_API_KEY")
    if env:
        return env.strip()
    sys.exit("No API key. Pass --key-file PATH or set GEMINI_API_KEY. See "
             "docs/brand-image-generation-guide.md.")


def enc(path, maxdim=1024):
    im = Image.open(path).convert("RGB")
    if max(im.size) > maxdim:
        r = maxdim / max(im.size)
        im = im.resize((round(im.size[0] * r), round(im.size[1] * r)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return base64.b64encode(buf.getvalue()).decode()


def neutralize_palette(im, chroma_thresh=12, red_margin=25):
    """Force every non-red pixel to neutral gray.

    The brand allows exactly one hue (red #e5261f). The image model
    intermittently returns warm beige/tan floor shadows or other stray tints,
    which silently break that rule. This flattens any off-hue pixel to gray
    while preserving genuine reds (including the darker red dress folds).
    """
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if max(r, g, b) - min(r, g, b) <= chroma_thresh:
                continue                                   # already neutral
            if r > g + red_margin and r > b + red_margin:
                continue                                   # real brand red
            v = (r + g + b) // 3
            px[x, y] = (v, v, v)
    return im


def fit_canvas(src_bytes, size):
    """Fit the generated image onto a white canvas of exactly `size` (w,h),
    preserving aspect ratio so figures are never distorted (background is white,
    so the letterbox is invisible)."""
    im = Image.open(io.BytesIO(src_bytes)).convert("RGB")
    tw, th = size
    r = min(tw / im.size[0], th / im.size[1])
    nw, nh = round(im.size[0] * r), round(im.size[1] * r)
    im = im.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGB", (tw, th), (255, 255, 255))
    canvas.paste(im, ((tw - nw) // 2, (th - nh) // 2))
    return canvas


def main():
    ap = argparse.ArgumentParser(description="Generate a brand-consistent Dance On Time illustration.")
    ap.add_argument("--subject", required=True,
                    help='What to draw, e.g. "a West Coast Swing couple dancing along a straight slot".')
    ap.add_argument("--out", required=True, help="Output path (relative to repo root is fine).")
    ap.add_argument("--aspect", default="3:2 landscape",
                    help='Aspect description for the prompt (default "3:2 landscape").')
    ap.add_argument("--size", default="1200x900",
                    help='Final canvas WxH, fit-on-white. Use "none" to keep the raw API output. '
                         'Web=1200x900, Instagram=1080x1080, FB event=1920x1005.')
    ap.add_argument("--refs", nargs="*", default=DEFAULT_REFS,
                    help="Reference image paths (default: the 3 canonical PNGs).")
    ap.add_argument("--key-file", help="Path to a file containing only the Gemini API key.")
    ap.add_argument("--no-neutralize", action="store_true",
                    help="Skip the palette guard that flattens stray non-red tints (e.g. beige "
                         "floor shadows) to neutral gray.")
    args = ap.parse_args()

    key = load_key(args.key_file)
    prompt = PROMPT_TEMPLATE.format(subject=args.subject, style_rules=STYLE_RULES, aspect=args.aspect)

    parts = [{"text": prompt}]
    for ref in args.refs:
        p = ref if os.path.isabs(ref) else os.path.join(REPO, ref)
        parts.append({"inline_data": {"mime_type": "image/png", "data": enc(p)}})

    body = {"contents": [{"parts": parts}], "generationConfig": {"responseModalities": ["IMAGE"]}}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key}, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            resp = json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:1500]
        if e.code == 429 and "free_tier" in detail:
            sys.exit("HTTP 429: the Gemini image model needs a BILLING-ENABLED Google project "
                     "(free tier = limit 0). Enable billing in AI Studio / Cloud Console, then retry.\n" + detail)
        sys.exit(f"HTTP {e.code}\n{detail}")

    out_bytes = None
    for cand in resp.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            d = part.get("inlineData") or part.get("inline_data")
            if d and d.get("data"):
                out_bytes = base64.b64decode(d["data"])
                break
        if out_bytes:
            break
    if not out_bytes:
        sys.exit("No image returned. Full response:\n" + json.dumps(resp)[:1500])

    dest = args.out if os.path.isabs(args.out) else os.path.join(REPO, args.out)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if args.size.lower() == "none":
        final = Image.open(io.BytesIO(out_bytes)).convert("RGB")
    else:
        w, h = (int(x) for x in args.size.lower().split("x"))
        final = fit_canvas(out_bytes, (w, h))
    if not args.no_neutralize:
        final = neutralize_palette(final)
    final.save(dest)
    print(f"Saved {dest}  {final.size}")


if __name__ == "__main__":
    main()
