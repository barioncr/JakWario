import os
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageColor


def clip(data, d_min, d_max):
    if data > d_max:
        return d_max
    elif data < d_min:
        return d_min


def fit_to_bounding_box(text, target, font_family):
    font_size = 200
    font = ImageFont.truetype(font_family, font_size)

    image = Image.new('RGB', target, color='white')
    draw = ImageDraw.Draw(image)

    while True:
        text_dimensions = draw.multiline_textbbox((0, 0), text, font=font)[2:]
        if text_dimensions[0] < target[0] and text_dimensions[1] < target[1]:
            break
        font_size -= 2
        font = ImageFont.truetype(font_family, font_size)

    return font_size, text_dimensions


def make_meme(top_text='', bottom_text='', meme_dir='hmeme'):
    wrap_width = 60
    # load meme shappen watermark
    watermark = Image.open('MemesHappen.png')
    # load template from folder
    try:
        memefile = random.choice(os.listdir(meme_dir))
        print(f'Using {memefile} as a template')
        template = Image.open(meme_dir + '/' + memefile).convert('RGB')
    except Exception as e:
        print(e)
        template = Image.open('hmeme' + '/' + '2717 - 20151115_223544.jpg')

    # get width and height of the template
    w, h = template.size

    # wrap top or bottom text if necessary
    if len(top_text) > wrap_width:
        top_text = textwrap.fill(top_text, width=wrap_width)
        font_size_top = clip((w * 2) // (wrap_width + 5), h * 0.01, h * 0.2)
    else:
        font_size_top = clip((w * 2) // (len(top_text) + 5), h * 0.01, h * 0.2)

    if len(bottom_text) > wrap_width:
        bottom_text = textwrap.fill(bottom_text, width=wrap_width)
        font_size_bot = clip((w * 2) // (wrap_width + 1), h * 0.01, h * 0.2)
    else:
        font_size_bot = clip((w * 2) // (len(bottom_text) + 5), h * 0.01, h * 0.2)

    # loading fonts
    font_top = ImageFont.truetype('impact.ttf', size=font_size_top)
    font_bot = ImageFont.truetype('impact.ttf', size=font_size_bot)

    canvas = ImageDraw.Draw(template)

    bb_top = canvas.multiline_textbbox((0, 0), top_text.upper(), font=font_top)
    bb_bot = canvas.multiline_textbbox((0, 0), bottom_text.upper(), font=font_bot)
    canvas.text(((w - bb_top[2]) // 2, 10), top_text.upper(), align='center', font=font_top, stroke_fill='black',
                stroke_width=4)
    canvas.text(((w - bb_bot[2]) // 2, h - (bb_bot[3] * 1.3)), bottom_text.upper(), align='center', font=font_bot,
                stroke_fill='black', stroke_width=4)

    template.paste(watermark, box=(w - 128, h - 42), mask=watermark.getchannel(3))

    template.save('tempememe.png')


def split_text(text: str, text_box_count: int) -> list:
    text_length = len(text)
    if text_box_count <= 0 or text_length == 0:
        return []

    words = text.split(' ')
    word_count = len(words)

    substrings = []

    for i in range(text_box_count):
        substring_words = words[i * word_count // text_box_count: (i + 1) * word_count // text_box_count]
        substring = ' '.join(substring_words)
        substrings.append(substring)

    return substrings


def make_skeleton(image, text_boxes, captions: str):
    fonts = os.listdir('_bafonts')
    colors = tuple(ImageColor.colormap.keys())

    skeleton_image = Image.open(image)
    canvas = ImageDraw.Draw(skeleton_image)

    captions = split_text(captions, len(text_boxes))

    for bar, box in zip(captions, text_boxes):
        font_family = '_bafonts/' + random.choice(fonts)

        bounds = ((box[2] - box[0]) * (box[3] - box[1]) // len(bar)) ** 0.5

        wrap_width = max(bounds, 5)
        bar = textwrap.fill(bar, wrap_width)
        font_size, bb = fit_to_bounding_box(bar, (box[2] - box[0], box[3] - box[1]), font_family)
        canvas.text(
            (box[0], box[1]), bar, font=ImageFont.truetype(font_family, size=font_size),
            fill=random.choice(colors), stroke_fill=random.choice(colors), stroke_width=2,
            align='center'
        )

    skeleton_image.save("skeletal.png")
    skeleton_image.close()


class SkeletonTemplate:
    fonts = os.listdir('_bafonts')
    colors_1 = list(ImageColor.colormap.keys())

    def __init__(self, img, boxes):
        self.image = img
        self.text_boxes = boxes

    def add_captions(self, captions: str):
        skeleton_image = Image.open(self.image)
        canvas = ImageDraw.Draw(skeleton_image)

        captions = split_text(captions, len(self.text_boxes))

        for bar, box in zip(captions, self.text_boxes):
            font_family = '_bafonts/' + random.choice(self.fonts)

            symbol_width = int((((box[2] - box[0]) * (box[3] - box[1])) // len(bar) // 2) ** 0.5)
            lines_count = (box[3] - box[1]) // (symbol_width * 2)

            print(symbol_width)
            wrap_width = max(len(bar) // lines_count, 5)
            bar = textwrap.fill(bar, wrap_width)

            font_size, bb = fit_to_bounding_box(bar, (box[2] - box[0], box[3] - box[1]), font_family)
            canvas.text(
                (box[0], box[1]), bar, font=ImageFont.truetype(font_family, size=font_size),
                fill=random.choice(self.colors_1), stroke_fill=random.choice(self.colors_1), stroke_width=2,
                align='center'
            )

        skeleton_image.save("skeletal.png")
        skeleton_image.close()


# skele_01 = SkeletonTemplate(
#     Image.open('_batemplates/skele_01.jpg'),
#     ((190, 280),)
# )
#
skele_02 = SkeletonTemplate(
    '_batemplates/skele_02.jpg',
    ((190, 280),)
)

skele_03 = SkeletonTemplate(
    '_batemplates/skele_03.jpg',
    ((20, 350, 420, 870), (500, 500, 890, 880))
)

skele_05 = SkeletonTemplate(
    '_batemplates/skele_05.jpg',
    ((30, 200, 460, 560),)
)

skeletons = (skele_03, skele_05)
