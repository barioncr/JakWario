import os
import random

from PIL import Image, ImageDraw, ImageFont

ememe = os.listdir('ememe')
hmeme = os.listdir('hmeme')


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def make_ememe(top_text='', bottom_text=''):
    template = Image.open('hmeme/' + random.choice(hmeme))

    w, h = template.size

    font_size_top = clamp((w + 100) // len(top_text) + 1, h * 0.01, h * 0.2)
    font_size_bot = clamp((w + 100) // len(bottom_text) + 1, h * 0.01, h * 0.2)

    font_top = ImageFont.truetype('impact.ttf', size=font_size_top)
    font_bot = ImageFont.truetype('impact.ttf', size=font_size_bot)
    canvas = ImageDraw.Draw(template)
    bb_top = canvas.textbbox((0, 0), top_text.upper(), font=font_top)
    bb_bot = canvas.textbbox((0, 0), bottom_text.upper(), font=font_bot)
    canvas.text(((w - bb_top[2]) // 2, 0), top_text.upper(), font=font_top, stroke_fill='black', stroke_width=4)
    canvas.text(((w - bb_bot[2]) // 2, h - bb_bot[3] - 10), bottom_text.upper(), font=font_bot, stroke_fill='black', stroke_width=4)
    template.save('tempememe.png')
