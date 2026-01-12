#question 3

import turtle
t=turtle

 
side=int(input("Enter the number of sides of polygon(>3):"))
length=int(input("Enter the length of sides:"))
depth=int(input("Enter the recursive depth:"))

t.speed(0)

def polygon(length, depth):
    if depth == 0:
        t.forward(length)
    else:
        segment_length = length/3

        polygon(segment_length, depth - 1)
        t.left(60)
        polygon(segment_length, depth -1)
        t.right(120)
        polygon(segment_length, depth -1)
        t.left(60)
        polygon(segment_length, depth -1)

def draw_polygon(side, length, depth):
    angle= 360/side

    for i in range(side):
        polygon(length, depth)
        t.left(angle)

draw_polygon(side, length, depth)

t.done()