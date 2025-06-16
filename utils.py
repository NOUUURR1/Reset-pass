import smtplib
from email.mime.text import MIMEText

def send_email_code(receiver_email, code):
    sender_email = "projectteam1235@gmail.com" 
    sender_password = "vvnu ueqo hugq txry"  

    message = MIMEText(f"كود إعادة تعيين كلمة المرور هو: {code}")
    message["Subject"] = "رمز إعادة تعيين كلمة المرور"
    message["From"] = sender_email
    message["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
        return True
    except Exception as e:
        print(f"فشل إرسال الإيميل: {e}")
        return False
