from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.readers.file import PyMuPDFReader
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
api_key = os.getenv("GEMINI_API_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)

Settings.llm = GoogleGenAI(
    model = "gemini-2.5-flash",
    api_key = api_key,
    temperature=0.2
)

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)
print("Loading documents into memory...")

parser = PyMuPDFReader()
documents = SimpleDirectoryReader(
    input_dir="./data",
    file_extractor={".pdf":parser}
).load_data()
index = VectorStoreIndex.from_documents(documents)

memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
chat_engine = index.as_chat_engine(
    chat_mode = "context",
    memory = memory,
    system_prompt =  "You are a helpful university assistant. Answer questions strictly based on the provided COMSATS handbook."
)
class QueryRequest(BaseModel):
    question:str


@app.post("/query")
def query_endpoint(request: QueryRequest):
    try:
        print(f"User: {request.question}")

        response = chat_engine.chat(request.question)

        print(f"Assistant:{response}")
        return {"answer": str(response)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port=8000)