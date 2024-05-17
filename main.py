from fastapi import FastAPI,UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chat_pdf import chat_pdf


app = FastAPI()
gen_chat = chat_pdf()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Document(BaseModel):
    link: str

class Chat(BaseModel):
    query: str
    # history: li+st

@app.post("/chat")
async def chat(chat: Chat):
    response = gen_chat.doc_chat(chat.query)
    return {"response": response}

@app.get("/reload")
async def reload():
    gen_chat.reload()
    return {"response": "reloaded"}

@app.get("/get-document_names")
async def get_document_names():
    return {"response": gen_chat.get_document_names()}
