import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        working_abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_abs_path, file_path))
        
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_abs_path, target_file]) == working_abs_path
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if (not os.path.exists(target_file) or not os.path.isfile(target_file)):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        file = open(target_file, 'r')
        file_content = file.read(MAX_CHARS)
        if file.read(1):
            file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        file.close()
        return file_content
        
    except Exception as e:
        return f"Error: {str(e)}"
