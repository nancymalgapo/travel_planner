import smtplib
import streamlit as st

from datetime import date
from io import BytesIO
from email.mime.text import MIMEText
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from typing import Tuple


def send_email(itinerary: str, recipient_email: str):
    try:
        smtp_server = st.secrets["smtp_server"]
        smtp_port = st.secrets["smtp_port"]
        sender_email = st.secrets["email_user"]
        sender_password = st.secrets["email_pass"]

        msg = MIMEText(itinerary)
        msg['Subject'] = 'Your Travel Itinerary'
        msg['From'] = sender_email
        msg['To'] = recipient_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        st.success("Itinerary sent to your email!")
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")


def create_pdf(itinerary: str) -> BytesIO:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.drawString(100, 750, "Travel Itinerary")
    pdf.drawString(100, 730, itinerary)
    pdf.save()
    buffer.seek(0)
    return buffer


def is_valid_input(departure_date, return_date, openai_key) -> Tuple[str, bool]:
    error_messages = []

    key_error, key_check = is_valid_openai_key(openai_key)
    if not key_check:
        error_messages.append(key_error)

    date_error, date_check = is_departure_before_return(departure_date, return_date)
    if not date_check:
        error_messages.append(date_error)

    if error_messages:
        return "\n".join(error_messages), False

    return "", True


def is_departure_before_return(departure_date: date, return_date: date) -> Tuple[str, bool]:
    if departure_date > return_date:
        return "Travel dates are not correct. Departure date should be before your return date.", False
    return "", True


def is_valid_openai_key(openai_key: str) -> Tuple[str, bool]:
    if not openai_key.startswith('sk-'):
        return "Invalid openai key", False

    return "", True
