import yfinance as yf
from langchain_core.tools import tool

@tool
def get_current_stock_price(ticker: str) -> str:
    """
    Verilen hisse senedi sembolünün (ticker) güncel piyasa fiyatını getirir.
    Örnek kullanım: AAPL, MSFT, TSLA.
    """
    try:
        print(f"📈 Piyasa Verisi Çekiliyor: {ticker}...")
        stock = yf.Ticker(ticker)
        
        # O günkü piyasa verilerinden en güncel fiyatı alıyoruz
        todays_data = stock.history(period='1d')
        if todays_data.empty:
            return f"{ticker} için güncel fiyat bulunamadı."
            
        current_price = todays_data['Close'].iloc[-1]
        
        return f"{ticker} güncel hisse fiyatı: ${current_price:.2f}"
    
    except Exception as e:
        return f"Hisse fiyatı çekilirken hata oluştu: {str(e)}"