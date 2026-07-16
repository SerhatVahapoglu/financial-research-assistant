from langchain_openai import ChatOpenAI
from src.validation.schemas import SynthesizedResponse
from . import AgentState

def synthesizer_node(state: AgentState):
    deneme = state.get("revision_count", 0) + 1
    print(f"✍️ Synthesizer: Veriler birleştiriliyor (Deneme: {deneme})...")
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    structured_llm = llm.with_structured_output(SynthesizedResponse)
    
    # Mevcut prompt kodunun yerine bunu yapıştır:
    context = f"PDF BİLGİLERİ:\n{state.get('documents', [])}\n\nWEB BİLGİLERİ:\n{state.get('web_results', [])}"
    
    prompt = f"""Soru: {state['question']}
    
    Aşağıdaki bağlamı kullanarak soruyu cevapla. 
    KATI KURALLAR:
    1. SADECE PDF ve WEB BİLGİLERİ içinde geçen verileri kullan.
    2. Eğer bilgi kaynaklarda yoksa "Bilgi bulunamadı" de. ASLA genel kültüründen sayılar, varsayımlar veya tahminler uydurma.
    
    BAĞLAM:
    {context}"""
    
    if state.get("validation_feedback"):
        prompt += f"\n\nDİKKAT! ÖNCEKİ CEVABINDA ŞU HATAYI YAPTIN:\n{state['validation_feedback']}\nLütfen sadece kaynaklarda geçen sayıları kullan!"

    response = structured_llm.invoke(prompt)
    
    return {
        "final_answer": response.final_answer,
        "claims": response.claims,
        "revision_count": deneme
    }