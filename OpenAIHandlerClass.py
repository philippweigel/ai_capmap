import config
import os
import openai


model = config.OPENAI_MODEL

class OpenAIHandler:

    def __init__(self, prompt):
        self.prompt = prompt

    def analyze_capabilities(self):
        """Spezifische Funktion zur Analyse von Unternehmens-Capabilities."""
        instructions = config.extract_capabilities_from_text_prompt
        # Implementierung der spezifischen Analyse
        response = self.send_prompt(instructions)
        return response
    
    def clean_text(self):
        instructions = config.clean_texts_from_pdf_prompt
        response = self.send_prompt(instructions)
        return response
    
    def generate_capability_map(self):
        instructions = config.generate_capability_map_from_capabilities_prompt
        response = self.send_prompt(instructions)
        return response
    
    def reformat_capability_map(self):
        instructions = config.reformat_capability_map_prompt
        response = self.send_prompt(instructions)
        return response
    

    def send_prompt(self, instructions):
        print(f"Instructions: {instructions}")
        print(f"Prompt: {self.prompt}")
        try:
            response = openai.chat.completions.create(
            model=model,
            messages=[
                {
                "role": "system",
                "content": f"{instructions} {self.prompt}"
                }
            ],
            temperature=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
            print(f"Choice from Open AI {response.choices[0].message.content}")
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error communicating with OpenAI: {e}")
            return None
            # This code is for v1 of the openai package: pypi.org/project/openai
