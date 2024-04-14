# Description: This file contains utility functions for the parser module.
import pytesseract
import re



def extract_data_from_cv(file):
    text = pytesseract.image_to_string(file)
    email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    email = email[0] if email else None
    phone = re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', text)
    phone = phone[0] if phone else None
    return email, phone, text