UPLOAD_FOLDER = 'uploads'
EXTRACTED_TEXT_FOLDER = 'extracted_text'
CAPABILITY_TEXT_FOLDER = 'capabilities/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
OPENAI_MODEL = "gpt-3.5-turbo-1106"



####PROMPT CONFIGS

extract_capabilities_from_texts_prompt = f"""
    Here are the rules:
    Ensure first level of business capabalities reflect the most critical to operations
    Avoid overlapping capabilities
    Aim to make your categories reflect key aspects of what the business actually does.
    Return the message in JSON format with this structure:

    "capabilities": [
    
      "name": "Customer Management",
      "level": 0,
      "subCapabilities": 
    
    Make sure that there are no json syntax error


    The map should reflect the hierarchical structure of these capabilities, 
    taking into account of this structure:

    Level 0: This level contains the core business areas or main categories of capabilities. Examples could be "customer management", "product development" or "operations and logistics".
    Level 1: This level further details the main categories into more specific capabilities. For example, "Customer Management" could be broken down into "Customer Acquisition", "Customer Care" and "Customer Feedback Management".
    Level 2: These levels break down the capabilities further into even more specific functions or activities. The focus here is on the level of detail and the mapping of specific functions or processes.
    Please extract business capabilities from the following text:
    """


clean_texts_from_pdf_prompt = 'Bitte nur Rechtschreibfehler und Grammatikfehler vom folgenden Text ausbessern'


generate_capability_map_from_capabilities_prompt = f"""
    "Can you please create a capability map based on the LeanIX reference model? 
    The map should reflect the hierarchical structure of these capabilities, 
    taking into account of this structure:

    Level 0: This level contains the core business areas or main categories of capabilities. Examples could be "customer management", "product development" or "operations and logistics".
    Level 1: This level further details the main categories into more specific capabilities. For example, "Customer Management" could be broken down into "Customer Acquisition", "Customer Care" and "Customer Feedback Management".
    Level 2: These levels break down the capabilities further into even more specific functions or activities. The focus here is on the level of detail and the mapping of specific functions or processes.

    The capabilities have been extracted from a text and include the following capabilities, please put divide these categories into level 0 first: 

    """

reformat_capability_map_prompt = f"""
Reformat and prepare the integrated capabilities so that it can be visualized with networkx 
"""
