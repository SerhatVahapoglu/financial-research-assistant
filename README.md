# 📈 AI Financial Research Assistant

Bu proje, 10-K raporlarını analiz eden, gerçek zamanlı finansal verilerle desteklenen, yapay zeka destekli bir araştırma asistanıdır. LangGraph kullanarak geliştirilmiş ajansal (agentic) bir RAG (Retrieval-Augmented Generation) mimarisine sahiptir.

## 🚀 Öne Çıkan Özellikler
- **Agile Agentic Workflow:** Soru analizi (Planner), veri getirme (Retriever), doğrulama (Validator) ve sentezleme ajanları ile hatasız bilgi akışı.
- **Web Fallback:** Yerel veri tabanında bulunmayan bilgiler için otomatik internet araştırması (Tavily).
- **Map-Reduce Analiz:** 300+ sayfalık 10-K raporlarından profesyonel Yönetici Özeti (Executive Summary) çıkaran analiz motoru.
- **Modern UI:** Streamlit ile interaktif finansal terminal arayüzü.
- **Otomatik Raporlama:** Analiz sonuçlarını e-posta ile otomatik gönderme yeteneği.

## 🛠️ Teknolojiler
- **Framework:** LangChain, LangGraph, Streamlit
- **LLM:** OpenAI GPT-4o, GPT-4o-mini
- **Database:** Qdrant (Vector Store)
- **Deployment:** Docker

## 🏗️ Mimari
Sistem şu akışla çalışır:
1. **Retriever:** Qdrant üzerinden ilgili döküman parçalarını çeker.
2. **Web Researcher:** Eğer yerel veri yetersizse devreye girer.
3. **Summarizer:** Map-Reduce yöntemi ile veriyi rapora dönüştürür.
4. **Sender:** Sonucu kullanıcıya iletir.

## ⚙️ Kurulum
1. Repoyu klonlayın: `git clone [repo-url]`
2. Bağımlılıkları yükleyin: `pip install -r requirements.txt`
3. `.env` dosyanızı oluşturun:
   ```text
   OPENAI_API_KEY=...
   TAVILY_API_KEY=...
   EMAIL_USER=...
   EMAIL_PASS=...