import os

def formatted_path(path_str):
    folder_name = os.path.basename(os.path.dirname(path_str))
    return folder_name.capitalize()
