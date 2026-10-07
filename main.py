import os
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Define the expected output
class Classification(BaseModel):
    category: str
    confidence: float = Field(ge=0, le=1)
    answer: str


# Input Guardrail
def validate_input(message):
    if not message.strip():
        raise ValueError("Message cannot be empty.")

    if len(message) > 1000:
        raise ValueError("Message is too long.")

    return message.strip()


# Load System Prompt
def load_prompt():
    path = Path(__file__).parent / "prompts" / "system_prompt.txt"
    return path.read_text(encoding="utf-8")


# Call the LLM
def classify_message(message):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY in .env")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b" ,
        messages=[
            {"role": "system", "content": load_prompt()},
            {"role": "user", "content": message}
        ],
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content


# Main Function
def main():
    message = input("Enter a customer message: ")

    message = validate_input(message)

    raw_result = classify_message(message)

    # Parse and validate the JSON response
    data = json.loads(raw_result)
    result = Classification.model_validate(data)

    print("\nResult:")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()