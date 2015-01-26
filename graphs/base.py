#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from Image import new, ANTIALIAS
from ImageDraw import Draw
from ImageFont import truetype

LIGHT_GREY  = (162,162,162)
LIGHT_GREEN = (59, 255, 134)
DARK_RED    = (255, 59, 59)

class BaseGraph(object):
    def __init__(self, width, height):
        self.image = new("RGB", (width * 10, height * 10), "white")

    def draw_line(self, start, end, colour=DARK_RED, width=1):
        cursor = Draw(self.image)
        cursor.line([start, end], fill=colour, width=width)

    def draw_circle(self, (x,y), r, colour=DARK_RED):
        cursor = Draw(self.image)
        cursor.ellipse((x-r, y-r, x+r, y+r), fill=colour)

    def save(self, filename, filetype="PNG"):
        x, y = self.image.size

        resized_img = self.image.resize((x / 10, y / 10), ANTIALIAS)
        resized_img.save(filename, filetype)