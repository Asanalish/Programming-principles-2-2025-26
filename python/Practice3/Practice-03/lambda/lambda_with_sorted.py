# sorted() сортирует, key= говорит как сортировать

if __name__ == "__main__":
    # Example 1: сортировка по длине слова
    words = ["apple", "kiwi", "banana"]
    by_length = sorted(words, key=lambda w: len(w))
    print(by_length)

    # Example 2: сортировка чисел по модулю
    numbers = [3, -10, 2, -5]
    by_abs = sorted(numbers, key=lambda x: abs(x))
    print(by_abs)

    # Example 3: сортировка по последней букве
    by_last_char = sorted(words, key=lambda w: w[-1])
    print(by_last_char)

    # Example 4: сортировка пар (имя, возраст) по возрасту
    people = [("Ali", 16), ("Dana", 15), ("Sanzhar", 17)]
    by_age = sorted(people, key=lambda p: p[1])
    print(by_age)
