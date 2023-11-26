UPLOAD_FOLDER = 'uploads'
EXTRACTED_TEXT_FOLDER = 'extracted_text'
CAPABILITY_TEXT_FOLDER = 'capabilities/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
OPENAI_MODEL = "gpt-3.5-turbo-1106"



####PROMPT CONFIGS


extract_capabilities_from_texts_prompt = f"""
    As an expert enterprise architect and computer scientist, your task is to analyze a given text and extract key business capabilities. 
    These capabilities should be structured into a JSON format, reflecting a hierarchical capability map based on the LeanIX reference model. 
    Here are the specific guidelines:

    Identify Critical Business Capabilities: Focus on identifying business capabilities that are most critical to the operations of the business. 
    These should reflect the core business areas or main categories of capabilities.
    Examples are, Strategic Management, Customer Management, Product Development.
    Make sure the naming of the capabilities goes have this structure like above mentioned: <Topic> <Definition of area>

    Structure the Hierarchy:

    Level 0 Capabilities: These should represent the core business areas or main categories.
    Level 1 Capabilities: These are more specific capabilities that detail the main categories.
    Level 2 Capabilities: At this level, break down the Level 1 capabilities into even more specific functions or activities.
    Avoid Overlapping Capabilities: Ensure that the capabilities identified do not overlap and each capability is distinct and clearly defined.

    Make sure that the same theme or area of capabilities can be found under the same root.

    Create a JSON Structure: Structure the extracted capabilities into a JSON format as shown below. Ensure the JSON syntax is correct and there are no errors.

    {{
    "capabilities": [
        {{
        "name": "Customer Management",
        "level": "0",
        "subCapabilities": [
            {{
            "name": "Customer Definition",
            "level": "1",
            "subCapabilities": [    
                {{
                "name": "Customer Segmentation",
                "level": "2"
                }}
            ]
            }}
        ]
        }}
        {{
        "name": "Product Management",
        "level": "0",
        "subCapabilities": [
            {{
            "name": "Product Development",
            "level": "1",
            "subCapabilities": [
                {{
                "name": "Product Design",
                "level": "2"
                }}
            ]
            }}
        ]
        }}
    ]
    }}
    Text Analysis: Please analyze the following text to extract business capabilities and create a capability map in the JSON format mentioned above. Return just the JSON message
    """


improve_capability_map_prompt = f"""
    Take on the role of an enterprise architect, evaluate the following capability map and 
    create a new enhanced and better version of the capability map. 
    Make sure that the same theme or area of capabilities can be found under the same root.
    Return just the JSON message
    """
