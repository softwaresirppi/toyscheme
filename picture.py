from turtle import *
from toyscheme_objects import SchemeNil
# Language level abstraction
# (open-picture height width) -> nil
# (close-picture)
# (draw-line point1_x point1_y point2_x point2_y) where both are conses

# ======ABSTRACTION CURTAIN========
# (make-frame origin horizontal vertical)
# painter is frame -> nil(draws)

# (line 0 1) :: painter
# beside :: painter -> painter -> painter
# ontop :: painter -> painter -> painter
# above :: painter -> painter -> painter

def open_picture(width, height):
    setup(float(width), float(height))
    window = Screen().cv._rootwindow
    window.attributes('-fullscreen', True)
    setworldcoordinates(0, 0, int(width), int(height))
    hideturtle()
    tracer(0)
    pencolor('white')
    bgcolor('black')
    title('Drawing')
    goto(0, 0)
    return SchemeNil()

def close_picture():
    update()
    exitonclick()
    return SchemeNil()

def draw_line(ax, ay, bx, by):
    penup()
    goto(float(ax), float(ay))
    pendown()
    goto(float(bx), float(by))
    return SchemeNil()