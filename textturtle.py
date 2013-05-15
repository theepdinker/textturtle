#!/usr/env/bin python
"""TextTurtle is a Turtle that can draw text!

Compatible with the Turtle methods that you may be familiar with
(it is a subclass of Turtle), 
but with the additional talent of drawing text.

simple use case:
    from textturtle import TextTurtle
    t = TextTurtle()
    t.text("hello")

The TextTurtle alphabet is uppercase ASCII, plus a space character.
Sorry, no punctuation for emiticons :(

You can use the standard Turtle method write() if you want other 
characters (but then you can't watch the Turtle draw it)
(and I am sure that you are clever enough to add characters with your Turtle!)

"""

import math
import turtle

from letters import filtered_letter_objects, text_width


class TextTurtle(turtle.Turtle):
    """Draw text with a Turtle! """
    def __init__(self, text_height=50, spacing=None, spacing_at_end=False):
        """
        text_height: text height in turtle units
        spacing: space between characters in turtle units,
            default is 0.3 * text_height
        spacing_at_end: 
            default: no spacing included at the end of the text
            If True, spacing is included at the end of the text
            (might be useful if one intends to continue the text
            with another part)
        """
        super(TextTurtle, self).__init__()
        self.text_height = text_height
        self.spacing = spacing
        if spacing is None:
            self.spacing = text_height * 0.3
        self.spacing_at_end = spacing_at_end

        
    def text(self, text):
        """
        Draw text on a baseline following the current heading
        
        """
        base_pen_state = self.isdown()
        base_heading = self.heading()
        spacing = self.spacing
        letter_objects = filtered_letter_objects(text)
        for i, letter in enumerate(letter_objects):
            is_last_letter = False if i<len(letter_objects)-1 else True
            if is_last_letter and not self.spacing_at_end:
                spacing = 0
            self._draw_letter(letter, spacing)
        self.setheading(base_heading)
        # put the pen back the way that we found it
        self.pen(pendown=base_pen_state)

        
    def text_circle(self, text, radius=None):
        """Draw text along a constant radius arc baseline 
        
        text:
            text to be drawn by the Turtle
            Draws counter-clockwise for positive radius,
            clock-wise for negative radius.
            Angular extent is a function of text, text height,
            text spacing, and radius
            ["text_circle_extent()" and "radius_for_extent()"
             may be useful for planning sizes where the text will fit] 

        radius:
            If radius is None, then use a radius where all text will 
            fit in the circle, counter-clockwise direction.
            If a radius value is entered,
            the Turtle convention will be followed of 
            positive radius is left of the Turtle, 
            resulting in counter-clockwise motion
            (use negative radius for clockwise)
            
        """
        if radius is None:
            radius = self.radius_for_extent(text, extent=360)
        base_pen_state = self.isdown()
        letter_objects = filtered_letter_objects(text)
        for i, letter in enumerate(letter_objects):
            # it is a little more pleasing to split the spacing 
            # before and after the character when printing in an arc
            half_spacing = self.spacing / 2.
            self.set_arc_segment_heading(half_spacing, radius)
            self.forward(half_spacing)
            self.set_arc_segment_heading(half_spacing, radius)
            character_width = letter.get_width(self.text_height)
            self.set_arc_segment_heading(character_width, radius)
            self._draw_letter(letter, 0)
            self.set_arc_segment_heading(character_width, radius)
            is_last_letter = False if i<len(letter_objects)-1 else True
            if not is_last_letter or self.spacing_at_end:
                self.set_arc_segment_heading(half_spacing, radius)
                self.forward(half_spacing)
                self.set_arc_segment_heading(half_spacing, radius)
        # put the pen back the way that we found it
        self.pen(pendown=base_pen_state)


    def text_circle_extent(self, text, radius, spacing_at_end=True):
        """Get the angle traveled along an arc for the length of text
        
        Might be useful for "planning ahead" to check if text will
        fit in an arc of the radius
        
        """
        # arc text generally looks better with the space at the end
        self.spacing_at_end = spacing_at_end
        letter_objects = filtered_letter_objects(text)
        heading_change = 0
        for i, letter in enumerate(letter_objects):
            character_width = letter.get_width(self.text_height)
            heading_change -= calc_heading_change(
                                character_width, radius) * 2.
            spacing_mult = 2.
            is_last_letter = False if i<len(letter_objects)-1 else True
            if is_last_letter and not self.spacing_at_end:
                spacing_mult = 1.5
            heading_change -= calc_heading_change(
                                self.spacing, radius) * spacing_mult
        return heading_change


    def radius_for_extent(self, text, extent=360, spacing_at_end=True):
        """Find the radius that will fit text in the "extent" of an arc
        
        """
        # include space at end to center text
        self.spacing_at_end = spacing_at_end
        width_of_text = text_width(text, self.text_height, self.spacing)
        if self.spacing_at_end:
            width_of_text += self.spacing
        else:
            width_of_text += self.spacing / 2.
        # the first estimate assumes that the length is along the
        # circumference, not in secant segments
        radius = width_of_text / math.radians(extent)
        # The exact formula is non-linear, 
        # so we will successively improve the estimate 
        # until we are within some accuracy tolerance.
        # 0.05 degrees should be close enough for most uses
        tolerance = 0.05
        # This usually requires only three or so tries, 
        # but we will include a counter to avoid infinite loops.
        max_tries = 20
        tries = 0
        while tries < max_tries:
            tries += 1
            calc_extent = self.text_circle_extent(text, radius, 
                                                self.spacing_at_end)
            # a simple ratio comes pretty close
            radius = radius * calc_extent / extent
            degrees_error = abs(calc_extent - extent)
            if degrees_error < tolerance:
                break
            # in a perfect world, we might raise an exception
            # if the number of tries was exceeded without
            # finding an adequately accurate answer
        return radius


    def set_arc_segment_heading(self, segment_length, radius):
        """Update heading for an inscribed arc segment
    
        Note that to return to a tangent position and heading,
        this should be applied at the start of a segment,
        and then applied again at the end of the segment
        
        """
        heading_change = calc_heading_change(segment_length, radius)
        self.setheading(self.heading() + heading_change)
        

    def head_to(self, x, y):
        """Set heading toward and move to a destination"""
        # This uses "x, y" input to be similar to Turtle.goto(),
        # even though the functions below use a tuple
        self.setheading(self.towards((x, y)))
        self.forward(self.distance((x, y)))


    def _draw_letter(self, letter_obj, spacing):
        """Draw a letter object 
        It is recommended to use text() 
        rather than this helper function for most cases
        (You can call text() with a single character, if you like)
        """  
        base_heading = self.heading()
        xy_start = self.position()
        segment_length = letter_obj.get_width(self.text_height) + spacing
        self.penup()
        p_data = _letter_to_baseline_coords(letter_obj, self.text_height,
                                          xy_start, base_heading)
        for i, p in enumerate(p_data):
            # The first move positions the turtle for writing the character
            # (which may not start at the current position)
            # so do not put the pen down on the first move.
            # For a space character, there is a special case to not put the
            # pen down.
            if i > 0 and not letter_obj.is_space:
                self.pendown()
            self.head_to(*p)
        self.penup()
        xy_start += turtle.Vec2D(segment_length, 0).rotate(base_heading)
        self.head_to(*xy_start)
        self.setheading(base_heading)


