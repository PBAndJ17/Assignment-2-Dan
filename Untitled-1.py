def encrypt_char(char, shift1, shift2):
    """
    Encrypt a single character based on the specified rules.
    
    Rules:
    - Lowercase letters:
        * First half (a-m): shift forward by shift1 * shift2
        * Second half (n-z): shift backward by shift1 + shift2
    - Uppercase letters:
        * First half (A-M): shift backward by shift1
        * Second half (N-Z): shift forward by shift2²
    - Other characters remain unchanged
    """
    if 'a' <= char <= 'm':
        # Lowercase first half - shift forward
        shift = shift1 * shift2
        new_pos = (ord(char) - ord('a') + shift) % 26
        return chr(ord('a') + new_pos)
    
    elif 'n' <= char <= 'z':
        # Lowercase second half - shift backward
        shift = shift1 + shift2
        new_pos = (ord(char) - ord('a') - shift) % 26
        return chr(ord('a') + new_pos)
    
    elif 'A' <= char <= 'M':
        # Uppercase first half - shift backward
        shift = shift1
        new_pos = (ord(char) - ord('A') - shift) % 26
        return chr(ord('A') + new_pos)
    
    elif 'N' <= char <= 'Z':
        # Uppercase second half - shift forward
        shift = shift2 ** 2
        new_pos = (ord(char) - ord('A') + shift) % 26
        return chr(ord('A') + new_pos)
    
    else:
        # All other characters remain unchanged
        return char


def decrypt_char(char, shift1, shift2):
    """
    Decrypt a single character by reversing the encryption rules.
    We need to try both possibilities and see which gives a valid result.
    """
    if 'a' <= char <= 'z':
        # Try as if it was originally from first half (a-m) - reverse forward shift
        shift = shift1 * shift2
        original_pos = (ord(char) - ord('a') - shift) % 26
        if 0 <= original_pos <= 12:  # Confirms it was in first half
            return chr(ord('a') + original_pos)
        
        # Otherwise it must be from second half (n-z) - reverse backward shift
        shift = shift1 + shift2
        original_pos = (ord(char) - ord('a') + shift) % 26
        return chr(ord('a') + original_pos)
    
    elif 'A' <= char <= 'Z':
        # Try as if it was originally from first half (A-M) - reverse backward shift
        shift = shift1
        original_pos = (ord(char) - ord('A') + shift) % 26
        if 0 <= original_pos <= 12:  # Confirms it was in first half
            return chr(ord('A') + original_pos)
        
        # Otherwise it must be from second half (N-Z) - reverse forward shift
        shift = shift2 ** 2
        original_pos = (ord(char) - ord('A') - shift) % 26
        return chr(ord('A') + original_pos)
    
    else:
        # All other characters (spaces, numbers, special chars) remain unchanged
        return char


def encrypt_file(input_file, output_file, shift1, shift2):
    """
    Reads from input_file, encrypts its contents, and writes to output_file.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        encrypted_content = ''.join(encrypt_char(char, shift1, shift2) for char in content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(encrypted_content)
        
        print(f"✓ Encryption complete: '{input_file}' -> '{output_file}'")
        return True
    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found!")
        return False
    except Exception as e:
        print(f"Error during encryption: {e}")
        return False


def decrypt_file(input_file, output_file, shift1, shift2):
    """
    Reads from input_file, decrypts its contents, and writes to output_file.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        decrypted_content = ''.join(decrypt_char(char, shift1, shift2) for char in content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(decrypted_content)
        
        print(f"✓ Decryption complete: '{input_file}' -> '{output_file}'")
        return True
    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found!")
        return False
    except Exception as e:
        print(f"Error during decryption: {e}")
        return False


def verify_decryption(original_file, decrypted_file):
    """
    Compares the original file with the decrypted file to verify successful decryption.
    """
    try:
        with open(original_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        with open(decrypted_file, 'r', encoding='utf-8') as f:
            decrypted_content = f.read()
        
        if original_content == decrypted_content:
            print(f"\n✓ SUCCESS: Decryption verification passed!")
            print(f"  '{original_file}' matches '{decrypted_file}'")
            return True
        else:
            print(f"\n✗ FAILURE: Decryption verification failed!")
            print(f"  '{original_file}' does NOT match '{decrypted_file}'")
            
            # Show differences for debugging
            if len(original_content) != len(decrypted_content):
                print(f"  Length difference: {len(original_content)} vs {len(decrypted_content)}")
            else:
                diff_count = sum(1 for a, b in zip(original_content, decrypted_content) if a != b)
                print(f"  Number of different characters: {diff_count}")
            
            return False
    
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return False
    except Exception as e:
        print(f"Error during verification: {e}")
        return False


def main():
    """
    Main program that orchestrates the encryption, decryption, and verification process.
    """
    print("=" * 60)
    print("Text Encryption and Decryption Program")
    print("=" * 60)
    
    # Get user input for shift values
    try:
        shift1 = int(input("\nEnter shift1 value: "))
        shift2 = int(input("Enter shift2 value: "))
    except ValueError:
        print("Error: Please enter valid integer values for shifts!")
        return
    
    print(f"\nUsing shift1={shift1}, shift2={shift2}")
    print("-" * 60)
    
    # Step 1: Encrypt the file
    print("\n[Step 1] Encrypting raw_text.txt...")
    if not encrypt_file("raw_text.txt", "encrypted_text.txt", shift1, shift2):
        return
    
    # Step 2: Decrypt the file
    print("\n[Step 2] Decrypting encrypted_text.txt...")
    if not decrypt_file("encrypted_text.txt", "decrypted_text.txt", shift1, shift2):
        return
    
    # Step 3: Verify the decryption
    print("\n[Step 3] Verifying decryption...")
    verify_decryption("raw_text.txt", "decrypted_text.txt")
    
    print("\n" + "=" * 60)
    print("Program complete!")
    print("Generated files:")
    print("  - encrypted_text.txt (encrypted content)")
    print("  - decrypted_text.txt (decrypted content)")
    print("=" * 60)


if __name__ == "__main__":
    main()