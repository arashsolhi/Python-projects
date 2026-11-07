import turtle
import random

screen = turtle.Screen()
screen.tracer(0)
t = turtle.Turtle()
t.speed(0)
t.color("green")
t.hideturtle()
t.penup()

x, y = 0.0, 0.0

for i in range(10000000): 
    r = random.random()

    if r < 0.01:
        nx, ny = 0, 0.16 * y
    elif r < 0.86:
        nx, ny = 0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6
    elif r < 0.93:
        nx, ny = 0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6
    else:
        nx, ny = -0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44
    
    x, y = nx, ny
    t.goto(x * 50, y * 50 - 250)
    t.dot(2)

    if i % 1000 == 0:
        screen.update()

screen.update()
turtle.done()