# For_loops_example
for i in range(1, 6):
    print(i)
  
# Iterating through list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
  
# Summation using for loop
numbers = [2, 4, 6, 8]
total = 0
for n in numbers:
    total += n
print(total)

# Loop through a string
word = "Python"
for letter in word:
    print(letter)
 
# Using range() with step 
for i in range(0, 11, 2):
    print(i)             #0, 2, 4, 6, ...


# For loop with break / Stop loop when number is found
for i in range(1, 10):
    if i == 5:
        break
    print(i)

# Search for an element in a list
numbers = [3, 7, 1, 9, 5]
for n in numbers:
    if n == 9:
        print("Found 9")
        break

# Stop when user input is correct
passwords = ["1234", "admin", "qwerty"]

for p in passwords:
    if p == "admin":
        print("Correct password")
        break

# Exit loop on negative number
nums = [5, 3, -1, 7]
for n in nums:
    if n < 0:
        break
    print(n)
#For loop with continue operator
for i in range(1, 6):
    if i == 3:
        continue
    print(i)
# Skip even numbers
for i in range(1, 11):
    if i % 2 == 0:
        continue
    print(i)

# Ignore empty strings 
words = ["hello", "", "world"]
for w in words:
    if w == "":
        continue
    print(w)


