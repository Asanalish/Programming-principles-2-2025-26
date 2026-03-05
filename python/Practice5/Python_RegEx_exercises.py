import re

# 1.Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s.
pattern = r"ab*"

tests = ["a", "ab", "abbbb", "ba", "ac"]
for s in tests:
    print(s, bool(re.fullmatch(pattern, s)))

# 2.Write a Python program that matches a string that has an 'a' followed by two to three 'b'.
pattern = r"ab{2,3}"

tests = ["ab", "abb", "abbb", "abbbb", "a"]
for s in tests:
    print(s, bool(re.fullmatch(pattern, s)))

# 3.Write a Python program to find sequences of lowercase letters joined with a underscore.
pattern = r"[a-z]+_[a-z]+"

text = "ok hello_world BAD Hello_world a_b one_two_three x__y"
print(re.findall(pattern, text))

# 4.Write a Python program to find the sequences of one upper case letter followed by lower case letters.
pattern = r"[A-Z][a-z]+"

text = "Almaty is in KZ. aLmaty, USA, Xy, A"
print(re.findall(pattern, text))

# 5.Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.
pattern = r"a.*b"

tests = ["ab", "axxxb", "a123b", "ba", "a---c"]
for s in tests:
    print(s, bool(re.fullmatch(pattern, s)))

# 6.Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.
text = "Hello, world. How are you, today."
result = re.sub(r"[ ,\.]", ":", text)
print(result)

# 7.Write a python program to convert snake case string to camel case string.
s = "my_first_variable"

parts = re.split(r"_+", s)     # разбиваем по _
camel = parts[0]              # первое слово как есть
for p in parts[1:]:
    camel += p.capitalize()   # делаем First, Variable

print(camel)  # myFirstVariable

# 8.Write a Python program to split a string at uppercase letters.
s = "SplitThisString"
parts = re.findall(r"[A-Z][a-z]*", s)
print(parts)

# 9.Write a Python program to insert spaces between words starting with capital letters.
s = "HelloWorldAgain"
result = re.sub(r"(?<!^)([A-Z])", r" \1", s)
print(result)

# 10.Write a Python program to convert a given camel case string to snake case.
s = "myFirstVariable"
snake = re.sub(r"([A-Z])", r"_\1", s).lower()
print(snake)  # my_first_variable

