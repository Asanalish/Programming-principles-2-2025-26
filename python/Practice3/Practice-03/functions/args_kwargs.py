# Example 1: *args — много чисел
def sum_numbers(*numbers):
    print("Sum =", sum(numbers))

# Example 2: *args — найти максимум
def max_number(*numbers):
    print("Max =", max(numbers))

# Example 3: **kwargs — данные по ключу
def print_person(**info):
    print("Person info:", info)

# Example 4: **kwargs — красивый вывод
def print_profile(**profile):
    for key in profile:
        print(key, "=", profile[key])

if __name__ == "__main__":
    sum_numbers(1, 2, 3)
    sum_numbers(10, 20, 30, 40)

    max_number(3, 9, 1, 7)

    print_person(name="Sanzhar", age=16)

    print_profile(name="Amina", city="Almaty", hobby="reading")
