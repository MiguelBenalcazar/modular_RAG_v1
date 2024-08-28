from tqdm.auto import tqdm
from RAG_BASIC.utils.utils import load_structure
from RAG_BASIC.chromadbClass.chromadb import Chromadb_Class
import os


path = './chunks_extracted'
list_chunks_dir = os.listdir(path)

data_acum = []
for i in tqdm(range(0, len(list_chunks_dir))):
    file = list_chunks_dir[i]
    path_file = os.path.join(path, file)
    chunk_data = load_structure(path = path_file)
    data_acum.append(chunk_data)

# Extract all items in `splits`
all_splits = list(map(lambda x: x['splits'], data_acum[0]))
all_splits_txt = ['\n'.join(i) for i in all_splits]
source = data_acum[0][0]['metadata']['source'].split('.')[0]


# current_path = os.getcwd()
# db_path = os.path.join(current_path, 'vector_db')
# model = "llama3.1"
# collection_name = "doc_test"

# db = Chromadb_Class(path=db_path, model=model, collection_name=collection_name)
# # db.add_data_collection(all_splits_txt)

# db.search_data_collection("¿Cuándo se realizó el segundo debate del Proyecto de Ley del Código Orgánico de la Producción, Comercio e Inversiones?")