def calc_heading_change(segment_length, radius):
    """The heading change to follow an inscribed segment of an arc
    
    Note that to return to a tangent position and heading,
    the heading change should be applied at the start of a segment,
    and then the value applied again at the end of the segment
    """
    return math.degrees(math.asin(segment_length / 2. / radius)) 


def _letter_to_baseline_coords(letter, height, base_xy, base_heading):
    """rotate letter points to match a baseline 
    Users should not typically have to access this helper function,
    as text() will rotate text to match the base_heading"""
    # lower left corner "normalized" to height 1
    xmin, ymin = letter.get_start_delta(1)
    letter_points = []
    # this all could probably be done much more concisely,
    # but it helped me to debug it to break it down into steps
    for point in letter.data:
        # the "raw" letter data
        x, y = point
        # translate to have lower-left at (0,0)
        lx = x - xmin
        ly = y
        # rotate it
        xy = turtle.Vec2D(lx, ly).rotate(base_heading)
        # translate to the start position
        delta_left = letter.get_delta_left(1)
        width = letter.get_width(1)
        xy += turtle.Vec2D(xmin+delta_left, 0).rotate(base_heading)
        # now with height
        hxy = turtle.Vec2D(*xy) * height
        # translate along the baseline
        tx, ty = turtle.Vec2D(*hxy) + turtle.Vec2D(*base_xy)
        letter_points.append((tx, ty))
    return letter_points


if __name__ == '__main__':
    """You may simply call text() to have your TextTurtle text! """
    t = TextTurtle()
    t.shape('turtle')
    t.text('hello')
    # undo works too!
    while t.undobufferentries():
        t.undo()
    # imprint the Official Seal
    # it fits better with a slightly smaller font
    t.text_height = 40
    # speed thing up, or else it is going to take a long time
    t.speed(9)
    # don't drag the pen when not writing
    t.penup()
    text = 'The Great Seal'
    # find a radius where the text will fit in a 180 degree arc
    # the "-180" follows the Turtle convention for clock-wise
    # Turtle.circle() calls it "extent", so we use that term too
    radius = t.radius_for_extent(text, extent=-180)
    # head_to() conveniently combines setheading() and goto()
    t.head_to(-radius, 0)
    # we want our text arc starting "up"
    t.setheading(90)
    # Write the text in an arc
    # the "-radius" follows the Turtle convention for turning to the right
    t.text_circle(text, -radius)
    # to draw the complimentary lower arc, we have to adjust the radius
    # to get the text arcs to line up,
    # as we will be following the "inner" track of a baseline,
    # rather than the "outer" track
    radius += t.text_height
    t.head_to(-radius, 0)
    t.setheading(-90)
    text = 'of Text Turtle'
    t_degrees = t.text_circle_extent(text, radius)
    # move along the arc to center the text
    t.circle(radius, (180. + t_degrees) / 2.)
    t.text_circle(text, radius)
    # keep the screen open
    turtle.done()
