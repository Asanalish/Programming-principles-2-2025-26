#If statements
x = 5
if x > 0:
    print("Positive") # Check positive number
  
# Check password length
password = "admin123"
if len(password) >= 6:
    print("Strong password")

#Check even number
num = 8
if num % 2 == 0:
    print("Even number")

# If else statements
score = 45
if score >= 50:
    print("Pass")
else:
    print("Fail") # Pass or fail

# Number sign
x = -3
if x > 0:
    print("Positive")
else:
    print("Negative or zero")

# Login check
username = "admin"
if username == "admin":
    print("Welcome")
else:
    print("Access denied")

# If elif else 
score = 82
if score >= 90:
    print("A")
elif score >= 75:
    print("B")
elif score >= 60:
    print("C")
else:
    print("F")  #Grade system

# Temperature check
temp = 18
if temp > 30:
    print("Hot")
elif temp > 15:
    print("Warm")
else:
    print("Cold")

# Traffic light
light = "yellow"
if light == "red":
    print("Stop")
elif light == "yellow":
    print("Get ready")
else:
    print("Go")

# Short hand if else (Ternary operator)
num = 7
result = "Even" if num % 2 == 0 else "Odd"
print(result)

a, b = 5, 9
max_num = a if a > b else b
print(max_num)

is_logged = True
print("Welcome") if is_logged else print("Please log in")


# Switch if elif else 
day = 3
if day == 1:
    print("Monday")
elif day == 2:
    print("Tuesday")
elif day == 3:
    print("Wednesday")
else:
    print("Unknown day") # Dat of the week
  




