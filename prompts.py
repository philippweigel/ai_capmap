import utils

####PROMPT CONFIGS

level_1_capabilities = utils.get_capabilities_from_sample_data_as_reference(tier = 1, level = 1)
level_2_capabilities = utils.get_capabilities_from_sample_data_as_reference(tier = 1, level = 2)

# Format capabilities into a string
level_1_capabilities = ', '.join(level_1_capabilities)
level_2_capabilities = ', '.join(level_2_capabilities)

extract_capabilities_from_text_chunk = f"""
    Take the role as an expert enterprise architect.
    You will be provided a text where you need to identify the most critical business architecture capabilities.
    Take the following capabilities as a reference:  {level_1_capabilities} {level_2_capabilities}
    Make sure that the capabilities are translated into english
    Provide the extracted capabilities in a clear, bullet-point format and return only the capabilities without context.
    If no capabilities can be identified, then return nothing.
    Text: <inserted text>
"""

apply_filter_referenced_capabilities= f"""
    Now go through all the chat responses above
    Note that tiers mean the following: Tier 1 = Strategic Capabilities, Tier 2 = Operational Capabilities, Tier 3 = Supporting Capabilities
"""

add_capabilities_to_most_relevant_capabilities= f"""
    Now go through all the relevant capabilities and create level 2 capabilities for each capability
    Here are the level 2 capabilities you should take as a reference: {level_2_capabilities}
    Please be aware that the tier level is determined by the capability from which it is derived.
    Make sure that the level 2 capabilities do not have the same name as the level 1 capability
"""

create_capability_map = f"""
    As an expert enterprise architect, your task is to analyze the listed business capabilities. 
    These capabilities should be structured into a JSON format, reflecting a hierarchical capability map. 

    Create a JSON Structure: Structure the extracted capabilities into a JSON format as shown below. Ensure the JSON syntax is correct and there are no errors.
    Example:
    {{
    "capabilities": [
        {{
        "name": "Brand Management",
        "level": "1",
        "tier": 1,
        "subCapabilities": [
            {{
            "name": "Brand Definition",
            "level": "2",
            "tier": 1,
            }},
            {{
            "name": "Brand Portfolio Management",
            "level": "2",
            "tier": 1
            }}
        ]
        }}
        {{
        "name": "Customer Management",
        "level": "1",
        "tier": 2,
        "subCapabilities": [
            {{
            "name": "Customer Definition",
            "level": "2",
            "tier": 2,
            }},
            {{
            "name": "Customer Matching",
            "level": "2",
            "tier": 2,
            }}
        ]
        }}
    ]
    }}
    Return just the JSON message
    """
