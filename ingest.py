import os
from dotenv import load_dotenv
from llama_index.readers.file import PyMuPDFReader
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Loading environment variables
load_dotenv()

# fething the Gemini API Key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Critical Error : GEMINI_API_KEY is missing from .env file or is incorrect")

# configuring settings for which model of gemini we are gonna use
# we are using gemini-2.5-pro for complex reasoning over text

Settings.llm = GoogleGenAI(
    model="gemini-2.5-flash",
    api_key= api_key,
    temperature = 0.2  # Low temperature makes the AI Strict and Factual
)
# We use a powerful, free local model to convert text to vectors!
# It will download the model automatically on the first run.
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

def run_pipeline():
    print("Initializing Ingestion Engine . . .")

    # read the document from the /data directory
    if not os.path.exists("./data") or not os.listdir("./data"):
        print("Error: The './data' directory is empty. Drop Your Documents in there.")
        return
    
    print("Reading documents from Storage . . .")
    parser = PyMuPDFReader()
    file_extractor = {".pdf": parser}
    reader = SimpleDirectoryReader(input_dir='./data', file_extractor=file_extractor)
    documents = reader.load_data()
    print(f"Loaded {len(documents)} pages successfully.")

    # Chuck the text, generate embeddings and building the vector index in memory

    print("Generating text embeddings and building the vector index...")
    index = VectorStoreIndex.from_documents(documents)
    print("Index Built Successfully")

    # Create a persistent Query Engine to chat with the data
    query_engine = index.as_query_engine()

    # Test query to verify everything works flawlessly
    print("\n🔬 Testing system with sample query...")
    test_query = "What are the rules regarding attendance or grading criteria?"
    print(f"User: {test_query}")

    response = query_engine.query(test_query)
    print(f"\nAI Assistant: \n{response}\n")

if __name__ == '__main__':
    run_pipeline()