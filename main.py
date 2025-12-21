import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if api_key == None:
    raise RuntimeError("GEMINI_API_KEY is not set in the environment variables.")

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument('user_prompt', type=str, help='User prompt')
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents= args.user_prompt
    )

    if response.usage_metadata == None:
        raise RuntimeError("Response usage metadata is None.")
    
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens:{response.usage_metadata.candidates_token_count}")
    print(response.text)


if __name__ == "__main__":
    main()
