from pydantic import BaseModel, Field
from typing import List
from langchain_openai import ChatOpenAI
from . import AgentState

class ResearchPlan(BaseModel):
    steps: List[str] = Field(description="Soruyu cevaplamak için yapılması gereken araştırma adımları.")
    company_ticker: str = Field(description="Soruda bahsi geçen şirketin borsa sembolü (Örn: AAPL, TSLA, MSFT). Eğer bir şirket bulunamazsa boş bırak.")

def planner_node(state: AgentState):
    print("🧠 Planner: Soru analiz ediliyor, plan ve hedef şirket çıkarılıyor...")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    structured_llm = llm.with_structured_output(ResearchPlan)
    
    plan = structured_llm.invoke(f"Şu soru için bir araştırma planı ve hedef şirket sembolü çıkar: {state['question']}")
    
    print(f"🎯 Hedef Şirket Tespit Edildi: {plan.company_ticker or 'Bulunamadı'}")
    
    return {
        "research_steps": plan.steps,
        "company_ticker": plan.company_ticker
    }