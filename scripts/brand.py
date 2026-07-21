"""Shared Dance On Time brand constants for the image tooling.

Single source of truth so the wordmark and palette stay identical across
generate-brand-image.py, add-title.py and make-poster.py.
See docs/brand-image-generation-guide.md.
"""

# Palette
INK = (47, 47, 65)      # #2f2f41
RED = (229, 38, 31)     # #e5261f
STEEL = (92, 90, 90)    # #5c5a5a
WHITE = (255, 255, 255)

# Fonts (Georgia stands in for Playfair Display)
GEORGIA_BOLD = r"C:\Windows\Fonts\georgiab.ttf"
GEORGIA = r"C:\Windows\Fonts\georgia.ttf"
GEORGIA_ITALIC = r"C:\Windows\Fonts\georgiai.ttf"

# The wordmark, split into coloured segments.
# RULE: only the middle word "On" is red; "Dance" and "Time" are ink.
WORDMARK = [("Dance ", INK), ("On ", RED), ("Time", INK)]
