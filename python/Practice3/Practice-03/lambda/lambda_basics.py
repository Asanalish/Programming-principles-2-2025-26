# Example 1: обычная функция
def double(x):
    return x * 2

# Example 2: lambda вместо простой функции
double_lambda = lambda x: x * 2  # noqa: E731

# Example 3: lambda с двумя аргументами
add_lambda = lambda a, b: a + b  # noqa: E731

# Example 4: lambda для проверки
is_positive = lambda x: x > 0  # noqa: E731

if __name__ == "__main__":
    print(double(5))
    print(double_lambda(5))

    print(add_lambda(3, 7))

    print(is_positive(10))
    print(is_positive(-2))
