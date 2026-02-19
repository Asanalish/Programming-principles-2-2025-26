# super() помогает вызвать __init__ родителя

# Example 1: родитель
class Person:
    def __init__(self, name):
        self.name = name

# Example 2: ребенок добавляет grade
class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade

# Example 3: ребенок добавляет city
class Worker(Person):
    def __init__(self, name, city):
        super().__init__(name)
        self.city = city

# Example 4: печать данных
if __name__ == "__main__":
    s = Student("Sanzhar", 11)
    print(s.name, s.grade)

    w = Worker("Ali", "Almaty")
    print(w.name, w.city)

    p = Person("Dana")
    print(p.name)
