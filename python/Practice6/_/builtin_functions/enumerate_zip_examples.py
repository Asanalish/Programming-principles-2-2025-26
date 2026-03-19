
names = ["Ali", "Dana", "Aruzhan"]
scores = [80, 90, 85]

# Enumerate
for i, name in enumerate(names):
    print(i, name)

# Zip
for name, score in zip(names, scores):
    print(name, score)


# Enumerate + zip(combination)
for i, (name, score) in enumerate(zip(names, scores)):
    print(i, name, score)