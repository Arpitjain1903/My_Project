import string
import random

chars = " " + string.punctuation + string.digits + string.ascii_letters
chars = list(chars)
key = chars.copy()
random.shuffle(key)

print("----------------------------")
print("Welcome to the Message Hider!")
print("----------------------------")

while True:
    print("\nMenu:")
    print("1. Encrypt a message")
    print("2. Decrypt a message")
    print("3. Exit")
    choice = input("Enter your option (1/2/3): ").strip()
    print("----------------------------")

    if choice == '1':
        text = input("Enter your message to encrypt: ")
        ciper_text = ""
        for letter in text:
            if letter in chars:
                index = chars.index(letter)
                ciper_text += key[index]
            else:
                ciper_text += letter  # keep unknown chars as is
        print("----------------------------")
        print(f"Original message : {text}")
        print(f"Encrypted message: {ciper_text}")
        print("----------------------------")
    elif choice == '2':
        text2 = input("Enter your message to decrypt: ")
        plain_text = ""
        for letter in text2:
            if letter in key:
                index = key.index(letter)
                plain_text += chars[index]
            else:
                plain_text += letter  # keep unknown chars as is
        print("----------------------------")
        print(f"Encrypted message : {text2}")
        print(f"Decrypted message : {plain_text}")
        print("----------------------------")
    elif choice == '3':
        print("Exiting... Goodbye!")
        break
    else:
        print("Invalid option. Please enter 1, 2, or 3.")
