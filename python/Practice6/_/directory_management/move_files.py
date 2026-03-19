import shutil
import os

# Create Folders
os.makedirs("copy", exist_ok=True)
os.makedirs("move", exist_ok=True)

# Copy file
shutil.copy("data.txt", "copy/data_copy.txt")
print("File copied")

# Move file
shutil.move("copy/data_copy.txt", "move/data_moved.txt")
print("File moved")

# Check
print("Original exists:", os.path.exists("data.txt"))
print("Moved exists:", os.path.exists("move/data_moved.txt"))