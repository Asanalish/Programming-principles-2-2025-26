# Reading from files

f = open("data.txt", "r")
print(f.read())  # reads whole file
f.close()

# Readline
f = open("data.txt", "r")
print(f.readline())  # first line
print(f.readline())  # second line
f.close()

# Readlines
f = open("data.txt", "r")
lines = f.readlines()  # list of lines
f.close()

print(lines)

# Loop through
for i, line in enumerate(lines):
    print(i, line.strip())