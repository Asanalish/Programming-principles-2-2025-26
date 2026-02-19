# class variable = общая для всех объектов
# instance variable = у каждого своя

# Example 1: общая школа
class Student:
    school = "My School"

    def __init__(self, name):
        self.name = name

# Example 2: общий курс валюты
class Money:
    rate = 470

    def __init__(self, dollars):
        self.dollars = dollars

# Example 3: счетчик созданных объектов
class User:
    count = 0

    def __init__(self, name):
        self.name = name
        User.count += 1

# Example 4: показать разницу class vs instance
class Phone:
    brand = "Generic"

    def __init__(self, model):
        self.model = model

if __name__ == "__main__":
    s1 = Student("Ali")
    s2 = Student("Dana")
    print(s1.name, s1.school)
    print(s2.name, s2.school)

    m = Money(10)
    print("Tenge:", m.dollars * Money.rate)

    u1 = User("A")
    u2 = User("B")
    print("Users created:", User.count)

    p1 = Phone("A1")
    p2 = Phone("B2")
    p2.brand = "Custom"  # только для p2
    print("p1 brand:", p1.brand, "model:", p1.model)
    print("p2 brand:", p2.brand, "model:", p2.model)
    print("Phone.brand:", Phone.brand)
