# Mini-project 3 for An Introduction to Interactive Programming in Python class

# based on the template from: http://www.codeskulptor.org/#examples-stopwatch_template.py

import simplegui

# define global variables
count = 0
HEIGHT = 300
WIDTH = 400
running = False
x = 0
y = 0


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    tc = t
    a = t / 600
    d = t % 10
    tc = t - d - 600*a
    tc = tc / 10
    if tc < 10:
        b = 0
        c = tc
    else:
        b = tc / 10
        c = tc % 10
    formatted = str(a) + ":" + str(b) + str(c) + ":" + str(d)
    return formatted

# define event handlers for buttons; "Start", "Stop", "Reset"

def start():
    global running
    running = True
    timer.start()

def stop():
    global running, x, y
    timer.stop()
    if running:
        y+=1
        if not count % 10:
            x+=1
    running = False


def reset():
    global count, running, x, y
    timer.stop()
    count = 0
    x = 0
    y = 0


# define event handler for timer with 0.1 sec interval
def tick():
    global count
    count+=1


# define draw handler

def draw(canvas):
    canvas.draw_text(str(format(count)), (WIDTH/3, HEIGHT/2), 48, 'Red')
    canvas.draw_text(str(x) + '/' + str(y), (4*WIDTH/5, HEIGHT/5), 28, 'Blue')


# create frame
frame = simplegui.create_frame('title', WIDTH, HEIGHT)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, tick)



# register event handlers

frame.add_button('Start', start, 150)
frame.add_button('Stop', stop, 150)
frame.add_button('Reset', reset, 150)


# Please remember to review the grading rubric

frame.start()
