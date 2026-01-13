import turtle #importing turtle into python

#Function to draw one side of polygon using recursion

def polygon(t, length, depth):
    # For 0 depth draws straight line
    if depth == 0:
        t.forward(length)
        return
    # Divide the length into 3 parts
    third = length / 3

    polygon(t, third, depth - 1)
    t.right(60)
    polygon(t, third, depth - 1)
    t.left(120)
    polygon(t, third, depth - 1)
    t.right(60)
    polygon(t, third, depth - 1)

# Function to draw the shape completely

def draw_shape(sides, length, depth):
    screen = turtle.Screen()
    screen.title("Recursive Geometric Pattern")

    t = turtle.Turtle()
    t.speed(0)

    # Calculate the angle for the turtle to turn after each side
    angle = 360 / sides

    for i in range(sides):
        polygon(t, length, depth)
        t.right(angle)

    screen.update()
    turtle.done()


if __name__ == "__main__":
    # To get the users input
    sides = int(input("Enter the number of sides: "))
    length = float(input("Enter the side length: "))
    depth = int(input("Enter the recursion depth: "))

    draw_shape(sides, length, depth)
