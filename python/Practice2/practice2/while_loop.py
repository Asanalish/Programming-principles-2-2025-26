#While_loop examples
i = 1
while i <= 5:
    print(i)
    i += 1 # from 1 to 5
  
# Sum numbers until limit
total = 0
i = 1
while i <= 5:
    total += i
    i += 1
print(total)

#Loop through a list using index
items = ["pen", "book", "laptop"]
i = 0
while i < len(items):
    print(items[i])
    i += 1

#While loop with break
#Stop on specific input
passwords = ["1234", "admin", "guest"]
i = 0
while i < len(passwords):
    if passwords[i] == "admin":
        print("Access granted")
        break
    i += 1
  
#Exit infinite loop
while True:
    print("Running...")
    break

# While loop with continue 
i = 0
while i < 10:
    i += 1
    if i % 2 == 0:
        continue
    print(i)   # Skip even numbers


numbers = [3, -1, 5, -2, 7]
i = 0
while i < len(numbers):
    if numbers[i] < 0:
        i += 1
        continue
    print(numbers[i])   # Skip negative numbers
    i += 1
