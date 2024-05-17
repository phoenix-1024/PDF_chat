from dotenv import load_dotenv
from google import generativeai as genai
import os
from llama_index import (
    VectorStoreIndex,
    Document
)
from llama_index import ServiceContext
from llama_index.llms import Gemini
from llama_index import SimpleDirectoryReader


load_dotenv()

genai.configure()

model = genai.GenerativeModel('gemini-pro')

class chat_pdf:
    service_context = ServiceContext.from_defaults(llm=Gemini(api_key=os.environ['GOOGLE_API_KEY']),embed_model="local:sentence-transformers/all-MiniLM-L12-v2")
    
    def __init__(self,):
        self.reader = SimpleDirectoryReader(input_dir="doc")
        self.reload()
        
    
    def reload(self,):
        self.documents = self.reader.load_data()
        index = VectorStoreIndex.from_documents(
            self.documents,service_context=self.service_context
            )

        self.chat_engine = index.as_chat_engine(
            service_context=self.service_context
            )

    def get_document_names(self,):
        names = [doc.metadata['file_name'] for doc in self.documents]
        names_str = ''
        for i,name in enumerate(names):
            names_str += f"{i}. {name} \n"
        return names_str
    
    def doc_chat(self,message):
        if len(self.documents) == 0:
            return "please upload a document to start chatting"
        else:
            response = self.chat_engine.chat(message).response
            return response

