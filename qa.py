
from dotenv import load_dotenv
from my_rag_lib.loaders import load_from_bytes
from my_rag_lib.chunkers import chunk_documents
from my_rag_lib.embeddings import get_embedder, build_vectorstore
from my_rag_lib.retrieval import Retriever
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from torch import chunk

load_dotenv()
llm = HuggingFaceEndpoint(
    repo_id="MiniMaxAI/MiniMax-M2.5",  # type: ignore
    task="text-generation"
)  # type: ignore

chat_model = ChatHuggingFace(llm=llm)

def process_and_index_file(file_bytes: bytes, file_name: str) -> Retriever:
    """
    Parses document bytes, creates chunks, embeds them into FAISS,
    and returns a ready-to-use Retriever instance.
    """
    # 1. Load document
    docs = load_from_bytes(file_bytes, file_name)

    # 2. Chunk document
    chunks = chunk_documents(
        docs, strategy="recursive", chunk_size=1000, chunk_overlap=300
    )

    # 3. Initialize embedder
    embedder = get_embedder(provider="huggingface_api")

    # 4. Build FAISS vector store
    vectorstore = build_vectorstore(chunks, embedder)

    # 5. Return configured Retriever object
    return Retriever(vectorstore=vectorstore, all_chunks=chunks)

def generalize_results(results: list) -> str:
    """
    Takes a list of retrieved chunks and formats them into a readable string.
    """
    response_chunks = "**Top Relevant Excerpts:**\n\n"
    for i, chunk in enumerate(results, start=1):
        response_chunks += f"**Excerpt {i}:**\n{chunk.page_content}\n\n"

    prompt = f"take these chunks and summarize them into a concise answer:\n\n{response_chunks}"

    return chat_model.invoke(prompt).content