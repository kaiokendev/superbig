import requests
from ..base import Source
from lxml.html.clean import Cleaner
import unicodedata
import hashlib

class UrlSource(Source):
    def __init__(self, url=''):
        super().__init__()
        
        if len(url) > 1:
            self.set(url)
        
    def get(self) -> str:
        data = ''
        if self.contents is not None:
            data = self.contents
        
        response = requests.get(self.url, headers={"User-Agent": "SuperBIG"})
        
        if response.status_code == 200:
            data = self.sanitize(unicodedata.normalize('NFKC', response.text))
            hash = hashlib.md5(data.encode()).hexdigest()
            if self.cache_key != hash:
                self.invalidate(hash)
        else:
            print("Couldn't fetch resource")
            print(response)
            
        self.contents = data
        return super().get()
            
    def set(self, url: str):
        self.url = url
        super().set()
        
    def sanitize(self, dirty_html):
        cleaner = Cleaner(page_structure=True,
                    meta=True,
                    embedded=True,
                    links=True,
                    style=True,
                    processing_instructions=True,
                    inline_style=True,
                    scripts=True,
                    javascript=True,
                    comments=True,
                    frames=True,
                    forms=True,
                    annoying_tags=True,
                    remove_unknown_tags=True,
                    safe_attrs_only=True,
                    safe_attrs=frozenset(['src','color', 'href', 'title', 'class', 'name', 'id']),
                    remove_tags=('span', 'font', 'div', 'a'),
                    kill_tags=['svg', 'img', 'header']
                    )
        clean = str(cleaner.clean_html(dirty_html))
        return clean.replace('\t', '').replace('\r','')