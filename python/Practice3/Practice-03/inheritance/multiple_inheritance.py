# multiple inheritance: класс наследуется от двух родителей

# Example 1: первый родитель
class CanRun:
    def run(self):
        print("Running")

# Example 2: второй родитель
class CanSwim:
    def swim(self):
        print("Swimming")

# Example 3: ребенок получает оба метода
class Athlete(CanRun, CanSwim):
    pass

# Example 4: использование
if __name__ == "__main__":
    a = Athlete()
    a.run()
    a.swim()

    a.run()
    a.swim()
