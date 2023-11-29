from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
import OpenAIHandler
import openai
import os
from dotenv import load_dotenv
import config
import utils
import logging
import pandas as pd


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')





load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


tier_1_capabilities = utils.get_capabilities_from_sample_data(1)
tier_2_capabilities = utils.get_capabilities_from_sample_data(2)
tier_3_capabilities = utils.get_capabilities_from_sample_data(3)

ref_capabilities = utils.get_capabilities_from_sample_data_as_reference()

# Format capabilities into a string
tier_1_capabilities = ', '.join(tier_1_capabilities)
tier_2_capabilities = ', '.join(tier_2_capabilities)
tier_3_capabilities = ', '.join(tier_3_capabilities)

ref_capabilities = ', '.join(ref_capabilities)

print(ref_capabilities).head()
