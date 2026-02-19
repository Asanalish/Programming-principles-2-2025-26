# Example 1: позиционные аргументы
def student_info(name, age):
    print(name, "is", age, "years old")

# Example 2: аргумент по умолчанию
def introduce(name, country="Kazakhstan"):
    print(name, "is from", country)

# Example 3: аргументы по ключу (keyword arguments)
def rectangle_area(width, height):
    print("Area =", width * height)

# Example 4: передача списка в функцию
def print_numbers(numbers):
    for num in numbers:
        print(num, end=" ")
    print()

if __name__ == "__main__":
    student_info("Ali", 16)

    introduce("Amina")
    introduce("Dana", "Turkey")

    rectangle_area(height=5, width=4)

    my_numbers = [10, 20, 30]
    print_numbers(my_numbers)
