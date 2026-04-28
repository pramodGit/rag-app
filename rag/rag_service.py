from fastapi import FastAPI, UploadFile, File
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama
import os
import uuid

app = FastAPI()

FAISS_DIR = "faiss_indexes"
os.makedirs(FAISS_DIR, exist_ok=True)

# ✅ Initialize local embeddings (FREE)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def get_index_path(user_id: str):
    return os.path.join(FAISS_DIR, user_id)

def load_db(user_id: str):
    path = get_index_path(user_id)
    if os.path.exists(path):
        return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    return None

@app.post("/upload")
async def upload_pdf(user_id: str, file: UploadFile = File(...)):
    try:
        file_path = f"{user_id}_{uuid.uuid4()}_{file.filename}"

        with open(file_path, "wb") as f:
            f.write(await file.read())

        loader = PyPDFLoader(file_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(docs)

        # ✅ Save FAISS index to disk
        db = FAISS.from_documents(chunks, embeddings)
        db.save_local(get_index_path(user_id))

        print(f"✅ Index saved for user: {user_id}")
        return {"message": "PDF processed successfully"}

    except Exception as e:
        print("Upload error:", str(e))
        return {"error": "Upload failed"}


@app.post("/ask")
async def ask(user_id: str, q: str):
    try:
        # ✅ Load from disk if not in memory
        db = load_db(user_id)

        if not db:
            return {"answer": "No document uploaded"}

        docs = db.similarity_search(q, k=8)
        context = "\n\n".join([d.page_content for d in docs])

        prompt = f"""
You are a resume analysis assistant. Extract and list information directly from the context.
Do NOT ask clarifying questions. Just answer directly based on the context.
If not found, say "Not found in document".

Context:
{context}

Question: {q}

Provide a direct, specific answer based only on the context above:
"""
        
        print("\n" + "="*60)
        print("📤 PAYLOAD SENT TO OLLAMA:")
        print("="*60)
        print(f"Question: {q}")
        print(f"Context chunks: {len(docs)}")
        print(f"Full prompt:\n{prompt}")
        print("="*60 + "\n")

        llm = ChatOllama(model="llama3.2")
        res = llm.invoke(prompt)

        print("📥 OLLAMA RESPONSE:")
        print(res.content)
        print("="*60 + "\n")

        return {"answer": res.content if res else "No response"}

    except Exception as e:
        print("Ask error:", str(e))
        return {"answer": "Error processing request"}