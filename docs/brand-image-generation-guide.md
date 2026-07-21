# Dance On Time — Brand Image Generation Guide

How to generate **new, brand-consistent illustrations** (any dance style or theme) that look
like they belong with the existing set — using the Google Gemini image API, conditioned on our
three canonical reference illustrations.

> This is the **approved, working method** as of 2026-07-20. It replaced the earlier hand-built
> SVG pipeline (which never got the faces right). The art-direction rules still live in
> [`illustration-style-guide.md`](illustration-style-guide.md); *this* file is the how-to for
> producing finished raster images.

The whole thing is one command:

```bash
python scripts/generate-brand-image.py \
  --subject "a Bachata couple in a close embrace, slow sensual side-to-side sway" \
  --out images/illustrations/bachata.png
```

---

## Why it works

Modern image models can be **conditioned on reference images**. The script sends the API:

1. our three canonical illustrations (`country-swing.png`, `bride-groom.png`, `dance-party.png`)
   as inline reference images, **plus**
2. a fixed block of brand **style rules** (palette, line, proportions, props), **plus**
3. the one thing that changes per image: your **`--subject`** line.

Feeding the real illustrations as references is what finally nailed the faces, proportions,
palette, and props that every from-scratch attempt missed. Keep those three PNGs in the repo —
they *are* the style.

---

## One-time setup

1. **Get a Google AI Studio API key** — <https://aistudio.google.com/apikey>.
2. **Enable billing on that key's project.** The image model ("nano banana",
   `gemini-2.5-flash-image`) is **not** on the free tier — without billing you get
   `HTTP 429, free_tier limit 0`. Cost is tiny: **~$0.04 per generated image.**
3. **Give the script the key without committing it.** Either:
   - set an environment variable: `GEMINI_API_KEY` (PowerShell: `$env:GEMINI_API_KEY="..."`), or
   - save the key to a file and pass `--key-file path\to\key.txt` (keep that file OUT of git —
     e.g. under the temp/scratchpad folder, never inside the repo).
4. Requirements: Python with **Pillow** (already present). No `pip install` and no extra SDK —
   the script uses the standard library for HTTP.

> **Security:** never paste the key into chat or commit it. If it leaks, rotate it in AI Studio.

---

## Usage

```bash
python scripts/generate-brand-image.py --subject "<what to draw>" --out <path> [options]
```

| Option       | Default            | What it does |
|--------------|--------------------|--------------|
| `--subject`  | *(required)*       | The scene to draw. Everything else is fixed brand rules. |
| `--out`      | *(required)*       | Where to save (relative to repo root is fine; dirs auto-created). |
| `--size`     | `1200x900`         | Final canvas `WxH`, fit-on-white (no distortion). `none` keeps the raw API output. |
| `--aspect`   | `3:2 landscape`    | Aspect wording sent to the model. Match it to `--size`. |
| `--refs`     | the 3 canonical PNGs | Override the reference images if you ever need to. |
| `--key-file` | — (uses `$GEMINI_API_KEY`) | Path to a file containing only the key. |

**Output sizes** (set `--size` *and* a matching `--aspect`):

| Use                 | `--size`    | `--aspect`         |
|---------------------|-------------|--------------------|
| Web illustration    | `1200x900`  | `3:2 landscape`    |
| Instagram square    | `1080x1080` | `1:1 square`       |
| Facebook event cover| `1920x1005` | `1.91:1 landscape` |

The generated image rarely comes out at the exact pixel size; the script fits it onto a white
canvas of the requested size, so figures are never stretched (the white letterbox is invisible
on our white backgrounds).

---

## Writing a good `--subject`

Only describe **who is dancing, the pose, and the mood** — do **not** restate colors, line style,
or props (those are already enforced by the built-in rules; repeating them just adds noise).

Good subjects name the dance's *signature look* so the pose is recognizable:

