import warnings
warnings.filterwarnings("ignore")

from typing import List, Any
from unstructured.partition.auto import partition
import os
import gzip
import pickle
from tqdm import tqdm



class readFile:
    def __init__(self, 
                 filename:str, 
                 strategy:str="hi_res",
                 extract_images_in_pdf: bool = True,
                 extract_image_block_types: List[str]=["Image", "Table"],
                 extract_image_block_to_payload:bool = False,
                 extract_image_block_output_dir : str="cropped_images_spa",
                 languages: List[str]=["eng"]
                 ) -> None:
            
        self.config = {}
            
        if filename == "":
            raise TypeError("filename is empty.")
        self.config["filename"] = filename
        self.config["strategy"] = strategy
        if extract_images_in_pdf:
            if extract_image_block_output_dir == "":
                raise TypeError("Please, enter directory where to save the images and tables to extract.")
            self.config["extract_images_in_pdf"] = extract_images_in_pdf
            self.config["extract_image_block_types"] = extract_image_block_types
            self.config["extract_image_block_to_payload"] = extract_image_block_to_payload
            self.config["extract_image_block_output_dir"] = extract_image_block_output_dir
        self.config["languages"] = languages  

    def __call__(self) -> Any:
        original_extracted = partition( **self.config) 
        sorted_data_extracted = self.extract_data_from_unstructured(original_extracted)
        self.save_data_structure(data=sorted_data_extracted)
        return original_extracted, sorted_data_extracted

    
    def extract_data_from_unstructured(self, data: List) -> List:
        print("--------------- Extract Data ---------------")
        start_flag = bool(True)
        page_numer = int(0)
        new_data_obj = Any
        new_data = list([])
        
        for i in tqdm(range(len(data))):
             #extract text no images nor tables
            if data[i].category !=  "Image" or data[i].category !=  "Table":
                metadata = data[i].metadata.to_dict()
                   
                if start_flag:
                    page_numer = metadata["page_number"]
                    new_data_obj = {
                        "page_number": metadata["page_number"],
                        "text": data[i].text,
                        "language": metadata["languages"],
                        "source": metadata['filename'],
                        "form_id": self.config["filename"][self.config["filename"].rindex('/') + 1:self.config["filename"].rindex('.')] # extract form id
                    }
                    start_flag = False
            
            if page_numer == metadata["page_number"]:
                new_data_obj["text"]+= f"\n{data[i].text}"
            else:
                new_data.append(new_data_obj) # save data
                new_data_obj = {
                    "page_number": metadata["page_number"],
                    "text": data[i].text,
                    "language": metadata["languages"],
                    "source": metadata['filename'],
                    "form_id": self.config["filename"][self.config["filename"].rindex('/') + 1:self.config["filename"].rindex('.')]
                }
                page_numer = metadata["page_number"]

            if i == len(data)-1:
                new_data.append(new_data_obj)

            self.filename = metadata['filename']
        return new_data
    
    
    def create_directory_if_not_exists(self, directory_path: str) -> None:
        os.makedirs(directory_path, exist_ok=True)
        print(f"Directory '{directory_path}' is created or already exists.")
    
    def save_data_structure(self, data:List, save_flag:bool=True,  directory_path:str='./data_extracted')-> None:
        if save_flag == False:
            return
        self.create_directory_if_not_exists(directory_path)
        file = self.filename.split('.')[0]
        path = os.path.join(directory_path, file)
        with gzip.open(f'{path}.pickle.gz', 'wb') as f:
            pickle.dump(data, f)