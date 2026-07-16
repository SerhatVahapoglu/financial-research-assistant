from langgraph.graph import StateGraph, END
from . import AgentState
from .planner import planner_node
from .retriever_agent import retriever_node
from .web_researcher import web_researcher_node
from .synthesizer import synthesizer_node
from .validator import validator_node

# Koşullu Yönlendirme (Conditional Edge) Mantığı
def route_validation(state: AgentState):
    # Eğer onaylandıysa bitir
    if state.get("validation_feedback") == "OK":
        return END
    # Eğer 3 defadan fazla denediyse sonsuz döngüden kaçmak için bitir
    elif state.get("revision_count", 0) >= 3:
        print("⚠️ Maksimum düzeltme denemesine (3) ulaşıldı. Süreç sonlandırılıyor.")
        return END
    # Hata varsa ve hakkı dolmadıysa Sentezleyiciye geri dön
    else:
        return "synthesizer"

def create_agent_graph():
    workflow = StateGraph(AgentState)
    
    # Ajanları Ekle
    workflow.add_node("planner", planner_node)
    workflow.add_node("retriever", retriever_node)
    workflow.add_node("web_researcher", web_researcher_node)
    workflow.add_node("synthesizer", synthesizer_node)
    workflow.add_node("validator", validator_node)
    
    # Sabit Akış (Düz çizgi)
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "retriever")
    workflow.add_edge("retriever", "web_researcher")
    workflow.add_edge("web_researcher", "synthesizer")
    workflow.add_edge("synthesizer", "validator")
    
    # Dinamik Akış (Koşullu Yönlendirme)
    workflow.add_conditional_edges(
        "validator",          # Validator'dan çıkışta sor
        route_validation,     # Bu fonksiyonun sonucuna bak
        {
            "synthesizer": "synthesizer", # Fonksiyon "synthesizer" derse geri dön
            END: END                      # Fonksiyon END derse bitir
        }
    )
    
    return workflow.compile()