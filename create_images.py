"""
generate_images.py
------------------
Generates all artwork for Space Flappy using Pillow.

Assets created:
  - background.png   : Deep-space starfield with nebula
  - rocket.png       : Player rocket ship sprite
  - asteroid_top.png : Top asteroid obstacle
  - asteroid_bot.png : Bottom asteroid obstacle
  - icon.png         : Window icon
"""

import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ── reproducible randomness ──────────────────────────────────────────────────
random.seed(42)

# ── constants ────────────────────────────────────────────────────────────────
OUT = "images"
BG_W, BG_H = 360, 640
ROCKET_W, ROCKET_H = 40, 56
AST_W, AST_H = 80, 600


# ── helpers ──────────────────────────────────────────────────────────────────
def save(img: Image.Image, name: str) -> None:
    """Save *img* to OUT/<name> and print confirmation."""
    path = f"{OUT}/{name}"
    img.save(path)
    print(f"  ✓  {path}  ({img.size[0]}×{img.size[1]})")


# ── background ───────────────────────────────────────────────────────────────
def make_background() -> Image.Image:
    """
    Create a deep-space background:
      1. Dark gradient base (top = near-black navy, bottom = deep purple)
      2. ~350 stars of varying brightness
      3. A soft cyan/purple nebula blurred over the midfield
    """
    img = Image.new("RGB", (BG_W, BG_H))
    draw = ImageDraw.Draw(img)

    # gradient rows
    for y in range(BG_H):
        t = y / BG_H
        r = int(2 + t * 20)
        g = int(0 + t * 5)
        b = int(30 + t * 40)
        draw.line([(0, y), (BG_W, y)], fill=(r, g, b))

    # nebula (separate layer, blurred then composited)
    nebula = Image.new("RGB", (BG_W, BG_H), (0, 0, 0))
    nd = ImageDraw.Draw(nebula)
    for _ in range(12):
        cx = random.randint(40, BG_W - 40)
        cy = random.randint(80, BG_H - 80)
        rx = random.randint(30, 90)
        ry = random.randint(20, 60)
        col = random.choice([
            (60, 0, 120), (0, 60, 120), (80, 0, 80),
            (0, 80, 100), (40, 0, 90),
        ])
        nd.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=col)
    nebula = nebula.filter(ImageFilter.GaussianBlur(radius=28))
    img = Image.blend(img, nebula, alpha=0.45)

    # stars
    draw2 = ImageDraw.Draw(img)
    for _ in range(350):
        sx = random.randint(0, BG_W - 1)
        sy = random.randint(0, BG_H - 1)
        bright = random.randint(160, 255)
        r_px = random.choice([0, 0, 0, 1])
        if r_px == 0:
            draw2.point((sx, sy), fill=(bright, bright, bright))
        else:
            draw2.ellipse(
                [sx - r_px, sy - r_px, sx + r_px, sy + r_px],
                fill=(bright, bright, bright),
            )

    # subtle planet in lower-right
    pd = ImageDraw.Draw(img)
    px, py, pr = 300, 520, 45
    for ring in range(pr, 0, -1):
        t2 = ring / pr
        rc = int(80 * t2 + 20 * (1 - t2))
        gc = int(40 * t2 + 10 * (1 - t2))
        bc = int(100 * t2 + 60 * (1 - t2))
        pd.ellipse(
            [px - ring, py - ring, px + ring, py + ring],
            fill=(rc, gc, bc),
        )
    # planet rings
    pd.arc([px - 65, py - 12, px + 65, py + 12], start=0, end=180, fill=(180, 160, 220), width=3)

    return img


