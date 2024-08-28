import chromadb
from typing import Any, List
from tqdm.auto import tqdm
import os
from RAG_BASIC.encoder.embedding import Embeddings
# from encoder.embedding import Embeddings

class Chromadb_Class:
    def __init__(
            self, 
            path: str="",
            collection_name: str = "docs", 
            model:str="all-MiniLM-L6-v2"
            ):
        
        self.path  = path
        # os.makedirs(path, exist_ok=True)
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path=path)
        self.encoder = Embeddings(type = model)
        self.collection = self.client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})

    def _get_embeddings(self, documents:List[str])->List[float]:
        return  self.encoder(documents)


    def add_data_collection(self, document:List[str])-> None:
        embedded_document = self._get_embeddings(documents= document)
        

        for i in tqdm(range(0, len(embedded_document))):
            # print(embedded_document[i]['embedding'])
         
            self.collection.add(
                ids=str(i),
                embeddings=embedded_document[i]['embedding'],
                documents= document[i]
            )
    
    def search_data_collection(self, prompt:str, n_results:int=15)-> Any:
        query_embedding = self._get_embeddings(prompt)
        
        results = self.collection.query(
            query_embeddings = query_embedding[0]['embedding'],
            n_results = n_results,
            include = ['embeddings', 'documents']
        ) 

        return results  
    
    def get_documents(self):
        data = self.collection.get(include=['embeddings', 'documents']) 
        return data['documents'], data['embeddings']
