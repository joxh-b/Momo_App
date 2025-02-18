import xml.etree.ElementTree as ET
import re

# Parse XML file and extract transactions
def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    transactions = []
    
    for sms in root.findall("sms"):
        message = sms.get("body")  # Extract SMS body
        parsed_data = extract_transaction(message)
        
        if parsed_data:
            transactions.append(parsed_data)

    return transactions

# Extract transaction details from SMS body
def extract_transaction(message):
    patterns = {
        "amount": r"RWF\s?(\d+[.,]?\d*)",
        "date": r"(\d{1,2}/\d{1,2}/\d{4})",
        "reference": r"Ref:\s?(\w+)",
        "type": r"(Deposit|Withdrawal|Airtime|Transfer|Bill Payment|Bundle Purchase)"
    }
    
    transaction = {
        "amount": extract_value(message, patterns["amount"]),
        "date": extract_value(message, patterns["date"]),
        "reference": extract_value(message, patterns["reference"]),
        "type": extract_value(message, patterns["type"], default="Unknown"),
        "message": message  # Store full message for debugging
    }
    
    if transaction["amount"] and transaction["date"]:
        return transaction
    else:
        return None  # Skip incomplete messages

# Helper function to extract values using regex
def extract_value(text, pattern, default=None):
    match = re.search(pattern, text)
    return match.group(1) if match else default
