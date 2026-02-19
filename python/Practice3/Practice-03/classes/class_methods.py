# методы класса: работают через self

# Example 1: метод приветствия
class Student:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print("Hello, I am", self.name)

# Example 2: метод прибавления к счетчику
class Counter:
    def __init__(self):
        self.value = 0

    def add_one(self):
        self.value += 1

# Example 3: метод для проверки возраста
class Person:
    def __init__(self, age):
        self.age = age

    def is_adult(self):
        return self.age >= 18

# Example 4: метод для добавления элементов в список
class ShoppingList:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

if __name__ == "__main__":
    s = Student("Amina")
    s.say_hello()

    c = Counter()
    c.add_one()
    c.add_one()
    print("Counter:", c.value)

    p = Person(16)
    print("Adult?", p.is_adult())

    shop = ShoppingList()
    shop.add_item("milk")
    shop.add_item("bread")
    print("Items:", shop.items)
