# __init__ задаёт стартовые данные

# Example 1: хранить имя
class Student:
    def __init__(self, name):
        self.name = name

# Example 2: хранить имя и возраст
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# Example 3: значение по умолчанию
class Book:
    def __init__(self, title, pages=100):
        self.title = title
        self.pages = pages

# Example 4: простая "копилка"
class PiggyBank:
    def __init__(self, money=0):
        self.money = money

if __name__ == "__main__":
    s = Student("Sanzhar")
    print(s.name)

    p = Person("Ali", 16)
    print(p.name, p.age)

    b = Book("Python Basics")
    print(b.title, b.pages)

    bank = PiggyBank()
    print("Money:", bank.money)
