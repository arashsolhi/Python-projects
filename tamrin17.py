import turtle
import random

screen = turtle.Screen()
screen.tracer(0)
t = turtle.Turtle()
t.speed(0)
t.hideturtle()
t.penup()

vertices = [
    (0, 200, "blue"),
    (-200, -200, "red"),
    (200, -200, "green")
]

x, y = 0, 0

for vx, vy, color in vertices:
    t.goto(vx, vy)
    t.dot(10, color)

for _ in range(10000):
    vx, vy, color = random.choice(vertices)
    x = (x + vx) / 2
    y = (y + vy) / 2
    t.goto(x, y)
    t.dot(3, color)

screen.update()
turtle.done()