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
import tiktoken

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')





load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")



tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo-1106")
