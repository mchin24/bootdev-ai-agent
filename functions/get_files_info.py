import os

def get_files_info(working_directory, directory="."):
    try:
        working_abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_abs_path, directory))
        
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_abs_path, target_dir]) == working_abs_path
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.exists(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        outputs = ["Result for current directory:"]
        for item in os.listdir(target_dir):
            file_name = item
            file_size = os.path.getsize(os.path.join(target_dir, item))
            is_dir = os.path.isdir(os.path.join(target_dir, item))
            outputs.append(f'- File: {file_name}: file_size={file_size} bytes, is_dir={is_dir}')
        
        return "\n".join(outputs)
    except Exception as e:
        return f"Error: {str(e)}"