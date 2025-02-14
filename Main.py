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
    return input("Enter a topic to learn about (or 'quit' to exit): ")

def run(topic_name):
    api_client = Groq()
    instructor_client = instructor.from_groq(api_client, mode=instructor.Mode.JSON)

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
        if topic_input.lower() == 'quit':
            break
        run(topic_input)