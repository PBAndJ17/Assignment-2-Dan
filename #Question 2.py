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
