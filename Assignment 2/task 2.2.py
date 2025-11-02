
#!/usr/bin/env python3
import re

def is_palindrome(s: str) -> bool:
    cleaned = re.sub(r'[^A-Za-z0-9]', '', s).lower()
    return cleaned == cleaned[::-1]

if __name__ == '__main__':
    text = input("Enter text to check: ")
    if is_palindrome(text):
        print("Palindrome")
    else:
        print("Not a palindrome")
