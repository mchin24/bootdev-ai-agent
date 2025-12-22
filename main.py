import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if api_key == None:
    raise RuntimeError("GEMINI_API_KEY is not set in the environment variables.")

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
        config=types.GenerateContentConfig(system_instruction = system_prompt)
    )

    # Output response
    if response.usage_metadata == None:
        raise RuntimeError("Response usage metadata is None.")
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens:{response.usage_metadata.candidates_token_count}")

    print(response.text)


if __name__ == "__main__":
    main()
