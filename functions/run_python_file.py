
import subprocess
import os
import google.genai.types as types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_abs_path, file_path))
        
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_abs_path, target_file]) == working_abs_path
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if (not os.path.exists(target_file) or not os.path.isfile(target_file)):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ['python', target_file]

        if args:
            command.extend(args)

        result = subprocess.run(command, capture_output=True, text=True, cwd=working_abs_path, timeout=30)

        outputs = []
        if result.returncode != 0:
            outputs.append(f"Process exited with code {result.returncode}")

        if not result.stdout.strip() and not result.stderr.strip():
            outputs.append("No output produced")

        if result.stdout.strip():
            outputs.append("STDOUT: " + result.stdout.strip())

        if result.stderr.strip():
            outputs.append("STDERR: " + result.stderr.strip())

        return "\n".join(outputs)

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the specified Python file, passing any arguments, and returns its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to target file, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Argumens to pass to the Python file as a list of strings",
            )
        },
    ),
)
