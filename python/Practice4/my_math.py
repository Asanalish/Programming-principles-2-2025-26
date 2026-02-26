import math

# Convert degree to radian
degree = 15
radian = math.radians(degree)

print(radian)

# Area of a trapezoid
height = 5
base1 = 5
base2 = 6

area = float((base1 + base2) / 2 * height)
print(area)

# Area of a regular polygon
n = 4
side = 25

area = (n * side ** 2) / (4 * math.tan(math.pi / n))
print(area)

# Area of a parallelogram
base = 5
height = 6

area = float(base * height)
print(area)