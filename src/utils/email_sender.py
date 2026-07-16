import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# src/utils/email_sender.py
import os
from dotenv import load_dotenv

load_dotenv() 

user = os.getenv("EMAIL_USER")
pw = os.getenv("EMAIL_PASS")

print(f"DEBUG - EMAIL_USER: {user}")
# Şifrenin tamamını göstermiyoruz (güvenlik!), sadece uzunluğunu ve ilk/son karakterlerini kontrol ediyoruz
print(f"DEBUG - PASSWORD LENGTH: {len(pw) if pw else 0}")
if pw:
    print(f"DEBUG - PASSWORD SAMPLE: {pw[:3]}***{pw[-3:]}")

def send_email_report(recipient_email, subject, report_content):
    # .env dosyasından al (Güvenlik için asla kod içine yazma!)
    sender_email = os.getenv("EMAIL_USER") 
    sender_password = os.getenv("EMAIL_PASS") # Gmail için "Uygulama Şifresi"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(report_content, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    # src/utils/email_sender.py içindeki except bloğunu şu şekilde güncelle
    except Exception as e:
        print(f"--- DETAYLI E-POSTA HATASI ---")
        print(f"Hata tipi: {type(e).__name__}")
        print(f"Hata mesajı: {str(e)}")
        return False