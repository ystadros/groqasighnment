import subprocess
import sys

libraries = [
    "pydantic",
    "groq",
    "instructor"
]

for library in libraries:
    subprocess.check_call([sys.executable, "-m", "pip", "install", library])

print("Libraries installed successfully!")

import os
from pydantic import BaseModel, Field  
from typing import List
from groq import Groq
import instructor

class TopicInfo(BaseModel):
    title: str
    details: List[str] = Field(..., description="Key facts about the topic")

def get_topic_input():
    return input("Enter a topic to learn about (or 'exit' to quit): ")

def run(topic_name):
    # Hardcoding the API key (Not recommended for production)
    api_key = "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"

    if not api_key:
        print("API Key is not set. Please set the GROQ_API_KEY environment variable.")
        return

    api_client = Groq(
        api_key=api_key,
    )

    instructor_client = instructor.from_groq(api_client, mode=instructor.Mode.TOOLS)

    response = instructor_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "user",
                "content": f"Tell me about {topic_name}",
            }
        ],
        response_model=TopicInfo,
    )

    print(response.model_dump_json(indent=2))

if __name__ == "__main__":
    while True:
        topic_input = get_topic_input()
        if topic_input.lower() == 'exit':
            break
        run(topic_input)






