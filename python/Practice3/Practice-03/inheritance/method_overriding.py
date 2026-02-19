# overriding: ребенок меняет метод родителя

# Example 1: базовый метод
class Animal:
    def sound(self):
        print("Some sound")

# Example 2: переопределяем у Cat
class Cat(Animal):
    def sound(self):
        print("Meow")

# Example 3: переопределяем у Dog
class Dog(Animal):
    def sound(self):
        print("Woof")

# Example 4: одинаковый вызов, разный результат
if __name__ == "__main__":
    a = Animal()
    c = Cat()
    d = Dog()

    a.sound()
    c.sound()
    d.sound()

    for x in [a, c, d]:
        x.sound()
