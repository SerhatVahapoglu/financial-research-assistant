import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader

def load_and_parse_document(file_path: str):
    """
    Dosyanın uzantısına göre doğru yükleyiciyi seçer ve dokümanı döndürür.
    """
    _, ext = os.path.splitext(file_path)
    
    print(f"📄 İşleniyor: {file_path}")
    
    if ext.lower() == '.pdf':
        loader = PyPDFLoader(file_path)
        return loader.load()
    
    elif ext.lower() == '.txt':
        # TextLoader ham metni olduğu gibi okur. 
        # SEC dosyaları bazen SGML tag'leri içerir ama GPT-4o bunları mükemmel temizler.
        loader = TextLoader(file_path, encoding='utf-8')
        return loader.load()
    
    else:
        print(f"⚠️ Desteklenmeyen dosya formatı: {ext}")
        return []