import json
import os
import sys

# Ana dizini yola ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.agents.graph import create_agent_graph
from src.validation.numeric_matcher import extract_numbers

def load_benchmark_data(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_evaluation():
    print("📊 Değerlendirme (Evaluation) Başlıyor...\n")
    
    # 1. Test verisini yükle
    dataset_path = os.path.join(os.path.dirname(__file__), 'benchmark_dataset.json')
    data = load_benchmark_data(dataset_path)
    
    # 2. Sistemimizi (LangGraph) başlat
    app = create_agent_graph()
    
    total_questions = len(data)
    correct_numbers = 0
    
    for i, item in enumerate(data, 1):
        question = item['question']
        expected_number = item['expected_number']
        
        print(f"[{i}/{total_questions}] Soru: {question}")
        
        # Sistemi çalıştır
        result = app.invoke({"question": question})
        final_answer = result["final_answer"]
        
        print(f"    Sistemin Cevabı: {final_answer}")
        
        # 3. Kendi Özel Metriğimiz: "Sayısal Kesinlik (Numeric Accuracy)"
        if expected_number:
            extracted_numbers = extract_numbers(final_answer)
            # Beklenen sayı, sistemin cevabından çıkarılan sayıların içinde mi?
            if expected_number in extracted_numbers:
                print("    ✅ Sayısal Eşleşme Başarılı!")
                correct_numbers += 1
            else:
                print(f"    ❌ Sayısal Eşleşme Hatalı! Beklenen: {expected_number}, Bulunanlar: {extracted_numbers}")
        else:
            # Beklenen bir sayı yoksa (metin sorusuysa) bu metriği otomatik geçeriz
            print("    ✅ (Sayısal eşleşme gerektirmeyen soru)")
            correct_numbers += 1
            
        print("-" * 50)
        
    # 4. Sonuçları Hesapla ve Göster
    accuracy = (correct_numbers / total_questions) * 100
    print(f"\n🏆 DEĞERLENDİRME SONUCU")
    print(f"Toplam Soru: {total_questions}")
    print(f"Sayısal Doğruluk Oranı (Numeric Accuracy): %{accuracy:.1f}")

if __name__ == "__main__":
    run_evaluation()