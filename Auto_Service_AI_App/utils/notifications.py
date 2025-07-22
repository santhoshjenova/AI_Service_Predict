# utils/notifications.py

import os
from twilio.rest import Client
import smtplib
from email.message import EmailMessage

# --- Environment Variables or replace with your credentials directly if needed ---
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_SMS_NUMBER")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASS = os.getenv("SMTP_PASSWORD")

def send_sms(to_number: str, msg: str):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH)
        message = client.messages.create(
            body=msg,
            from_=TWILIO_PHONE,
            to=to_number
        )
        print("SMS sent:", message.sid)
        return True
    except Exception as e:
        print("SMS Failed:", e)
        return False

def send_whatsapp(to_number: str, msg: str):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH)
        message = client.messages.create(
            body=msg,
            from_='whatsapp:' + TWILIO_PHONE,
            to='whatsapp:' + to_number
        )
        print("WhatsApp sent:", message.sid)
        return True
    except Exception as e:
        print("WhatsApp Failed:", e)
        return False

def send_email(to_email: str, subject: str, body: str):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = SMTP_EMAIL
        msg['To'] = to_email
        msg.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SMTP_EMAIL, SMTP_PASS)
            smtp.send_message(msg)
        print("Email sent!")
        return True
    except Exception as e:
        print("Email Failed:", e)
        return False
