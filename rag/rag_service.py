from fastapi import FastAPI, UploadFile, File
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
import os
import uuid

app = FastAPI()

db_map = {}

# ✅ Initialize local embeddings (FREE)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

@app.post("/upload")
async def upload_pdf(user_id: str, file: UploadFile = File(...)):
    try:
        file_path = f"{user_id}_{uuid.uuid4()}_{file.filename}"

        # Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Load PDF
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        # Split into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(docs)

        # Create vector DB (NO OpenAI here)
        db = FAISS.from_documents(chunks, embeddings)

        db_map[user_id] = db

        return {"message": "PDF processed successfully"}

    except Exception as e:
        print("Upload error:", str(e))
        return {"error": "Upload failed"}


@app.post("/ask")
async def ask(user_id: str, q: str):
    try:
        db = db_map.get(user_id)

        if not db:
            return {"answer": "No document uploaded"}

        # Retrieve relevant chunks
        docs = db.similarity_search(q, k=5)
        context = "\n\n".join([d.page_content for d in docs])

        prompt = f"""
Answer ONLY from the context.
If not found, say "Not found in document".

Context:
{context}

Question:
{q}
"""

        # ✅ OpenAI used ONLY here
        llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        res = llm.invoke(prompt)

        return {"answer": res.content if res else "No response"}

    except Exception as e:
        print("Ask error:", str(e))
        return {"answer": "Error processing request"}