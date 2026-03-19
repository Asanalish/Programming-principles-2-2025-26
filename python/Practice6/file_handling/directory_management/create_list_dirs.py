import os

# create folder
if not os.path.exists("folder1"):
    os.mkdir("folder1")
    print("folder1 created")

# nested folders
os.makedirs("a/b/c", exist_ok=True)
print("nested folders created")

# current dir
print(os.getcwd())

# change dir
os.chdir("folder1")
print(os.getcwd())

# go back
os.chdir("..")

# List files
files = os.listdir()
for f in files:
    print(f)

# Find .py files
for f in files:
    if f.endswith(".py"):
        print(f)

# Remove dir
os.mkdir("temp_folder")
os.rmdir("temp_folder")
print("temp_folder removed")