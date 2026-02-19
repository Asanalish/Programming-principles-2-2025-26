# Example 1: самая простая функция (без аргументов)
def say_hello():
    print("Hello!")

# Example 2: функция с аргументом
def greet_person(name):
    print("Hello,", name)

# Example 3: функция с двумя аргументами
def add_numbers(a, b):
    print("Sum =", a + b)

# Example 4: функция, которая что-то возвращает
def square(number):
    return number * number

if __name__ == "__main__":
    say_hello()
    greet_person("Sanzhar")
    add_numbers(3, 5)

    result = square(4)
    print("Square =", result)
