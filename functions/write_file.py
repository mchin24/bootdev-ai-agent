import os

def write_file(working_directory, file_path, content):
    try:
        working_abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_abs_path, file_path))
        
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_abs_path, target_file]) == working_abs_path
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        
        file = open(target_file, 'w')
        file.write(content)
        file.close()

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error: {str(e)}"
