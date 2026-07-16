from src.ingestion.indexer import retrieve_documents
from . import AgentState
from qdrant_client.http.models import Filter, FieldCondition, MatchAny # <-- MatchAny ekledik

def retriever_node(state: AgentState):
    ticker_input = state.get("company_ticker") # "AAPL, TSLA" string'i
    
    # Virgülle ayırıp liste haline getiriyoruz
    tickers = [t.strip() for t in ticker_input.split(',')]
    print(f"📚 Retriever: Şu şirketler aranıyor: {tickers}")
    
    # MatchAny: Listeden herhangi biriyle eşleşenleri getir (OR operatörü gibi)
    qdrant_filter = Filter(
        must=[
            FieldCondition(
                key="metadata.ticker",
                match=MatchAny(any=tickers),
            )
        ]
    )
    
    # Birden fazla şirketten veri çekeceğimiz için 'k' değerini biraz artırabiliriz
    docs = retrieve_documents(state["question"], "financial_reports_collection", k=10, qdrant_filter=qdrant_filter)
    
    return {"documents": [d.page_content for d in docs]}