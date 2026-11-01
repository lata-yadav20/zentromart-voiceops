import os
import glob
import chromadb
import re

class KnowledgeBase:
    def __init__(self, kb_dir="kb", db_path="./chroma_db"):
        self.kb_dir = kb_dir
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="zentromart_policies")
        
    def ingest_documents(self):
        files = glob.glob(f"{self.kb_dir}/*.md")
        documents, metadatas, ids = [], [], []
        
        for file in files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split strictly by [SECTION-ID] tags
            sections = re.split(r'(?=## \[[A-Z0-9-]+\])', content)
            
            for i, chunk in enumerate(sections):
                chunk = chunk.strip()
                if not chunk:
                    continue
                
                # Extract section ID if present
                match = re.search(r'## \[([A-Z0-9-]+)\]', chunk)
                section_id = match.group(1) if match else f"{os.path.basename(file)}_part_{i}"
                
                documents.append(chunk)
                metadatas.append({"source": os.path.basename(file), "section_id": section_id})
                ids.append(section_id)
                
        if documents:
            try:
                self.collection.delete(ids=ids) # Clear old chunks
            except:
                pass
            self.collection.add(documents=documents, metadatas=metadatas, ids=ids)
        print(f"Ingested {len(documents)} policy chunks into the vector database.")

    def retrieve(self, query, n_results=3):
        results = self.collection.query(query_texts=[query], n_results=n_results)
        if results['documents']:
            return "\n\n".join(results['documents'][0])
        return ""