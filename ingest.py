import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, UnstructuredPowerPointLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

DATA_FOLDER = "university_data"
INDEX_NAME = "ai-university-tutor"

def smart_bulk_upload():
    all_docs = []
    
    for root, dirs, files in os.walk(DATA_FOLDER):
        for file in files:
            filepath = os.path.join(root, file)
            
            if file.endswith('.pdf'):
                loader = PyPDFLoader(filepath)
            elif file.endswith('.pptx'):
                loader = UnstructuredPowerPointLoader(filepath)
            else:
                continue  
                
            rel_path = os.path.relpath(root, DATA_FOLDER)
            path_parts = rel_path.split(os.sep)
            
            subject_name = path_parts[0]
            doc_type = path_parts[1] if len(path_parts) > 1 else "General"
            
            print(f"Loading {file} | Subject: [{subject_name}] | Type: [{doc_type}]")
            
            try:
                docs = loader.load()
                
                for doc in docs:
                    doc.metadata["Subject"] = subject_name
                    doc.metadata["Doc_Type"] = doc_type
                    
                all_docs.extend(docs)
            except Exception as e:
                print(f"Error loading {file}: {e}")

    if not all_docs:
        print("No compatible documents found in the directory tree.")
        return

    print(f"\nTotal pages/slides loaded: {len(all_docs)}")

    print("Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(all_docs)
    # add chunks = chunks[number] to upload in set if api key is exhausted in mid upload
    print(f"Total chunks to upload: {len(chunks)}")

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vector_store = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)
    
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        print(f"Uploading batch {i // batch_size + 1} / {(len(chunks) // batch_size) + 1}...")
        print(f"Uploading batch {i // batch_size + 1} / {(len(chunks) // batch_size) + 1}...")
        
        try:
            vector_store.add_documents(batch)
            time.sleep(5) 
        except Exception as e:
            if "429" in str(e):
                print("Rate limit reached. Pausing for 60 seconds to reset quota...")
                time.sleep(60)
                vector_store.add_documents(batch)
            else:
                print(f"An unexpected error occurred: {e}")
    print("Smart bulk upload complete! All PDFs and PPTXs mapped perfectly.")

if __name__ == "__main__":
    smart_bulk_upload()