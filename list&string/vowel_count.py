s = input("Enter text: ").lower()
count = sum(1 for ch in s if ch in "aeiou")
print("Vowels:", count)