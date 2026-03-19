import shutil
import os

# copy file
shutil.copy("data.txt", "backup.txt")
print("File copied")

# create temp file
f = open("temp.txt", "w")
f.write("temp")
f.close()

# delete safely
# Check if file exists before deleting
if os.path.exists("data_backup.txt"):
    os.remove("data_backup.txt")
else:
    print("File not found")

# Move (rename) a file
shutil.move("data.txt", "archive/data_old.txt")