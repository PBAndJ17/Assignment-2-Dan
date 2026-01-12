import turtle

# Recursive function to draw the modified edge
def draw_edge(length, depth):
    if depth == 0:
        turtle.forward(length)
    else:
        length /= 3

        draw_edge(length, depth - 1)
        turtle.right(60)
        draw_edge(length, depth - 1)
        turtle.left(120)
        draw_edge(length, depth - 1)
        turtle.right(60)
        draw_edge(length, depth - 1)


# Function to draw the polygon using the recursive edges
def draw_polygon(sides, length, depth):
    angle = 360 / sides
    for _ in range(sides):
        draw_edge(length, depth)
        turtle.left(angle)


# -------- Main Program --------
sides = int(input("Enter the number of sides: "))
length = int(input("Enter the side length: "))
depth = int(input("Enter the recursion depth: "))




# Draw the pattern
draw_polygon(sides, length, depth)

turtle.done()
