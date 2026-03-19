from functools import reduce

numbers = [1, 2, 3, 4, 5]

print("Numbers:", numbers)

# map
squared = list(map(lambda x: x*x, numbers))
print(squared)

# filter
even = list(filter(lambda x: x % 2 == 0, numbers))
print(even)

# reduce
product = reduce(lambda a, b: a*b, numbers)
print(product)

# basic functions
print("len:", len(numbers))
print("sum:", sum(numbers))
print("min:", min(numbers))
print("max:", max(numbers))

# sorted
print("sorted:", sorted([5, 2, 9, 1]))

# type + conversion
print(type(numbers))
print(int("10"))
print(float("2.5"))
print(str(100))