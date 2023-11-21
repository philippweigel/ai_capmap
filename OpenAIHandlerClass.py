import config
import os
import openai


model = config.OPENAI_MODEL

class OpenAIHandler:

    def __init__(self, input):
        self.input = input

    def extract_capabilities_from_extracted_texts(self):
        return self.send_prompt(config.extract_capabilities_from_texts_prompt)
    
    def generate_capability_map(self):
        return self.send_prompt(config.generate_capability_map_from_capabilities_prompt)
    

    def send_prompt(self, instructions):
        full_prompt = f"{instructions} {self.input}"
        try:
            response = openai.chat.completions.create(
            model=model,
            messages=[
                {
                "role": "system",
                "content": full_prompt
                }
            ],
            temperature=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error communicating with OpenAI: {e}")
            return None
            # This code is for v1 of the openai package: pypi.org/project/openai
