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
def encrypt_text(text, key):
    encrypted_text = ""
    for char in text:
        encrypted_text += chr(ord(char) + key)
    return encrypted_text


def decrypt_text(text, key):
    decrypted_text = ""
    for char in text:
        decrypted_text += chr(ord(char) - key)
    return decrypted_text


def encrypt_file(filename, key):
    with open(filename, "r+") as file:
        content = file.read()
        file.seek(0)
        file.write(encrypt_text(content, key))
        file.truncate()
    print("Encrypted successfully")

def decrypt_file(filename, key):
    with open(filename, "r+") as file:
        content = file.read()
        file.seek(0)
        file.write(decrypt_text(content, key))
        file.truncate()
    print("Decrypted successfully")

filename = "raw_text.txt"

if __name__ == "__main__":
    decrypt_file(filename, 5)
    
print("hey")
