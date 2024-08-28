from tqdm.auto import tqdm
from RAG_BASIC.utils.utils import load_structure
from RAG_BASIC.chromadbClass.chromadb import Chromadb_Class
from RAG_BASIC.BM25_rank.BM25_class import BM25_score
from RAG_BASIC.utils.utils import save_structure

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


def ask_question(questions) -> None:

    llama31 = []
    llama3 = []
    phi3 = []

    for query in questions:

    
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
        

        output1 = ollama.generate(
            model="llama3",
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
        

        output2 = ollama.generate(
            model="phi3",
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
        

        llama31.append(output['response'])
        llama3.append(output1['response'])
        phi3.append(output2['response'])

    save_structure(data=llama31, path = './test_responses', file_name = 'llama31')
    save_structure(data=llama3, path = './test_responses', file_name = 'llama3')
    save_structure(data=phi3, path = './test_responses', file_name = 'phi3')
        
        
def main():
    question = [
        '¿Cuál es el objetivo del Código Orgánico de la Producción, Comercio e Inversiones?',
        '¿Qué se considera como actividad productiva según el COPCI?',
        '¿Quiénes están sujetos a la normativa del COPCI?',
        '¿Qué derechos se reconocen a los inversionistas según el COPCI?',
        '¿Cuál es la definición de "inversión productiva" en el COPCI?',
        '¿Qué incentivos fiscales generales establece el COPCI?',
        ' ¿Qué es el salario digno según el COPCI?',
        '¿Qué función cumple el Consejo Sectorial de la Producción según el COPCI?',
        '¿Cómo se clasifica la inversión según su origen en el COPCI? ',
        '¿Qué mecanismos establece el COPCI para la transformación de la matriz productiva? '

    ]

    ask_question(question)



    
    

if __name__ == "__main__":
    main()

    




'''
Pregunta: ¿Cuál es el objetivo del Código Orgánico de la Producción, Comercio e Inversiones? Respuesta: El objetivo es regular el proceso productivo en las etapas de producción, distribución, intercambio, comercio, consumo, manejo de externalidades e inversiones productivas orientadas a la realización del Buen Vivir.

Pregunta: ¿Qué se considera como actividad productiva según el COPCI? Respuesta: Se considera actividad productiva al proceso mediante el cual la actividad humana transforma insumos en bienes y servicios lícitos, socialmente necesarios y ambientalmente sustentables, incluyendo actividades comerciales y otras que generen valor agregado.

Pregunta: ¿Quiénes están sujetos a la normativa del COPCI? Respuesta: Están sujetos a esta normativa todas las personas naturales y jurídicas, y demás formas asociativas que desarrollen una actividad productiva en cualquier parte del territorio nacional.

Pregunta: ¿Qué derechos se reconocen a los inversionistas según el COPCI? Respuesta: Los derechos reconocidos incluyen la libertad de producción y comercialización de bienes y servicios, la libertad de importación y exportación, y el acceso a beneficios fiscales, entre otros.

Pregunta: ¿Cuál es la definición de "inversión productiva" en el COPCI? Respuesta: Se define como el flujo de recursos destinados a producir bienes y servicios, ampliar la capacidad productiva y generar fuentes de trabajo en la economía nacional.

Pregunta: ¿Qué incentivos fiscales generales establece el COPCI? Respuesta: Algunos incentivos incluyen la reducción progresiva del impuesto a la renta, exoneración del anticipo al impuesto a la renta por cinco años para inversiones nuevas, y deducciones adicionales para mejorar la productividad y la innovación.

Pregunta: ¿Qué es el salario digno según el COPCI? Respuesta: El salario digno mensual es aquel que cubre al menos las necesidades básicas de la persona trabajadora y su familia, determinado por el costo de la canasta básica familiar dividido por el número de perceptores del hogar.

Pregunta: ¿Qué función cumple el Consejo Sectorial de la Producción según el COPCI? Respuesta: El Consejo Sectorial de la Producción es el máximo órgano de rectoría gubernamental en materia de inversiones y desarrollo productivo.

Pregunta: ¿Cómo se clasifica la inversión según su origen en el COPCI? Respuesta: La inversión se clasifica en inversión nacional, realizada por personas o entidades ecuatorianas, e inversión extranjera, realizada por personas o entidades domiciliadas fuera del país.

Pregunta: ¿Qué mecanismos establece el COPCI para la transformación de la matriz productiva? Respuesta: El COPCI establece que el Estado fomentará la transformación de la matriz productiva mediante políticas que promuevan la inversión, el desarrollo de infraestructura, y la implementación de tecnologías de producción limpia.

'''