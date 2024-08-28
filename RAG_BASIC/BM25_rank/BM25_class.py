import warnings
warnings.filterwarnings("ignore")

import bm25s
from typing import List, Any
import spacy
import Stemmer


class BM25_score:
    '''
        Methods:
        Robertson et al. (method="robertson")
        ATIRE (method="atire")
        BM25L (method="bm25l")
        BM25+ (method="bm25+")
        Lucene (method="lucene")
    
    '''
    def __init__(self, corpus:List[str]=None, path_load:str=None,load:bool=False, method: str="bm25+" , load_corpus:bool=True)->None:
        self.stemmer = Stemmer.Stemmer("spanish")
        self.nlp = spacy.load("es_dep_news_trf")
        if load == False:
            if not corpus:
                raise TypeError("To create new retriever please add corpus")
            if not method:
                raise TypeError("Add a method to use, Robertson, ATIRE, BM25L, BM25, Lucene")
            
            # optional: create a stemmer
            
            text_cleaned = self.clean_text(corpus)
        
            corpus_tokens = bm25s.tokenize(text_cleaned, stemmer=self.stemmer)
            self.retriever = bm25s.BM25(corpus=corpus, method=method)
            self.retriever.index(corpus_tokens)
        else:
            if not path_load:
                raise TypeError("Add path from the retriever you want to load")
            self.retriever= bm25s.BM25.load(path_load, load_corpus=load_corpus)
        

    def __search__(self, query:str, k:int=5)-> (Any, Any) :
        query = [query]
        text_cleaned = self.clean_text(query)
        query_tokens = bm25s.tokenize(text_cleaned, stemmer=self.stemmer)
        docs, scores = self.retriever.retrieve(query_tokens, k=k)
        return docs, scores
    

    
    def save(self, path:str='./BM25_retriever')-> str:
        self.retriever.save(path)
        print(f"Retriever Saved in {path}")

    def clean_text(self, corpus: List[str])-> List[str]:
        if not corpus:
            raise TypeError("Please pass the corpus information")

        txt = []
        for i in corpus:
            doc = self.nlp(i)
            filtered_tokens = [token.text for token in doc if 
                    not token.is_stop  #delete stop words
                    and not token.is_punct # delete punctuation
                    and not token.is_space] # delete space
            sentence = " ".join(filtered_tokens) 
            txt.append(sentence)
        return txt


        
    