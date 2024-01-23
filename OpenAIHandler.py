import prompts
import openai
import utils
import constants

model = constants.OPENAI_MODEL

def send_prompt(instructions, input):
    # Define the base message structure
    base_message = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": input}
    ]

    response_format = { "type": "text" }

    # Use the textarea values instead of config values
    if instructions == "create capability map":
        base_message = []
        base_message.append({"role": "system", "content": "Take the role as an expert enterprise architect"})
        base_message.append({"role": "user", "content": "Here are the capabilities:" + input})
        base_message.append({"role": "user", "content": "please translate the capabilities into english"})
        base_message.append({"role": "user", "content": utils.clean_text(prompts.apply_filter_referenced_capabilities)})        
        base_message.append({"role": "user", "content": utils.clean_text(prompts.add_capabilities_to_most_relevant_capabilities)})
        base_message.append({"role": "user", "content": utils.clean_text(prompts.create_capability_map)})
        response_format = {"type": "json_object"}

    # 
    # if instructions == "check_text_grammar_and_spelling":
    #     base_message = []
    #     base_message.append({"role": "system", "content": "Be a helpful assistant"})
    #     base_message.append({"role": "user", "content": f"""
    #                          Please review the text for grammar and spelling errors and provide the corrected version with all 
    #                          grammar and spelling issues resolved. When reviewing the text, do not return a translated text. 
    #                          Here is:""" + input})
    #     response_format = {"type": "text"}

        
    # Handle unknown instructions
    if not base_message:
        return "Instructions not known"

    try:
        response = openai.chat.completions.create(
        model=model,
        messages=base_message,
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format=response_format,
        seed=1
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        return None
        # This code is for v1 of the openai package: pypi.org/project/openai
