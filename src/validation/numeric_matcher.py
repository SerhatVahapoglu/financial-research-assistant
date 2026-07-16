import re

def extract_numbers(text: str) -> set:
    """
    Bir metnin içindeki tüm sayıları bulur ve temizler.
    Regex (Düzenli İfade) kullanarak ondalıklı ve virgüllü sayıları da yakalar.
    """
    if not text:
        return set()
        
    # Bu kural: "Sadece rakamları, veya aralarında nokta/virgül olan rakamları bul" demek.
    # Örnek: 1.234, 500, 0.00001
    numbers = re.findall(r'\b\d+(?:[.,]\d+)*\b', text)
    
    # Sayıları karşılaştırması kolay olsun diye içindeki virgülleri temizleyip (örn: 1,000 -> 1000) 
    # benzersiz bir küme (set) olarak döndürüyoruz.
    return set(num.replace(',', '') for num in numbers)

def validate_claim(numeric_value: str, source_quote: str) -> bool:
    """
    Yapay zekanın iddia ettiği sayı, gösterdiği kaynak metinde gerçekten var mı diye kontrol eder.
    """
    # Eğer bu cümlede finansal bir sayı yoksa, kontrol etmeye gerek yok, True dön.
    if not numeric_value or numeric_value.strip() in ["", "None", "Yok"]:
        return True 
        
    # Kaynak metindeki (orijinal PDF'teki) tüm sayıları çıkar
    source_numbers = extract_numbers(source_quote)
    
    # LLM'in iddia ettiği sayıyı çıkar
    claim_numbers = extract_numbers(numeric_value)
    
    # Eğer iddia edilen sayı, kaynağın içindeki sayılar listesinde yoksa yalan söylüyordur (Halüsinasyon)
    for num in claim_numbers:
        if num not in source_numbers:
            print(f"🚨 HALÜSİNASYON YAKALANDI: İddia edilen '{num}' sayısı orijinal metinde yok!")
            return False
            
    return True