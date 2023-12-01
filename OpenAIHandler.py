import config
import openai
import utils

model = config.OPENAI_MODEL

def send_prompt(instructions, input):
    # Define the base message structure
    base_message = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": input}
    ]

    response_format = { "type": "text" }

    # Modify the message based on specific instructions
    if instructions == config.create_capability_map_prompt:
        base_message.append({"role": "assistant", "content": utils.clean_text(config.divide_capabilities_prompt)})
        base_message.append({"role": "assistant", "content": utils.clean_text(config.check_naming_of_capabilities_prompt)})
        base_message.append({"role": "assistant", "content": utils.clean_text(config.aggregate_same_topic_prompt)})
        response_format = { "type": "json_object" }

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
