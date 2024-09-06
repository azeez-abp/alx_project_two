import os

current_path = os.path.abspath(__file__)

# Get the directory name of the current script (i.e., the root folder)
root_folder = os.path.dirname(current_path)
root_folder = str.replace(root_folder, "app", "")
