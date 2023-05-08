from ..base import Chunker, Embedder, Collecter, InjectionPoint, Retriever, Injector, Source
from ..chunker import NaiveChunker
from ..embedder import SentenceTransformerEmbedder
from ..collector import ChromaCollector
from ..injector import GenericInjector

class PseudocontextProvider():
    def __init__(self,
                 prompt: str = '',
                 collector: Collecter | None = None, 
                 chunker: Chunker | None = None, 
                 retriever: Retriever | None = None, 
                 embedder: Embedder | None = None, 
                 injector: Injector | None = None,
                 chunk_len: int = 500, 
                 first_len: int = 300, 
                 last_len:int = 300):
        self.prompt = prompt
        self.chunker = chunker or NaiveChunker(chunk_len=chunk_len, first_len=first_len, last_len=last_len)
        self.embedder = embedder or SentenceTransformerEmbedder()
        self.collector = collector or ChromaCollector(self.embedder)
        self.injector = injector or GenericInjector(self.chunker, self.collector, self.embedder, {})
        
    def __enter__(self):
        return self.with_pseudocontext(self.prompt)
    
    def __exit__(self, type, value, trace):
        pass
    
    def add_source(self, injection_point_name: str, source: Source):
        self.injector.add_source(InjectionPoint(injection_point_name), source)
        
    def with_pseudocontext(self, prompt: str, auto_infer_sources={}):
        self.injector.auto_infer_settings = auto_infer_sources
        prepared_prompt = self.injector.prepare(prompt)
        new_prompt = self.injector.inject(prepared_prompt)
        return new_prompt