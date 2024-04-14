# Description: This file contains utility functions for the parser module.

# IMPORT SETTINGS
from django.conf import settings
from email_validator import validate_email
import PyPDF2
import re
import xlwt
import os
import re
import textract
from pathlib import Path
import subprocess
import docx2txt



def extract_data_from_cv(file):
    pdf_reader = PyPDF2.PdfReader(file)
    
    # Extract text from each page
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num] 
        text += page.extract_text()
    email_matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    email = None
    for email_match in email_matches:
        try:
            validate_email(email_match)
            email = email_match
            break
        except Exception:
            pass
    phone_matches = re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', text)
    phone = phone_matches[0] if phone_matches else None
    print(text)
    return email, phone, text



def extract_data_from_docx(file):
    
    text = extract_text(f"/home/media/cv_files/{str(file.name)}")
    print(text)
    email_matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    email = None
    for email_match in email_matches:
        try:
            validate_email(email_match)
            email = email_match
            break
        except Exception:
            pass
    phone = re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', text)
    phone = phone[0] if phone else None
    return email, phone, text

def extract_data_from_doc(file):
    text = extract_text(f"/home/media/cv_files/{str(file.name)}")
    print(text)
    email_matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    email = None
    for email_match in email_matches:
        try:
            validate_email(email_match)
            email = email_match
            break
        except Exception:
            pass
    phone = re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', text)
    phone = phone[0] if phone else None
    print("=============>",text)
    print(type(text))
    return email, phone, text


def generate_xls(cvs):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('CV Data')
    row_num = 0
    for cv in cvs:
        ws.write(row_num, 0, cv.email)
        ws.write(row_num, 1, cv.contact_number)
        ws.write(row_num, 2, cv.text_content)
        row_num += 1
    xls_file = os.path.join('media', 'cv_data.xls')
    wb.save(xls_file)
    return xls_file



def extract_text(file_path):
    
    file_name, file_extension = str(file_path).split('.')
        
    try:
        if file_extension == 'docx':
            return docx2txt.process(file_path)
        elif file_extension == 'doc':
            output = subprocess.check_output(['antiword', file_path])
            return output.decode('utf-8')  # Assuming output is in UTF-8 encoding
    except subprocess.CalledProcessError:
        print("Error: Failed to extract text from the document.")
        return None