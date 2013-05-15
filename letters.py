#!/usr/env/bin python

"""Data to define simple block letters """
# Definitely not the most efficient path to draw a particular letter,
# but I found these pleasing to watch being drawn
# pen down the entire path (might retrace part of path)
# Unit height of 1
# smallest detail is 0.125 (1/8)
# 90 or 45 degree turns
letters_data = {
    'A': ((0.0, 0.0), (0.5, 1.0), (0.75, 0.5), (0.25, 0.5),
    (0.75, 0.5), (1.0, 0.0)),
    'B': ((0.0, 0.0), (0.0, 1.0), (0.625 ,1.0), (0.75, 0.875), 
    (0.75, 0.625), (0.625, 0.5), (0.0, 0.5), (0.625, 0.5),
    (0.75, 0.375), (0.75, 0.125), (0.625, 0.0), (0.0, 0.0)),
    'C': ((0, 0.125), (-0.125, 0),(-0.625, 0),(-0.75, 0.125),
    (-0.75, 0.875), (-0.625, 1), (-0.125, 1), (0, 0.875)),
    'D': ((0.0, 0.0), (0.0, 1.0), (0.625 ,1.0), (0.75, 0.875), 
    (0.75, 0.125), (0.625, 0.0), (0.0, 0.0)),
    'E': ((0, 0), (-0.75, 0), (-0.75, 0.5), (0, 0.5), (-0.75, 0.5),
    (-0.75, 1), (0, 1)),
    'F': ((0,0), (0, 0.5), (0.75, 0.5), (0, 0.5), (0, 1), (0.75, 1)),
    'G': ((0, 0.5), (-0.125, 0.5), (0, 0.5), (0, 0.125), (-0.125, 0),
    (-0.625, 0), (-0.75, 0.125), (-0.75, 0.875), (-0.625, 1), 
    (-0.125, 1), (0, 0.875)),
    'H': ((0, 0), (0, 1), (0, 0.5), (0.75, 0.5), (0.75, 1), (0.75, 0)),
    'I': ((0, 0), (0.25, 0), (0.125, 0), (0.125, 1), (0, 1), (0.25, 1)),
    'J': ((0, 0.125), (0.125, 0), (0.375, 0), (0.5, 0.125), (0.5, 1)),
    'K': ((0, 0), (0, 1), (0, 0.5), (0.75, 1), (0, 0.5), (0.75, 0)),
    'L': ((0, 0), (0, 1), (0, 0), (0.75, 0)),
    'M': ((0, 0), (0, 1), (0.5, 0), (1, 1), (1,0)),
    'N': ((0, 0), (0, 1), (0.75, 0), (0.75, 1)),
    'O': ((0, 0.125), (-0.125, 0), (-0.625, 0), (-0.75, 0.125), 
    (-0.75, 0.875), (-0.625, 1), 
    (-0.125, 1), (0, 0.875), (0, 0.125)),
    'P': ((0, 0), (0, 1), (0.625, 1), (0.75, 0.875), (0.75, 0.625),
    (0.625, 0.5), (0, 0.5)),
    'Q': ((0, 0.125), (-0.125, 0), (-0.625, 0), (-0.75, 0.125), 
    (-0.75, 0.875), (-0.625, 1), 
    (-0.125, 1), (0, 0.875), (0, 0.125), (0.125, 0)),
    'R': ((0, 0), (0, 1), (0.625, 1), (0.75, 0.875), (0.75, 0.625),
    (0.625, 0.5), (0, 0.5),(0.625, 0.5), (0.875, 0)),
    'S': ((0, 0.125), (0.125, 0), (0.625, 0), (0.75, 0.125),
    (0.75, 0.375), (0.675, 0.5), (0.125, 0.5), (0, 0.625),
    (0, 0.875), (0.125, 1), (0.625, 1), (0.75, 0.875)),
    'T': ((0, 1), (0.5, 1), (0.5, 0), (0.5, 1), (1,1)),
    'U': ((0, 1), (0, 0.125), (0.125, 0), (0.625, 0),
    (0.75, 0.125), (0.75, 1)),
    'V': ((0, 1), (0.375, 0), (0.75, 1)),
    'W': ((0, 1), (0.25, 0), (0.5, 1), (0.75, 0), (1, 1)),
    'X': ((0, 0), (0.375, 0.5), (0, 1), (0.375, 0.5), (0.75, 1),
    (0.375, 0.5), (0.75, 0)),
    'Y': ((0, 1), (0.375, 0.5), (0.375, 0), (0.375, 0.5), (0.75, 1)),
    'Z': ((0, 1), (0.75, 1), (0, 0), (0.75, 0)),
    # the space character is the one exception to the pen down path rule
    ' ': ((0, 0), (0.625, 0)),
}


class Letter(object):
    """Define a "letter" with data and methods to help draw it """
    def __init__(self, letter, height=None):
        self.letter = letter
        # the space character is the one exception to the pen down path
        # rule, so make an attribute available to identify it
        self.is_space = True if letter == ' ' else False
        self.data = letters_data[letter]
        if height is None:
            height = 50
        self.height = height
        # letter definitions may or may not start at (0, 0),
        # and have variable width,
        # so it is useful to have the "left" and "right" edges
        # and width readily available
        self.x_max = max([p[0] for p in self.data])
        self.x_min = min([p[0] for p in self.data])
        self.unit_width = self.x_max - self.x_min
        self.unit_start_position = self.data[0]


    def get_width(self, height=None):
        """Get the letter width
        allows "height" to be temporarily set """
        if height is None:
            height = self.height
        return self.unit_width * height


    def get_start_delta(self, height=None):
        """Get the position to start drawing the letter
        allows "height" to be temporarily set """
        if height is None:
            height = self.height
        return -self.x_min * height, self.data[0][1] * height


    def get_delta_left(self, height=None):
        """Get the distance for the starting point to the left-hand edge 
        (a positive value, even if in the -X direction)"""
        if height is None:
            height = self.height
        return self.data[0][0] - self.x_min * height


def text_width(text, height=50, spacing=None):
    """Get the width that text will be in Turtle units
    Might be useful for planning ahead if thing will fit"""
    if spacing == None:
        spacing = height * 0.3
    w = 0
    for c in filtered_letter_objects(text):
        w += c.get_width(height) + spacing
    w -= spacing
    return w


def filtered_chars_from_text(text):
    """Filter characters to those that are defined """
    chars = []
    for c in text:
        # just skip any characters that are not defined
        if c.upper() in letters_data:
            chars.append(c.upper())
    return chars


def filtered_letter_objects(text):
    """Letter objects from "filtered" text (characters that are defined) """
    chars = filtered_chars_from_text(text)
    letter_objects = map(Letter, [c for c in chars])
    return letter_objects

