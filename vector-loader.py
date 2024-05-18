# Import Essential dependencies
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Create a new file named vectorstore in your current directory.
if __name__=="__main__":
    DB_FAISS_PATH = 'vectorstore/db_faiss'
    loader = PyPDFLoader("./data/SE-confluence.pdf")
    docs = loader.load()

    # Ensure that docs is a list of objects with a 'page_content' attribute
    if not all(hasattr(doc, 'page_content') for doc in docs):
        print("Error: All documents must have a 'page_content' attribute.")
        exit(1)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings(api_key="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"))
    vectorstore.save_local(DB_FAISS_PATH)
    embeddings = OpenAIEmbeddings(api_key="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")
    # Load the vectorstore with allow_dangerous_deserialization set to True
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)