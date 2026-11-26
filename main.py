"""The World in One Day - Thursday 26 November 2026.

Deterministic newspaper-style summary image. All text and geometry are fixed
in this file, so every run produces the same bytes.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

PAPER = (247, 243, 232)
INK = (20, 20, 20)
NAVY = (18, 38, 74)
RED = (178, 34, 34)
TEAL = (0, 105, 110)
OCHRE = (176, 112, 16)
GREEN = (38, 112, 64)
PURPLE = (86, 52, 120)
GREY = (92, 92, 92)
RULE = (196, 188, 168)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def centred(draw, cx, y, text, fnt, fill):
    box = draw.textbbox((0, 0), text, font=fnt)
    draw.text((cx - (box[2] - box[0]) / 2, y), text, font=fnt, fill=fill)


def lines(draw, x, y, rows, fnt, fill, leading):
    for row in rows:
        draw.text((x, y), row, font=fnt, fill=fill)
        y += leading
    return y


def panel(draw, x, y, w, h, colour, kicker, headline, body):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=RULE, width=2)
    draw.rectangle([x, y, x + w, y + 32], fill=colour)
    draw.text((x + 12, y + 7), kicker, font=font(SANS_B, 16), fill=WHITE)
    hy = lines(draw, x + 12, y + 42, headline, font(SERIF_B, 22), INK, 26)
    lines(draw, x + 12, hy + 6, body, font(SANS, 17), (40, 40, 40), 22)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Date strip
    d.rectangle([0, 0, W, 56], fill=INK)
    d.text((36, 14), "THURSDAY 26 NOVEMBER 2026", font=font(SANS_B, 24), fill=WHITE)
    d.text((700, 18), "WORLD NEWS", font=font(SANS_B, 20), fill=(240, 210, 120))

    # Masthead
    centred(d, W // 2, 70, "The World in One Day", font(SERIF_B, 56), INK)
    centred(d, W // 2, 134, "One day of world news, in one image", font(SERIF, 20), GREY)
    d.line([36, 168, 988, 168], fill=INK, width=3)
    d.line([36, 174, 988, 174], fill=RULE, width=1)

    # Lead visual: tariff panel
    d.rectangle([36, 190, 420, 452], fill=NAVY)
    centred(d, 228, 206, "14", font(SERIF_B, 110), WHITE)
    centred(d, 228, 330, "TRADING PARTNERS", font(SANS_B, 24), (240, 210, 120))
    centred(d, 228, 364, "named in the US plan", font(SANS, 18), WHITE)
    for i, tag in enumerate(["CHINA", "EU", "JAPAN", "INDIA"]):
        tx = 58 + i * 92
        d.rounded_rectangle([tx, 404, tx + 80, 434], radius=8, fill=WHITE)
        centred(d, tx + 40, 410, tag, font(SANS_B, 15), NAVY)

    # Lead text
    d.text((444, 190), "TRADE  |  WASHINGTON", font=font(SANS_B, 17), fill=RED)
    lines(d, 444, 216, ["US proposes tariffs", "on 14 partners"],
          font(SERIF_B, 42), INK, 48)
    lines(d, 444, 322, [
        "Plan targets excess capacity;",
        "China faces the top rate. On Thu,",
        "Seoul vowed more talks to",
        "protect its interests.",
    ], font(SANS, 19), (45, 45, 45), 26)
    d.rectangle([444, 434, 700, 468], fill=(255, 244, 214), outline=OCHRE, width=2)
    d.text((456, 441), "Not yet in effect", font=font(SANS_B, 17), fill=INK)
    d.text((714, 441), "Hearing first", font=font(SANS, 17), fill=GREY)

    # Story grid: 3 columns x 2 rows
    gx = [36, 356, 676]
    gy = [486, 692]
    pw, ph = 312, 192
    panel(d, gx[0], gy[0], pw, ph, RED, "ENERGY | MIDDLE EAST",
          ["Oil edges up on", "Hormuz fears"],
          ["Houthis say they hit Saudi",
           "Ras Tanura refinery; Iran",
           "reports ships hit mines.",
           "Brent $94.71 on Thursday."])
    panel(d, gx[1], gy[0], pw, ph, OCHRE, "DISASTER | EGYPT",
          ["Cairo tanker fire", "kills at least 31"],
          ["A fuel tanker crashed on",
           "the ring road on Wed.",
           "Health ministry: 31 dead,",
           "21 injured; toll preliminary."])
    panel(d, gx[2], gy[0], pw, ph, NAVY, "WAR FINANCE | EUROPE",
          ["EU leaders split on", "Ukraine loan"],
          ["At Thu's Brussels summit,",
           "leaders weigh a €45bn loan",
           "for Kyiv in 2027. Four states",
           "object to sharing its cost."])
    panel(d, gx[0], gy[1], pw, ph, GREEN, "HEALTH | DR CONGO",
          ["Ebola cases", "pass 12,000"],
          ["Government data Thu:",
           "12,021 confirmed cases,",
           "5,904 deaths. Second-",
           "largest outbreak on record."])
    panel(d, gx[1], gy[1], pw, ph, TEAL, "SPACE | CHINA-PAKISTAN",
          ["First Pakistani", "aboard Tiangong"],
          ["Muhammad Zeeshan Ali is",
           "the first foreign astronaut",
           "on China's station, after",
           "Shenzhou-24 docked Wed."])
    panel(d, gx[2], gy[1], pw, ph, PURPLE, "LABOUR | BANGLADESH",
          ["Garment pay up 36%,", "deal falls short"],
          ["Minimum rises to 17,000",
           "taka from Dec 1. Advocates",
           "Thu called it short of a",
           "living wage."])

    # Brief strip
    d.rectangle([36, 898, 988, 946], fill=INK)
    d.text((48, 910), "BRIEF  |  NORTH KOREA:", font=font(SANS_B, 17), fill=(240, 210, 120))
    d.text((300, 910), "KCNA Thu: Kim urges wider tactical nuclear deployment",
           font=font(SANS, 17), fill=WHITE)

    # Footer
    d.line([36, 962, 988, 962], fill=RULE, width=1)
    centred(d, W // 2, 970,
            "Sources: Reuters, AP, CNN, European Council, Media Selangor",
            font(SANS, 16), (70, 70, 70))
    centred(d, W // 2, 993,
            "Unconfirmed attack claims are shown as attributed claims, not settled facts",
            font(SANS, 15), (70, 70, 70))

    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    build().save(path, format="PNG")


if __name__ == "__main__":
    main()
