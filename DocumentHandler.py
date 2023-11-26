from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from OpenAIHandlerClass import OpenAIHandler
import openai
import os
from dotenv import load_dotenv
import config

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

text_loader_kwargs={'autodetect_encoding': True}
loader = DirectoryLoader(path="extracted_text/", glob="**/*.txt", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
documents = loader.load()

#print(documents[0])


text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
    add_start_index = True,
)


split_documents = text_splitter.split_documents(documents)


openai_handler = OpenAIHandler(split_documents[0].page_content)

print(openai_handler.get_embedding())

##TODO: Save the embedding for every chunck text into a vector database, then take the query of user convert it into a embedding and the find the answer to the query
