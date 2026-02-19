# Example 1: обычная функция
def double(x):
    return x * 2

# Example 2: lambda вместо простой функции
double_lambda = lambda x: x * 2

# Example 3: lambda с двумя аргументами
add_lambda = lambda a, b: a + b

# Example 4: lambda для проверки
is_positive = lambda x: x > 0

# Example 5: lambda внутри функции
def select_operation(choice):
    if choice == 1:
        return lambda a, b: a + b
    elif choice == 2:
        return lambda a, b: a - b
    else:
        return lambda a, b: a * b

if __name__ == "__main__":
    print(double(5))           # 10
    print(double_lambda(5))    # 10
    print(add_lambda(3, 7))    # 10
    print(is_positive(10))     # True
    print(is_positive(-2))     # False

    operation = select_operation(1)
    print(operation(10, 6))    # 16

    operation = select_operation(2)
    print(operation(10, 6))    # 4

    operation = select_operation(3)
    print(operation(10, 6))    # 60
