# 1. Create file and write data

f = open("data.txt", "w")  # create file and overwrite if exists
f.write("Hello\n")
f.write("This is Python\n")
f.close()

print("File created and written")

# 2. Append new lines
f = open("data.txt", "a")  # add to end of file
f.write("New line 1\n")
f.write("New line 2\n")
f.close()

print("Data appended")

# 3. Verify content
f = open("data.txt", "r")
print(f.read())  # print whole file
f.close()