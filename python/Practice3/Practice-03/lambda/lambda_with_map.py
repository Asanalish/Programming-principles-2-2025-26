# map() делает преобразование каждого элемента

if __name__ == "__main__":
    # Example 1: умножить все числа на 2
    numbers = [1, 2, 3, 4]
    doubled = list(map(lambda x: x * 2, numbers))
    print(doubled)

    # Example 2: добавить 1 к каждому
    plus_one = list(map(lambda x: x + 1, numbers))
    print(plus_one)

    # Example 3: сделать строки большими буквами
    names = ["ali", "dana", "sanzhar"]
    upper_names = list(map(lambda s: s.upper(), names))
    print(upper_names)

    # Example 4: перевести доллары в тенге (примерно * 470)
    dollars = [1, 5, 10]
    tenge = list(map(lambda x: x * 470, dollars))
    print(tenge)
