import re

def extract_email(text):
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return emails[0] if emails else "Not Found"

def extract_phone(text):
    phones = re.findall(r'\+?\d[\d\s\-]{8,15}\d', text)
    return phones[0] if phones else "Not Found"
