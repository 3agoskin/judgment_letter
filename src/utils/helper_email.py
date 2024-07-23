import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage


SENDER_EMAIL = 'email'
EMAIL_PASSWORD = 'password'

def send_email(email_to, email_content, date_court_session):
    
    msg = MIMEMultipart('alternative')
    msg['From'] = SENDER_EMAIL
    msg['To'] = email_to
    msg['Subject'] = f"Уведомление дела назначенного к {date_court_session}"
    user_message = email_content

    part1 = MIMEText(user_message, 'html')
    msg.attach(part1)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        smtp.login(SENDER_EMAIL, EMAIL_PASSWORD)
        smtp.send_message(msg)
    