| Dance / theme        | Example `--subject` |
|----------------------|---------------------|
| West Coast Swing     | `a West Coast Swing couple, the woman traveling along a straight "slot" with a connected one-hand lead, cool and controlled posture` |
| East Coast / Lindy   | `a lively East Coast Swing couple mid-swingout, bright bouncy energy, her skirt flaring` |
| Bachata              | `a Bachata couple in a close embrace, slow sensual side-to-side sway, deep knee bend` |
| Salsa                | `a Salsa couple in a fast cross-body lead, her spinning under his raised arm, sharp footwork` |
| Two-step (country)   | `a country two-step couple gliding counter-clockwise, hand-in-hand promenade frame, cowboy hat and boots` |
| Waltz (wedding)      | `a wedding first-dance couple in a closed waltz frame, the bride in a white gown with a veil, one red boutonniere on the groom` |
| Line dance           | `a row of four dancers doing a country line dance in unison, mid-kick, hats and boots` |
| Group / party        | `a lively social dance party with several couples and a DJ at a mixer in the back` |
| Solo instructor      | `a friendly dance instructor demonstrating a step, one arm extended, welcoming` |

Tips:
- Keep it to one or two sentences. Name the **frame/handhold** and the **energy** (smooth vs.
  bouncy vs. sensual) — that's what distinguishes dances visually.
- For weddings, say "bride in white gown / groom with red boutonniere" so the red lands there.
- Generate a couple of takes and pick the best — each run is ~4 cents.

---

## The prompt template (for reference / manual use)

The script builds this automatically. It's here so you can also paste it into AI Studio by hand,
or audit exactly what's sent. `{style_rules}` is the fixed block; you fill `{subject}`/`{aspect}`.

```
Create a NEW clean hand-inked line-art illustration of {subject}, in the EXACT same art style,
palette, line quality and proportions as the three reference images provided. {style_rules}
Output a single {aspect} illustration that looks like it belongs in the same set as the references.
```

`{style_rules}` (the enforced brand block):

> STYLE RULES (match the three reference images EXACTLY): warm near-black tapered ink line
> (thicker outer contour, thin interior folds), confident and smooth, no sketchy multi-strokes;
> pure white background; skin is left WHITE with an outline, NEVER a flesh tone; soft warm-gray
> shading only for fold/volume and a soft light-gray floor-shadow ellipse under each figure.
> EXACTLY ONE saturated color in the entire image: red #e5261f, and it is used sparingly.
> ONLY ONE PERSON in the whole image wears an all-red dress: the single hero/lead woman (her
> flaring knee-length red dress, and only she may have red hair). Every OTHER figure is grayscale -
> additional/background women wear white, light-gray or black dresses (NEVER red) with at most one
> tiny red accent (a belt, hair ribbon, or small flower); every man is fully grayscale (white or
> light-gray shirt, gray trousers, black belt, black shoes, black hair) with at most a small red tie
> or bowtie. Small red accents on a few figures are fine, but there must be exactly ONE full red dress
> in the image - never multiple women in red. ABSOLUTELY NO blue, green, yellow, brown, or any other
> hue anywhere; no gradients-as-style, no neon.
> When several people appear, they are ALL adults aged roughly 25-65 (no children, no elderly) with
> the SAME neutral white skin (outline only, NO skin-tone shading and no dark skin) - make them read as
> distinct individuals through SUBTLE variety ONLY: different hairstyles, hair colour (black or grey),
> outfit cut, build/height and dance style, NEVER through skin tone or extreme age.
> Keep a roughly BALANCED ~50/50 mix of men and women across the whole cast - never all one gender;
> pair dancers as man-and-woman couples in clean CONNECTED frames where the joined hands actually meet
> in a proper handhold and the embracing hand lands on the partner - NO tangled, floating or weirdly
> overlapping hands.
> Natural adult proportions ~7.5 heads tall (never chibi, never big-head); faces in a gentle 3/4
> profile toward each other with tiny simple features, a small nose, a small warm closed smile, and
> a few freckle dots on the cheek (freckles are a signature - include them); articulated hands with
> real fingers in a genuine handhold; real footwear - default to elegant heels for women and dress
> shoes for men, reserve cowboy boots/hats ONLY for explicitly country/western themes; a couple of
> small tapered motion swooshes beside the moving skirt/limb.
> Faint pale-gray (#e8e8e8) thin-line room props BEHIND the figures: a snake plant lower-left, a
> small framed landscape picture upper-right, tiny wall brackets, and a few horizontal floorboard
> lines - props never compete with the figures. Figures large and centered, feet in the lower third,
> comfortable headroom.

To tune the brand rules for everyone, edit `STYLE_RULES` in
[`scripts/generate-brand-image.py`](../scripts/generate-brand-image.py) — one place, all images.

---

## The "Dance On Time" wordmark (fixed — use it consistently)

Whenever the business name is set as text on an image, colour it the **same way every time**:

- **"Dance"** — ink `#2f2f41` (dark grey/near-black)
- **"On"** — red `#e5261f`  ← the red word is always **On**
- **"Time"** — ink `#2f2f41`

So: **<span>Dance</span> <span style="color:#e5261f">On</span> <span>Time</span>** — only the middle
word "On" is red; "Dance" and "Time" are dark. Set in the Playfair Display / Georgia-Bold serif,
optionally with a short red rule beneath. Do **not** put the red on "Dance" or "Time", and don't
recolour the whole name red. This wordmark colouring is baked into the title code in
[`scripts/generate-brand-image.py`](../scripts/generate-brand-image.py) / the cover compositing step.

---

## Pre-ship brand checklist

Eyeball every generated image against this before saving it as final:

1. **Exactly one** saturated color, and it's `#e5261f` (dress / lead's hair / a tie / checker floor)?
2. **Only ONE person in an all-red dress** (the hero woman) — no crowd of duplicate red dresses;
   other women in white/gray/black with at most a tiny red accent? (Override only if you asked for more.)
