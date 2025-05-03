import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = client.responses.create(
    model='gpt-4.1-mini',
    input='How many "R"s are there in the word "strawberry"?'
)



print(response.output_text)