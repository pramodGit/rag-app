from fastapi import FastAPI, UploadFile, File
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI

app = FastAPI()

db_map = {}

@app.post("/upload")
async def upload_pdf(user_id: str, file: UploadFile = File(...)):
    file_path = f"{user_id}_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(chunks, embeddings)

    db_map[user_id] = db

    return {"message": "PDF processed"}

@app.post("/ask")
async def ask(user_id: str, q: str):
    db = db_map.get(user_id)

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

    llm = ChatOpenAI()
    res = llm.invoke(prompt)

    return {"answer": res.content}
