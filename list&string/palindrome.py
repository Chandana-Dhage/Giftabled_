s = input("Enter text: ").lower()
print("Palindrome" if s == s[::-1] else "Not palindrome")