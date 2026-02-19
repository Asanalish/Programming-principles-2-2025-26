# Example 1: самый простой класс
class Student:
    pass

# Example 2: объект класса + добавляем поле вручную
class Phone:
    pass

# Example 3: класс с методом
class Dog:
    def bark(self):
        print("Woof!")

# Example 4: класс с двумя методами
class Calculator:
    def add(self, a, b):
        print(a + b)

    def mul(self, a, b):
        print(a * b)

if __name__ == "__main__":
    s = Student()
    print("Student object:", s)

    p = Phone()
    p.model = "iPhone"
    print("Phone model:", p.model)

    d = Dog()
    d.bark()

    c = Calculator()
    c.add(3, 5)
    c.mul(2, 4)
