import os
import shutil
import glob
from sec_edgar_downloader import Downloader

def download_10k_reports(tickers: list):
    # 1. Ayarlar
    raw_data_dir = os.path.join(os.path.dirname(__file__), '../../data/raw')
    os.makedirs(raw_data_dir, exist_ok=True)

    # SEC için kendimizi tanıtıyoruz (Kuraldır)
    dl = Downloader("FinancialResearchAssistant", "serhat.vahapoglu@example.com")

    print(f"📥 {len(tickers)} şirket için 10-K raporları indiriliyor...")

    for ticker in tickers:
        print(f"--- {ticker} işleniyor ---")

        # v5+ API: num_filings_to_download / amount yerine artık "limit" kullanılıyor
        dl.get("10-K", ticker, limit=1)

        # 2. Dosyayı bulma
        # v5'ten itibaren klasör adı "form" argümanıyla BİREBİR aynı yazılıyor (örn. "10-K", "10-k" değil)
        # ve dosya adı da "full-submission.txt" yerine detay dosyasına göre değişebiliyor.
        # Bu yüzden hem büyük/küçük harfe hem de dosya adına göre esnek arama yapıyoruz.
        search_path = os.path.join("sec-edgar-filings", ticker, "10-K", "*", "*")
        files = glob.glob(search_path)

        # Sadece dosyaları al (klasörleri değil), tercihen full-submission.txt önceliklendir
        files = [f for f in files if os.path.isfile(f)]
        preferred = [f for f in files if f.endswith("full-submission.txt")]
        if preferred:
            files = preferred

        if files:
            # En son inen dosyayı al
            source_file = max(files, key=os.path.getctime)

            # 3. Dosyayı data/raw/ klasörüne taşı ve adlandır
            dest_file = os.path.join(raw_data_dir, f"{ticker}_10k.txt")
            shutil.copy2(source_file, dest_file)
            print(f"✅ {ticker} dosyası {dest_file} yoluna başarıyla taşındı.")
        else:
            print(f"❌ {ticker} için dosya bulunamadı. Aranan yol: {search_path}")

    print("\n🚀 Tüm indirme işlemleri tamamlandı!")
    # İndirme geçici klasörünü temizleyebilirsin
    # shutil.rmtree("sec-edgar-filings")