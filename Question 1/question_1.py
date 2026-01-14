
def shift_in_group(ch, shift, group):
   
    i = group.index(ch)
    new_i = (i + shift) % len(group)
    return group[new_i]

# Encryption for single characters according to the rules defined
def encrypt_char(ch, shift1, shift2):
    # THe alphabetical groups are defined according to question
    low1 = "abcdefghijklm"
    low2 = "nopqrstuvwxyz"
    up1  = "ABCDEFGHIJKLM"
    up2  = "NOPQRSTUVWXYZ"

    # The non alphabetical characters are returned without change
    if not ch.isalpha():
        return ch

    k1 = shift1 * shift2      # For lowercase (a-m)
    k2 = shift1 + shift2      # For lowercase (n-z)
    k3 = shift1               # For uppercase (A-M)
    k4 = shift2 * shift2      # For uppercase (N-Z)

    # Encryption applied based on the character groups
    if ch in low1:
        return shift_in_group(ch, +k1, low1)
    elif ch in low2:
        return shift_in_group(ch, -k2, low2)
    elif ch in up1:
        return shift_in_group(ch, -k3, up1)
    elif ch in up2:
        return shift_in_group(ch, +k4, up2)

    return ch  

# Decryption for single characters according to the rules defined
def decrypt_char(ch, shift1, shift2):
    # The alphabetical groups are defined according to question
    low1 = "abcdefghijklm"
    low2 = "nopqrstuvwxyz"
    up1  = "ABCDEFGHIJKLM"
    up2  = "NOPQRSTUVWXYZ"

     # The non alphabetical characters are returned without change
    if not ch.isalpha():
        return ch

    k1 = shift1 * shift2     # For lowercase (a-m)
    k2 = shift1 + shift2     # For lowercase (n-z)
    k3 = shift1              # For uppercase (A-M)
    k4 = shift2 * shift2     # For uppercase (N-Z)

     # Decryption applied based on the character groups
    if ch in low1:
        return shift_in_group(ch, -k1, low1)
    elif ch in low2:
        return shift_in_group(ch, +k2, low2)
    elif ch in up1:
        return shift_in_group(ch, +k3, up1)
    elif ch in up2:
        return shift_in_group(ch, -k4, up2) 

    return ch

# To Encrypt letter by letter
def encrypt_text(text, shift1, shift2):
    result = ""
    for ch in text:
        result += encrypt_char(ch, shift1, shift2)
    return result

# To decrypt letter by letter
def decrypt_text(text, shift1, shift2):
    result = ""
    for ch in text:
        result += decrypt_char(ch, shift1, shift2)
    return result


def main():
    # Obtains the shift values from the user
    shift1 = int(input("Enter shift1 (integer): "))
    shift2 = int(input("Enter shift2 (integer): "))

    with open("raw_text.txt", "r", encoding="utf-8") as f:
        raw = f.read()

    # The text is encrypted and written in a file   
    encrypted = encrypt_text(raw, shift1, shift2)
    with open("encrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(encrypted)

    # The encrypted text is decrypted and written in a file
    decrypted = decrypt_text(encrypted, shift1, shift2)
    with open("decrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(decrypted)

    # A check for whether decryption is correct
    if decrypted == raw:
        print("SUCCESS: Decryption matches the original file.")
    else:
        print("FAIL: Decryption does NOT match the original file.")


main()
