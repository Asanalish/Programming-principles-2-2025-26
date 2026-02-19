# Example 1: return одного значения
def add(a, b):
    return a + b

# Example 2: return строки
def get_greeting(name):
    return "Hello, " + name

# Example 3: return True/False
def is_even(number):
    return number % 2 == 0

# Example 4: return двух значений (кортеж)
def min_and_max(numbers):
    return min(numbers), max(numbers)

if __name__ == "__main__":
    print("Sum:", add(2, 7))

    message = get_greeting("Sanzhar")
    print(message)

    print("Is 10 even?", is_even(10))
    print("Is 11 even?", is_even(11))

    values = [5, 1, 9, 3]
    smallest, biggest = min_and_max(values)
    print("Min =", smallest, "Max =", biggest)
