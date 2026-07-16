import os
import time  # 1. Bunu ekle
from .file_parser import load_and_parse_document
from .chunker import chunk_markdown_documents
from .indexer import index_documents

def run_batch_ingestion(directory_path: str):
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf") or filename.endswith(".txt"):
            ticker = filename.split('_')[0]
            file_path = os.path.join(directory_path, filename)
            
            print(f"🚀 İşleniyor: {filename} (Ticker: {ticker})")
            
            docs = load_and_parse_document(file_path)
            chunks = chunk_markdown_documents(docs, metadata={"ticker": ticker, "doc_type": "10-K"})
            
            # 2. İndeksleme öncesi bir bekleme süresi ekleyelim
            print("⏳ OpenAI API limitine takılmamak için kısa bir ara veriliyor...")
            time.sleep(2)  # 2 saniye bekle
            
            index_documents(chunks, "financial_reports_collection")
            
    print("✅ Tüm veri seti başarıyla veritabanına aktarıldı!")