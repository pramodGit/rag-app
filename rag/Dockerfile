FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn langchain langchain-community langchain-openai langchain-text-splitters openai faiss-cpu pypdf tiktoken python-multipart

CMD ["uvicorn", "rag_service:app", "--host", "0.0.0.0", "--port", "8000"]
