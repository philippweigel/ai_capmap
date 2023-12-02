import utils

UPLOAD_FOLDER = 'uploads'
EXTRACTED_TEXT_FOLDER = 'extracted_text'
CAPABILITY_TEXT_FOLDER = 'capabilities/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
OPENAI_MODEL = "gpt-3.5-turbo-1106"


####PROMPT CONFIGS

level_1_capabilities = utils.get_capabilities_from_sample_data_as_reference(tier = 1, level = 1)
level_2_capabilities = utils.get_capabilities_from_sample_data_as_reference(tier = 1, level = 2)

# Format capabilities into a string
level_1_capabilities = ', '.join(level_1_capabilities)
level_2_capabilities = ', '.join(level_2_capabilities)

extract_capabilities_from_text_chunk_prompt = f"""
    Take the role as an expert enterprise architect.
    You will be provided a text where you need to identify business capabilities.
    Focus on identifying business capabilities that are most critical to the operations of the business. 
    These should reflect the core business areas or main categories of capabilities.
    Make sure that the capabilities are translated into english
    Provide the extracted capabilities in a clear, bullet-point format and return only the capabilities without context.
    If no capabilities can be found, then return nothing.

    Text: <inserted text>
"""



create_capability_map_prompt = f"""
    As an expert enterprise architect, your task is to analyze the listed business capabilities. 
    These capabilities should be structured into a JSON format, reflecting a hierarchical capability map based on the LeanIX reference model. 
    Here are the specific guidelines:

    Focus on identifying business capabilities that are most critical to the operations of the business. 
    Structure the Hierarchy:

    Level 1 Capabilities: These should represent the core business areas or main categories. Examples are {level_1_capabilities}
    Level 2 Capabilities: These are more specific capabilities that detail the main categories. Examples are {level_2_capabilities}
    Avoid Overlapping Capabilities: Ensure that the capabilities identified do not overlap and each capability is distinct and clearly defined.

    Make sure that the same theme or area of capabilities can be found under the same root.

    Create a JSON Structure: Structure the extracted capabilities into a JSON format as shown below. Ensure the JSON syntax is correct and there are no errors.

    {{
    "capabilities": [
        {{
        "name": "Customer Management",
        "level": "1",
        "subCapabilities": [
            {{
            "name": "Customer Definition",
            "level": "2"
            }}
        ]
        }}
        {{
        "name": "Product Management",
        "level": "1",
        "subCapabilities": [
            {{
            "name": "Product Development",
            "level": "2",
            }}
        ]
        }}
    ]
    }}
    Return just the JSON message
    """

divide_capabilities_prompt=f"""Evaluate the following capability map and adjust the capability Map as neccessary.
If a capability covers multiple topics, try to divide it so that one capability covers only one topic
    Example: 
        Booking process and fleet management - Divide it into "Booking process management" and "Fleet management"
Return just the JSON message

Capability Map: <insert capability map>
"""

check_naming_of_capabilities_prompt = f"""Evaluate the following capability map and adjust the capability Map as neccessary.
    Here are the rules:

    Make sure the naming of the capabilities have this structure like this: <Topic> <Definition of area>
    Examples: 
        {level_1_capabilities}

    Return just the JSON message

    Capability Map: <insert capability map>
    """

aggregate_same_topic_prompt = f"""Evaluate the following capability map and adjust the capability Map as neccessary.
    Here are the rules:
    Make sure that the same theme or area of capabilities can be found under the same root.

    Return just the JSON message

    Capability Map: <insert capability map>
"""


instruction_prompt = f"""Try to improve the capability map
"""
