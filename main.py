import os
import argparse
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if api_key == None:
    raise RuntimeError("GEMINI_API_KEY is not set in the environment variables.")

def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    match function_call.name:
        case "get_file_content":
            function_result = get_file_content('calculator', **function_call.args)
        case "get_files_info":
            function_result = get_files_info('calculator', **function_call.args)
        case "run_python_file":
            function_result = run_python_file('calculator', **function_call.args)
        case "write_file":
            function_result = write_file('calculator', **function_call.args)
        case _: 
            function_result = None

    if function_result is None:
        return types.Content(
            role="tool",
            parts = [
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Unknown function: {function_call.name}"}
                )
            ]
        )
    else:
        return types.Content(
            role="tool",
            parts = [
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"result" : function_result}
                )
            ]
        )

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument('user_prompt', type=str, help='User prompt')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()

    # Add user prompt to messages content
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # Initialize the GenAI client, generate content
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents= messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt)
    )

    # Output response
    if response.usage_metadata == None:
        raise RuntimeError("Response usage metadata is None.")
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens:{response.usage_metadata.candidates_token_count}")

    responses = []
    if response.function_calls is not None:
        for function_call in response.function_calls:
            function_response = call_function(function_call, args.verbose)

            if not function_response.parts[0].function_response.response:
                raise RuntimeError("Function response is empty.")
            
            responses.append(function_response.parts[0])

            if args.verbose:
                print(f"-> {function_response.parts[0].function_response.response}")
            return None

    print(response.text)


if __name__ == "__main__":
    main()
