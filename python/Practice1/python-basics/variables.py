x = 4
x = "Sally"
print(x)
#Casting 
x = str(3)
y = int(3)
z = float(3)
#To get the TYPE
print(type(x))
#legal variable names
myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"
#Illegal variable names
#2myvar = "John"
#my-var = "John"
#my var = "John"
#Assigning multiple values
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)
#One value to multiple values
x = y = z = "Orange"
print(x)
print(y)
print(z)
#Unpack a Collection
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)
#Output variables
x = "Python "
y = "is "
z = "awesome"
print(x + y + z) #Python is awesome
#Global variables
'''If you create a global variable, and then
a local variable with the same name -> local will be used only inside of a function
but global everywhere outside of a function'''
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc() #Python is fantastic

print("Python is " + x) #Python is awesome (global)
