import os
import random

from PIL import Image, ImageDraw, ImageFont

ememe = os.listdir('ememe')


def make_ememe(top_text='', bottom_text=''):
    id = random.randint(0, len(ememe))
    template = Image.open('ememe/' + ememe[id])
    font_size = 70
    w, h = template.size
    font = ImageFont.truetype('impact.ttf', size=font_size)
    canvas = ImageDraw.Draw(template)
    bb_top = canvas.textbbox((0, 0), top_text, font=font)
    bb_bot = canvas.textbbox((0, 0), bottom_text, font=font)
    canvas.text(((w - bb_top[2]) // 2, 0), top_text, font=font, stroke_fill='black', stroke_width=4)
    canvas.text(((w - bb_bot[2]) // 2, h - bb_bot[3] - 10), bottom_text, font=font, stroke_fill='black', stroke_width=4)
    template.save('tempememe.png')
