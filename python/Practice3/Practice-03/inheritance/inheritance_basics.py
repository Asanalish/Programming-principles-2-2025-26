# наследование: ребенок получает методы родителя

# Example 1: базовый класс
class Animal:
    def speak(self):
        print("Animal sound")

# Example 2: наследник без изменений
class Dog(Animal):
    pass

# Example 3: еще один наследник
class Cat(Animal):
    pass

# Example 4: одинаковый метод у разных объектов
if __name__ == "__main__":
    a = Animal()
    a.speak()

    d = Dog()
    d.speak()

    c = Cat()
    c.speak()

    animals = [a, d, c]
    for x in animals:
        x.speak()
