from src.validation.numeric_matcher import validate_claim
from . import AgentState

def validator_node(state: AgentState):
    print("🕵️‍♂️ Validator: Rakamlar GERÇEK kaynaklarda aranıyor...")
    claims = state.get("claims", [])
    feedback = ""

    # HİLE ENGELLENDİ: LLM'in yazdığına değil, doğrudan veritabanından gelen PDF ve Web verilerine bakıyoruz!
    real_documents = " ".join(state.get("documents", [])) + " " + " ".join(state.get("web_results", []))

    for claim in claims:
        is_valid = validate_claim(claim.numeric_value, real_documents)
        if not is_valid:
            feedback += f"HATA: İddia ettiğin '{claim.numeric_value}' sayısı, orijinal belgelerimizde (PDF/Web) bulunamadı. Lütfen genel kültüründen rakam uydurma!\n"

    if feedback:
        print(f"🚨 Validator: Hata bulundu, Synthesizer'a geri gönderiliyor.")
        return {"validation_feedback": feedback}

    print("✅ Validator: Tüm sayılar doğru, onaylandı!")
    return {"validation_feedback": "OK"}