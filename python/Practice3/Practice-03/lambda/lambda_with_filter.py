# filter() оставляет только то, что True

if __name__ == "__main__":
    # Example 1: оставить только четные
    numbers = [1, 2, 3, 4, 5, 6]
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(evens)

    # Example 2: оставить только положительные
    mixed = [-3, 0, 2, -1, 5]
    positives = list(filter(lambda x: x > 0, mixed))
    print(positives)

    # Example 3: оставить слова длиной >= 5
    words = ["cat", "apple", "banana", "sun"]
    long_words = list(filter(lambda w: len(w) >= 5, words))
    print(long_words)

    # Example 4: оставить оценки >= 60
    scores = [45, 60, 72, 10, 90]
    passed = list(filter(lambda s: s >= 60, scores))
    print(passed)
