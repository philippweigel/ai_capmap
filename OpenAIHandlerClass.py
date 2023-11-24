import config
import os
import openai


model = config.OPENAI_MODEL

class OpenAIHandler:

    def __init__(self, input):
        self.input = input

    def extract_capabilities_from_extracted_texts(self):
        return self.send_prompt(config.extract_capabilities_from_texts_prompt)
    
    def send_prompt(self, instructions):
        full_prompt = f"{instructions} {self.input}"
        instructions_for_system_prompt = config.extract_capabilities_from_texts_prompt
        improve_capability_map_prompt = config.improve_capability_map_prompt
        try:
            response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": instructions_for_system_prompt},
                {"role": "user", "content": self.input},
                {"role": "assistant", "content": improve_capability_map_prompt}
            ],
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={ "type": "json_object" },
            seed=1
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error communicating with OpenAI: {e}")
            return None
            # This code is for v1 of the openai package: pypi.org/project/openai
