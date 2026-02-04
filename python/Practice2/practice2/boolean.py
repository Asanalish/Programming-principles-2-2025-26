# Python Booleans
print(20 > 10)
print(20 == 21)
print(99 < 98.9)

a = 200
b = 33
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

print(bool("Hello"))
print(bool(15))

x = "Hello"
y = 15
print(bool(x))
print(bool(y))

bool("abc") #Any string is True, except empty strings
bool(123) #Any number is True, except 0
bool(["apple", "cherry", "banana"]) #Any list, tuple, set, and dictionary are True, except empty ones
 
#The following will return False:
bool(False) 
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({}) 


# One more value, or object in this case, evaluates to False:
mylist = []
print(bool(mylist))  #False


def myFunction():
  return True
print(myFunction())

# Print "YES!" if the function returns True, otherwise print "NO!":
def myFunction() :
  return True
if myFunction():
  print("YES!")
else:
  print("NO!")

#booleans 
print(10>9) #return True

print(10==9) #return False

print(10<9) #return False

print(bool("abc")) #return True

print(bool(0)) #return False because 0-False


