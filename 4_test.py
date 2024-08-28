from tqdm.auto import tqdm
from RAG_BASIC.utils.utils import load_structure
from RAG_BASIC.chromadbClass.chromadb import Chromadb_Class
from RAG_BASIC.BM25_rank.BM25_class import BM25_score
import os
from sentence_transformers import CrossEncoder
import ollama

current_path = os.getcwd()
db_path = os.path.join(current_path, 'vector_db')
model = "llama3.1"
collection_name = "doc_test"

k_items = 5
bm25 = BM25_score(load=True, path_load='./BM25_retriever')

n_results = 10
db = Chromadb_Class(path=db_path, model=model, collection_name=collection_name)



def ask_question() -> None:
    while True:
        query = input("Please write your question (or type 'exit' to quit): ")
        
        if query.lower() == 'exit':
            print("Exiting the RAG simulation. Goodbye!")
            break

    
        retrieval_vector_db = db.search_data_collection(query, n_results=n_results)
        retrieval_vector_db_documents = retrieval_vector_db['documents'][0]


        retrieval_bm25 =bm25.__search__(query=query, k=k_items)
        retrieval_bm25_documents  = [item['text'] for item in retrieval_bm25[0][0]]

        retrieval_vector_db_documents.extend(retrieval_bm25_documents) 
        rerank_data = [(query, doc) for doc in retrieval_vector_db_documents]

        
        model = CrossEncoder('cross-encoder/ms-marco-TinyBERT-L-2', max_length=512)
        scores = model.predict(rerank_data) 

        filter_min_score =0.2
        documents_and_scores = [(retrieval_vector_db_documents[i], scores[i]) for i in range(len(retrieval_vector_db_documents)) if scores[i] > filter_min_score]

        # Sort the list by scores in descending order (higher scores first)
        sorted_documents_and_scores = sorted(documents_and_scores, key=lambda x: x[1], reverse=True)

        # Print the documents in order from better to worse based on their scores
        doc = []
        for document, score in sorted_documents_and_scores:
            doc.append(document)


        output = ollama.generate(
            model="llama3.1",
            prompt=f"""Basándote ÚNICAMENTE en la siguiente información (organizada de más a menos importante): {doc}

                       Responde a esta pregunta: {query}

                       Instrucciones:
                       - Usa SOLO la información proporcionada arriba, priorizando la más relevante.
                       - La información está ordenada de más a menos importante.
                       - Si la información no contiene datos relevantes para la pregunta, responde 'No hay información disponible'.
                       - Proporciona la respuesta más breve y directa posible.
                       - No añadas explicaciones adicionales ni uses conocimientos externos.
                       - Responde en español."""
                       )
        

    
        
        print("RESULTS WITH FILTERED INFO")
        print(f'{query} \n answer : {output["response"]}')


        output = ollama.generate(
            model="llama3.1",
            prompt=f"""Basándote ÚNICAMENTE en la siguiente información (organizada de más a menos importante): {retrieval_vector_db_documents}

                       Responde a esta pregunta: {query}

                       Instrucciones:
                       - Usa SOLO la información proporcionada arriba, priorizando la más relevante.
                       - La información está ordenada de más a menos importante.
                       - Si la información no contiene datos relevantes para la pregunta, responde 'No hay información disponible'.
                       - Proporciona la respuesta más breve y directa posible.
                       - No añadas explicaciones adicionales ni uses conocimientos externos.
                       - Responde en español."""
                       )
        

        

        print("RESULTS WITH UNFILTERED INFO")
        print(f'{query} \n answer : {output["response"]}')
        

def main():
    ask_question()



    
    

if __name__ == "__main__":
    main()