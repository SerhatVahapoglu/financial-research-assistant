import warnings
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from src.mcp.openbb_client import get_current_stock_price
from . import AgentState

# Konsol uyarılarını gizliyoruz
warnings.filterwarnings("ignore")

# 1. Alet Çantamız (Araçları buraya listeliyoruz)
tavily_tool = TavilySearchResults(max_results=2)
tools = [tavily_tool, get_current_stock_price]

# 2. Modelimiz (Beyin)
# Web araştırması için 4o-mini oldukça hızlı ve yeterlidir.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 3. Kendi kendine araç seçebilen ReAct Ajanını oluşturuyoruz
researcher_agent = create_react_agent(llm, tools=tools)

def web_researcher_node(state: AgentState):
    """
    Qdrant'ta bilgi bulunamadığında veya eksik olduğunda devreye giren Web Ajanı.
    İnternette ve OpenBB'de araştırma yapar, sonucu formatlayarak belgelere ekler.
    """
    print("🌐 Web Researcher: Qdrant yetersiz kaldı, internet araştırması başlatılıyor...")
    
    question = state.get("question")
    
    # Ajanı çalıştırıp web ve OpenBB üzerinden araştırma yapmasını sağlıyoruz.
    # create_react_agent, "messages" formatında girdi bekler.
    response = researcher_agent.invoke({
        "messages": [("user", f"Lütfen şu finansal soruyu araştır ve net bir cevap ver: {question}")]
    })
    
    # Ajanın kendi araçlarını kullanarak ürettiği nihai metni alıyoruz
    web_result = response["messages"][-1].content
    
    # 1. Mevcut belgeleri (Qdrant'tan gelenleri) al (silinmemesi için)
    current_docs = state.get("documents", [])
    if current_docs is None:
        current_docs = []
        
    # 2. Web sonucunu temiz ve belirgin bir formatta etiketle
    # Bu etiket, Validator ve Synthesizer'ın bu bilgiyi "güvenilir kaynak" saymasını sağlar
    formatted_web_context = (
        f"[WEB ARAMASI KAYNAĞI]: Yerel veri tabanında bulunamayan bilgi için "
        f"internet ve finansal API'ler üzerinden şu güncel veriler elde edilmiştir:\n{web_result}"
    )
    
    # 3. Formate edilmiş web sonucunu belgelere ekle
    current_docs.append(formatted_web_context)
    
    print("🌐 Web Researcher: İnternet araştırması tamamlandı ve 'Resmi Belgeler' arasına eklendi.")
    
    # State'i güncelliyoruz
    return {"documents": current_docs}