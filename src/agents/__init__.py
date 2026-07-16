from typing import TypedDict, List, Any

class AgentState(TypedDict):
    question: str
    research_steps: List[str]
    documents: List[str]
    web_results: List[str]
    final_answer: str
    company_ticker: str      # Sorumuzun hedef şirketi (Örn: AAPL)
    
    # Doğrulama için yeni eklenenler
    claims: List[Any]        # Cımbızlanan iddialar ve sayılar
    revision_count: int      # Kaçıncı deneme olduğu
    validation_feedback: str # Validator'un yazdığı hata mesajı