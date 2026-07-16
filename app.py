import streamlit as st
import sys
import os

# Proje dizinini sisteme ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importları tek seferde ve doğru yollardan yapıyoruz
from src.agents.graph import create_agent_graph
from src.agents.summarizer import generate_executive_summary
from src.utils.email_sender import send_email_report

# QA Ajanını başlat
qa_graph = create_agent_graph()

st.set_page_config(page_title="Finansal Analiz Terminali", layout="wide")

st.title("📈 AI Finansal Analiz Terminali")

# Tab yapısı
tab1, tab2 = st.tabs(["💬 Soru-Cevap (QA)", "📊 Yönetici Özeti (10-K)"])

# --- TAB 1: SORU-CEVAP ---
with tab1:
    st.header("Finansal Soru-Cevap")
    question = st.text_input("Şirketler veya piyasalar hakkında bir şey sor:", key="qa_input")
    
    if st.button("Sor"):
        if question:
            with st.spinner("Veritabanı ve internet taranıyor..."):
                # Ajanı çalıştır
                result = qa_graph.invoke({"question": question, "documents": []})
                
                # --- YENİ SATIR ---
                print(f"DEBUG - AJANIN DÖNDÜRDÜĞÜ SONUÇ: {result}") 
                # ------------------
                
                # app.py içindeki ilgili satırı değiştir
                answer = result.get("final_answer", "Cevap üretilemedi.")
                st.info(answer)
        else:
            st.warning("Lütfen bir soru girin.")

# --- TAB 2: ÖZETLEME ---
with tab2:
    st.header("10-K Yönetici Özeti")
    ticker = st.text_input("Şirket Kodu (Örn: AAPL):", "AAPL", key="ticker_input")
    
    if st.button("Raporu Oluştur"):
        with st.spinner("Wall Street derinliklerine iniliyor..."):
            rapor = generate_executive_summary(ticker)
            st.session_state['rapor'] = rapor

    if 'rapor' in st.session_state:
        st.markdown(st.session_state['rapor'])
        
        st.divider()
        email = st.text_input("Raporu kime gönderelim?", key="email_input")
        if st.button("📩 E-posta ile Gönder"):
            if send_email_report(email, f"Analiz Raporu: {ticker}", st.session_state['rapor']):
                st.success("Rapor başarıyla gönderildi!")
            else:
                st.error("E-posta gönderilemedi.")