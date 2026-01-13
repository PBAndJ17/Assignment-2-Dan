# Q1 - Encrypt -> Decrypt -> Verify (Beginner Friendly, reversible)
# Files used:
#   input:  raw_text.txt
#   output: encrypted_text.txt
#   output: decrypted_text.txt

def shift_in_group(ch, shift, group):
    """
    Shift a character inside a given group (string) with wrap-around.
    group length is 13 for each half.
    shift can be + (forward) or - (backward).
    """
    i = group.index(ch)
    new_i = (i + shift) % len(group)
    return group[new_i]


def encrypt_char(ch, shift1, shift2):
    # Define the 4 half-groups ()
    low1 = "abcdefghijklm"
    low2 = "nopqrstuvwxyz"
    up1  = "ABCDEFGHIJKLM"
    up2  = "NOPQRSTUVWXYZ"

    # If not a letter, keep unchanged
    if not ch.isalpha():
        return ch

    # Shifts from the question
    k1 = shift1 * shift2      # lowercase a-m forward
    k2 = shift1 + shift2      # lowercase n-z backward
    k3 = shift1               # uppercase A-M backward
    k4 = shift2 * shift2      # uppercase N-Z forward (shift2 squared)

    # Apply rules
    if ch in low1:
        return shift_in_group(ch, +k1, low1)
    elif ch in low2:
        return shift_in_group(ch, -k2, low2)
    elif ch in up1:
        return shift_in_group(ch, -k3, up1)
    elif ch in up2:
        return shift_in_group(ch, +k4, up2)

    return ch  # safety (should not reach)


def decrypt_char(ch, shift1, shift2):
    # Same 4 half-groups
    low1 = "abcdefghijklm"
    low2 = "nopqrstuvwxyz"
    up1  = "ABCDEFGHIJKLM"
    up2  = "NOPQRSTUVWXYZ"

    if not ch.isalpha():
        return ch

    # Same shift amounts
    k1 = shift1 * shift2
    k2 = shift1 + shift2
    k3 = shift1
    k4 = shift2 * shift2

    # Reverse (opposite direction)
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

    # Read raw_text.txt
    with open("raw_text.txt", "r", encoding="utf-8") as f:
        raw = f.read()

    # Encrypt -> encrypted_text.txt
    encrypted = encrypt_text(raw, shift1, shift2)
    with open("encrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(encrypted)

    # Decrypt -> decrypted_text.txt
    decrypted = decrypt_text(encrypted, shift1, shift2)
    with open("decrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(decrypted)

    # Verify
    if decrypted == raw:
        print("SUCCESS: Decryption matches the original file.")
    else:
        print("FAIL: Decryption does NOT match the original file.")


main()