# ── rocket ───────────────────────────────────────────────────────────────────
def make_rocket() -> Image.Image:
    """
    Draw a top-down rocket sprite with:
      - Silver/white fuselage body
      - Red nose cone
      - Blue engine exhaust glow
      - Yellow flame trail at the bottom
    """
    img = Image.new("RGBA", (ROCKET_W, ROCKET_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = ROCKET_W // 2

    # engine flame (bottom)
    for i, col in enumerate([(255, 200, 50, 180), (255, 130, 0, 140), (255, 80, 0, 80)]):
        fw = 10 - i * 2
        fh = 14 - i * 3
        fy = ROCKET_H - fh - i * 2
        draw.ellipse([cx - fw, fy, cx + fw, fy + fh + 6], fill=col)

    # engine nozzle
    draw.rounded_rectangle([cx - 8, ROCKET_H - 20, cx + 8, ROCKET_H - 8], radius=3, fill=(90, 90, 110))

    # fuselage
    body_top = 14
    body_bot = ROCKET_H - 20
    draw.rounded_rectangle(
        [cx - 10, body_top, cx + 10, body_bot],
        radius=8,
        fill=(220, 225, 235),
        outline=(140, 145, 160),
        width=1,
    )

    # fuselage stripe
    stripe_y = (body_top + body_bot) // 2
    draw.line([(cx - 9, stripe_y), (cx + 9, stripe_y)], fill=(80, 130, 200), width=3)

    # side fins
    for sign in (-1, 1):
        fx_inner = cx + sign * 10
        fx_outer = cx + sign * 20
        fin_top = ROCKET_H - 36
        fin_bot = ROCKET_H - 14
        draw.polygon(
            [(fx_inner, fin_top), (fx_outer, fin_bot), (fx_inner, fin_bot)],
            fill=(200, 50, 50),
            outline=(160, 30, 30),
        )

    # nose cone
    cone_pts = [
        (cx, 0),
        (cx - 10, body_top + 4),
        (cx + 10, body_top + 4),
    ]
    draw.polygon(cone_pts, fill=(220, 60, 60), outline=(170, 30, 30))

    # cockpit window
    draw.ellipse([cx - 5, body_top + 8, cx + 5, body_top + 18], fill=(100, 180, 255, 200), outline=(60, 120, 200))

    return img


# ── asteroid pipe ────────────────────────────────────────────────────────────
def make_asteroid_pipe(flipped: bool = False) -> Image.Image:
    """
    Build a rocky asteroid column obstacle (replaces the green pipe).
    Parameters
    ----------
    flipped : bool
        If True the jagged opening faces downward (top pipe).
        If False the jagged opening faces upward (bottom pipe).
    """
    img = Image.new("RGBA", (AST_W, AST_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # base rock colour with darker edges
    for x in range(AST_W):
        t = abs(x - AST_W / 2) / (AST_W / 2)
        r = int(90 - t * 30)
        g = int(80 - t * 25)
        b = int(75 - t * 25)
        draw.line([(x, 0), (x, AST_H)], fill=(r, g, b))

    # surface craters
    random.seed(7 + int(flipped))
    for _ in range(18):
        cx2 = random.randint(8, AST_W - 8)
        cy2 = random.randint(8, AST_H - 8)
        cr = random.randint(4, 14)
        draw.ellipse(
            [cx2 - cr, cy2 - cr, cx2 + cr, cy2 + cr],
            fill=(60, 55, 50),
            outline=(40, 35, 30),
        )
        # highlight rim
        draw.arc(
            [cx2 - cr, cy2 - cr, cx2 + cr, cy2 + cr],
            start=200,
            end=320,
            fill=(120, 110, 100),
            width=2,
        )

    # jagged edge (the opening side)
    edge_y = 0 if flipped else AST_H
    num_teeth = 9
    tooth_h = 18
    xs = [round(i * AST_W / num_teeth) for i in range(num_teeth + 1)]
    for i in range(num_teeth):
        mid_x = (xs[i] + xs[i + 1]) // 2
        if flipped:
            pts = [(xs[i], 0), (mid_x, tooth_h), (xs[i + 1], 0)]
        else:
            pts = [(xs[i], AST_H), (mid_x, AST_H - tooth_h), (xs[i + 1], AST_H)]
        draw.polygon(pts, fill=(100, 90, 85))

    # edge glow
    glow_col = (180, 120, 60, 80)
    for k in range(6):
        gy = k if flipped else AST_H - k
        alpha = 80 - k * 12
        draw.line([(0, gy), (AST_W, gy)], fill=(200, 140, 80, max(alpha, 0)))

    return img


# ── icon ─────────────────────────────────────────────────────────────────────
def make_icon() -> Image.Image:
    """Small 64×64 window icon: rocket on dark background."""
    bg = Image.new("RGBA", (64, 64), (10, 5, 30, 255))
    rocket_small = make_rocket().resize((22, 32), Image.LANCZOS)
    bg.paste(rocket_small, (21, 16), rocket_small)
    return bg


# ── main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating Space Flappy assets …")
    save(make_background(), "background.png")
    save(make_rocket(),     "rocket.png")
    save(make_asteroid_pipe(flipped=True),  "asteroid_top.png")
    save(make_asteroid_pipe(flipped=False), "asteroid_bot.png")
    save(make_icon(),       "icon.png")
    print("Done — all assets written to images/")
