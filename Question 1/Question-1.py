
def shift_in_group(ch, shift, group):
  
    i = group.index(ch)
    new_i = (i + shift) % len(group)
    return group[new_i]


def encrypt_char(ch, shift1, shift2):
    low1 = "abcdefghijklm"
    low2 = "nopqrstuvwxyz"
    up1  = "ABCDEFGHIJKLM"
    up2  = "NOPQRSTUVWXYZ"

    if not ch.isalpha():
        return ch

    k1 = shift1 * shift2      
    k2 = shift1 + shift2      
    k3 = shift1               
    k4 = shift2 * shift2      


    if ch in low1:
        return shift_in_group(ch, +k1, low1)
    elif ch in low2:
        return shift_in_group(ch, -k2, low2)
    elif ch in up1:
        return shift_in_group(ch, -k3, up1)
    elif ch in up2:
        return shift_in_group(ch, +k4, up2)

    return ch  


def decrypt_char(ch, shift1, shift2):
    
    low1 = "abcdefghijklm"
    low2 = "nopqrstuvwxyz"
    up1  = "ABCDEFGHIJKLM"
    up2  = "NOPQRSTUVWXYZ"

    if not ch.isalpha():
        return ch

    
    k1 = shift1 * shift2
    k2 = shift1 + shift2
    k3 = shift1
    k4 = shift2 * shift2

    
    if ch in low1:
        return shift_in_group(ch, -k1, low1)   # was +k1
    elif ch in low2:
        return shift_in_group(ch, +k2, low2)   # was -k2
    elif ch in up1:
        return shift_in_group(ch, +k3, up1)    # was -k3
    elif ch in up2:
        return shift_in_group(ch, -k4, up2)    # was +k4

    return ch


def encrypt_text(text, shift1, shift2):
    result = ""
    for ch in text:
        result += encrypt_char(ch, shift1, shift2)
    return result


def decrypt_text(text, shift1, shift2):
    result = ""
    for ch in text:
        result += decrypt_char(ch, shift1, shift2)
    return result


def main():
    shift1 = int(input("Enter shift1 (integer): "))
    shift2 = int(input("Enter shift2 (integer): "))

    
    with open("raw_text.txt", "r", encoding="utf-8") as f:
        raw = f.read()

    
    encrypted = encrypt_text(raw, shift1, shift2)
    with open("encrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(encrypted)

    
    decrypted = decrypt_text(encrypted, shift1, shift2)
    with open("decrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(decrypted)

    
    if decrypted == raw:
        print("SUCCESS: Decryption matches the original file.")
    else:
        print("FAIL: Decryption does NOT match the original file.")


main()