4. Skin left white for **everyone** (no flesh tones, no dark skin); adults 25–65 only; crowd variety is
   subtle (hairstyle / outfit / build / dance style), not skin tone or extreme age? Men black-haired & grayscale?
   Roughly **~50/50 men and women** (not all one gender), hands connecting cleanly (no tangled/floating hands)?
5. Tapered line weight; soft gray fold-shading; a soft gray floor-shadow under each figure?
6. ¾-profile faces with tiny features **and freckles**?
7. Natural ~7.5-head proportions; articulated hands; real footwear; feet grounded?
8. At least two faint gray room props behind (plant / framed picture / brackets / floorboards)?
9. Motion swooshes on the moving parts?
10. Sit it beside the three canonical PNGs — does it read as a **fourth in the set**?
11. If the name is on it: **"Dance" + "Time" dark, "On" red** — only the middle word is red?

If something's off (extra color, weird hands, wrong pose), just regenerate — it's cheap, and each
run varies. Adjust the `--subject` for pose problems; edit `STYLE_RULES` for systemic ones.

---

## Troubleshooting

| Symptom | Cause / fix |
|---------|-------------|
| `HTTP 429 ... free_tier ... limit: 0` | Billing not enabled on the key's project. Enable it; the model isn't free. |
| `No API key` | Set `GEMINI_API_KEY` or pass `--key-file`. |
| `No image returned` | The model returned text/safety only. Re-run, or simplify the `--subject`. |
| A second color sneaks in (blue jeans, brown hair) | Regenerate; if it recurs, strengthen the "NO other hue" line in `STYLE_RULES`. |
| Faces/hands look off | Regenerate (variance is high); keep all 3 references attached — they anchor anatomy. |
| Pose doesn't read as the dance | Name the signature frame/handhold and energy in `--subject` (see the recipe table). |

---

## Files

- [`scripts/generate-brand-image.py`](../scripts/generate-brand-image.py) — the generator.
- [`images/illustrations/{country-swing,bride-groom,dance-party}.png`](../images/illustrations/) —
  the canonical references. **Do not delete or restyle these** — they define the brand.
- [`illustration-style-guide.md`](illustration-style-guide.md) — the underlying art-direction spec.
