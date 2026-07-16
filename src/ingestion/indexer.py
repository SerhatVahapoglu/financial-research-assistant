import os
import time
from langchain_huggingface import HuggingFaceEmbeddings # YENİ IMPORT
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.http.models import Filter
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
client = QdrantClient(url=QDRANT_URL)

# YENİ LOCAL EMBEDDING MODELİ
print("⏳ Local Embedding modeli yükleniyor (İlk çalışmada modeli indirir)...")
# Sadece bu satırı değiştiriyoruz: 'mps' parametresi M1 GPU'sunu tetikler!
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={'device': 'mps'}  # <-- Mac M1/M2/M3'ler için sihirli kelime
)

def index_documents(chunks, collection_name: str):
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            # BOYUT 1536'dan 384'e DÜŞTÜ (BGE-Small için boyut budur)
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        print(f"🆕 '{collection_name}' koleksiyonu oluşturuldu (Boyut: 384).")

    print(f"Veriler {len(chunks)} parça halinde indeksleniyor (Batch işlemi)...")
    
    batch_size = 50  # Artık API limiti olmadığı için batch boyutunu büyütebiliriz!
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
    )
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"   - {i} ile {i + len(batch)} arası parçalar yükleniyor...")
        vector_store.add_documents(batch)
        # Kendi makinemizi kullandığımız için time.sleep(0.5)'i silebiliriz veya çok kısaltabiliriz.
        
    print("✅ Tüm veri seti başarıyla batch halinde indekslendi!")

def retrieve_documents(query: str, collection_name: str, k: int = 10, qdrant_filter: Filter = None):
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
    )
    
    if qdrant_filter:
        print(f"🔍 Uygulanan filtre ile arama yapılıyor...")
        return vector_store.similarity_search(query, k=k, filter=qdrant_filter)
    
    return vector_store.similarity_search(query, k=k)