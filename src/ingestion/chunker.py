from langchain_text_splitters import MarkdownTextSplitter

def chunk_markdown_documents(documents, metadata: dict, chunk_size: int = 2000, chunk_overlap: int = 200):
    """
    Döküman listesini tek bir metin haline getirip küçük parçalara böler.
    Hem LlamaParse (.text) hem de LangChain (.page_content) formatlarını destekler.
    """
    text_parts = []
    for doc in documents:
        # Gelen veri LlamaParse objesi ise:
        if hasattr(doc, 'text'):
            text_parts.append(doc.text)
        # Gelen veri LangChain objesi ise:
        elif hasattr(doc, 'page_content'):
            text_parts.append(doc.page_content)
        # Sadece düz metin gelmişse:
        elif isinstance(doc, str):
            text_parts.append(doc)
            
    full_text = "\n\n".join(text_parts)
    
    splitter = MarkdownTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    
    chunks = splitter.create_documents([full_text])
    
    # Her bir parçaya kimlik (metadata) basıyoruz
    for chunk in chunks:
        chunk.metadata.update(metadata)
        
    print(f"✅ Metin başarıyla {len(chunks)} parçaya bölündü ve {metadata} etiketleri eklendi.")
    
    return chunks