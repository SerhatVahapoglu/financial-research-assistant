from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# Sistemin ana dizini bulabilmesi için
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.agents.graph import create_agent_graph

# API Uygulamamızı başlatıyoruz
app = FastAPI(
    title="Financial Research AI API",
    description="Multi-Agent tabanlı finansal araştırma asistanı.",
    version="1.0.0"
)

# LangGraph sistemimizi tek bir sefer ayağa kaldırıp hafızada tutuyoruz
print("🚀 AI Ajanları Yükleniyor...")
agent_app = create_agent_graph()
print("✅ Sistem Hazır!")

# Kullanıcının göndereceği JSON veri formatı
class QueryRequest(BaseModel):
    question: str

# POST isteği atacağımız uç nokta (endpoint)
@app.post("/query")
def ask_question(request: QueryRequest):
    try:
        # Gelen soruyu LangGraph'a veriyoruz
        result = agent_app.invoke({"question": request.question})
        
        # Sonucu temiz bir JSON olarak dışarı dönüyoruz
        return {
            "question": request.question,
            "answer": result.get("final_answer", "Cevap üretilemedi."),
            "validation_status": "Success",
            "extracted_claims": result.get("claims", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Basit bir sağlık kontrolü endpoint'i
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Sistem tıkır tıkır çalışıyor!"}