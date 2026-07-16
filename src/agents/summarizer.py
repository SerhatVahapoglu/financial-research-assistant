import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from src.ingestion.indexer import retrieve_documents

def generate_executive_summary(company_ticker: str) -> str:
    """
    Qdrant'taki 10-K verilerini kullanarak Map-Reduce mantığıyla
    kurumsal bir Yönetici Özeti (Executive Summary) oluşturur.
    """
    print(f"🔍 1. Aşama: {company_ticker.upper()} için Qdrant'tan en kritik parçalar çekiliyor...")
    
    # 1. Anlamsal olarak hedef şirketi tepeye çıkarmak için sorguyu hazırlıyoruz
    query = f"{company_ticker} financial performance, revenue, strategic outlook, primary risk factors Item 1A Item 7"
    
    # 2. Qdrant'tan en iyi 60 belgeyi çekiyoruz (Filtresiz)
    raw_docs = retrieve_documents(query, "financial_reports_collection", k=60)
    
    # 3. Post-Retrieval Filtering (GERÇEK Metadata'ya göre ayıklama)
    company_docs = []
    search_ticker = company_ticker.upper()
    
    for doc in raw_docs:
        # Ekran görüntüsünde bulduğumuz gerçek 'ticker' anahtarını çekiyoruz
        # Küçük harfle ('apple') geldiği için her ihtimale karşı .upper() ile büyütüyoruz
        db_ticker = str(doc.metadata.get("ticker", "")).upper()
        
        # Eğer kullanıcı "AAPL" yazdıysa ama Qdrant'ta "APPLE" kayıtlıysa diye esnek eşleşme:
        is_match = (
            search_ticker == db_ticker or 
            (search_ticker == "AAPL" and db_ticker == "APPLE") or
            search_ticker in db_ticker or 
            db_ticker in search_ticker
        )
        
        if is_match:
            company_docs.append(doc)
            if len(company_docs) == 15: # Rapor için 15 kritik parça yeterli
                break
    
    if not company_docs:
        return f"❌ {company_ticker} için veritabanında belge bulunamadı. Lütfen adını kontrol edin."

    print(f"🧠 2. Aşama (MAP): {len(company_docs)} belge parçası yapay zeka tarafından analiz ediliyor...")
    
    # Map (Küçük Özetler Çıkarma) Ajanı
    mapper_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    map_prompt = PromptTemplate.from_template(
        "Aşağıdaki 10-K rapor parçasını oku. Şirketin finansal durumu, gelirleri veya riskleriyle "
        "ilgili en önemli 2-3 detayı Türkçe olarak özetle. Rakamları mutlaka koru. "
        "Eğer önemli bir finansal/risk bilgisi yoksa sadece 'Önemli bilgi yok' yaz.\n\n"
        "Metin: {text}"
    )
    
    mini_summaries = []
    for i, doc in enumerate(company_docs):
        chain = map_prompt | mapper_llm
        res = chain.invoke({"text": doc.page_content})
        
        if "Önemli bilgi yok" not in res.content:
            mini_summaries.append(f"- {res.content}")
            
    print(f"📊 3. Aşama (REDUCE): {len(mini_summaries)} adet not birleştirilip Yönetici Özeti yazılıyor...")
    
    # Reduce (Ana Raporlayıcı) Ajanı - GPT-4o
    reducer_llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
    reduce_prompt = PromptTemplate.from_template(
        "Sen kıdemli bir Wall Street Finansal Analistisin. Aşağıda {company} şirketinin 10-K raporundan "
        "yapay zeka asistanları tarafından çıkarılmış ham notlar bulunuyor. Bu notları kullanarak "
        "yatırımcılar için profesyonel bir 'Yönetici Özeti (Executive Summary)' raporu hazırla.\n\n"
        "Rapor şu formatta ve Markdown dilinde olmalıdır:\n"
        "# {company} - Yönetici Özeti (10-K)\n"
        "## 📈 1. Finansal Performans ve Gelirler\n"
        "[Buraya yaz]\n"
        "## 🎯 2. Gelecek Vizyonu ve Strateji\n"
        "[Buraya yaz]\n"
        "## ⚠️ 3. Temel Risk Faktörleri\n"
        "[Buraya yaz]\n\n"
        "Ham Notlar:\n{notes}"
    )
    
    combined_notes = "\n".join(mini_summaries)
    reduce_chain = reduce_prompt | reducer_llm
    final_report = reduce_chain.invoke({"company": company_ticker.upper(), "notes": combined_notes})
    
    print("✅ Rapor başarıyla oluşturuldu!\n")
    return final_report.content