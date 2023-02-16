import openai
from util.config import openapi_key
def request_gpt(text):
    openai.api_key = openapi_key
    response = openai.Completion.create(
        prompt=text, 
        engine="text-davinci-003",
        max_tokens=1024,    
        temperature=0.3
    )
    return f"*{text}*\n{response.choices[0].text}"