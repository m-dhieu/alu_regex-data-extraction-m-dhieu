#!/usr/bin/env python3

import os
import stat
import sys
import re
import time

# Add execute permission to the file for the user.
if __name__ == "__main__":
    script_path = os.path.abspath(sys.argv[0])
    current_permissions = os.stat(script_path).st_mode
    os.chmod(script_path, current_permissions | stat.S_IXUSR)

# Make the user experience interactive.   
def welcome_user():
    """
    An interactive welcome prompt to personalize the user experience.
    """
    print("Hello! Please enter your name:")
    user_name = input("> ").strip()
    print(f"\nHello {user_name} 😊")
    print("Welcome to the Regex Data Extraction Tool!")
    time.sleep(2)
    print("This tool extracts emails, URLs, phone numbers, credit cards, times(12h/24h), HTML tags, hashtags, and currency amounts from text.")
    time.sleep(3)
    print("Let's get started...\n")
    time.sleep(1)
    return user_name
    
# Sample text to test the functionality of the data extraction tool.
sample_text = """
Emails:
user@example.com                        # standard email
firstname.lastname@company.co.uk        # email with subdomain and country TLD
bad-email@.com                          # malformed email
user@domain                             # malformed email (no TLD)
m.dhieu@alustudent.com                  # existing email with standard format

URLs:
https://www.example.com                 # standard HTTPS URL
https://subdomain.example.org/page      # URL with subdomain and path
http://example.net                      # HTTP URL
ftp://invalid.protocol.com              # malformed (unsupported protocol)
www.missingprotocol.com                 # URL without protocol
https://github.com/m-dhieu              # existing standard HTTPS URL
www.agasobanuyefilms.com                # existing URL

Phone numbers:
(123) 456-7890                          # US format (parentheses)
123-456-7890                            # US format (dashes)
123.456.7890                            # US format (dots)
1234567890                              # US format (plain digits)
(321) 654 0987                          # US format (spaces)
12-3456-7890                            # Malformed/other format
+249 91 234 5678                        # Sudan (country code +249)
+211 92 123 4567                        # South Sudan (country code +211)
+250 788 123 456                        # Rwanda (country code +250)
+1 202 555 0173                         # US (country code +1)

Credit card numbers:
1234 5678 9012 3456                     # standard 16-digit
1234-5678-9012-3456                     # 16-digit with dashes
1234567890123456                        # 16-digit plain
1234-5678-9012                          # malformed (too short)

Times:
14:30                                  # 24-hour format
2:30 PM                                # 12-hour format
11:59 PM                               # 12-hour format
25:61                                  # invalid time
13:60                                  # invalid time
00:00 AM                               # edge case

HTML tags:
<p>                                    # simple tag
<div class="example">                  # tag with attribute
<img src="image.jpg" alt="description">  # tag with multiple attributes
<a href="https://example.com" target="_blank"> # tag with URL attribute
<123invalid>                           # malformed tag
<selfclosing/>                         # self-closing tag

Hashtags:
#example                               # simple hashtag
#ThisIsAHashtag                        # CamelCase hashtag
#123numbers                            # hashtag starting with numbers
hello#world                            # hashtag in the middle of text
#_underscore                           # hashtag with underscore

Currency amounts:
$19.99                                 # US Dollar 
$1,234.56                              # US Dollar with comma 
$1234                                  # US Dollar, no comma 
€50                                    # Euro (Europe)
$12.3                                  # US Dollar, single decimal 
$0.99                                  # US Dollar, less than 1 
$10,000.00                             # US Dollar, large amount 
£2,500.00                              # British Pound 
SDG 5,000.00                           # Sudanese Pound 
SSP 3,200.50                           # South Sudanese Pound 
RWF 150,000.00                         # Rwandan Franc 
INR 75,000.00                          # Indian Rupee 
JPY 1,000,000                          # Japanese Yen  
CAD 2,500.00                           # Canadian Dollar 
ZAR 12,345.67                          # South African Rand 
"""

# Dictionary of regex patterns for each data type to extract.
patterns = {
    # allows longer TLDs, prevents leading/trailing/consecutive dots in local part
    "emails": r"\b[a-zA-Z0-9](?:[a-zA-Z0-9._%+-]{0,62}[a-zA-Z0-9])?@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",

    # matches http(s), www, and domain-only URLs, supports query/fragment, and IDNs
    "urls": r"\b(?:https?://|www\.)[a-zA-Z0-9\-._~%]+(?:\.[a-zA-Z0-9\-._~%]+)+(?:/[^\s]*)?\b",

    # supports optional country code (1-4 digits), various separators, and parentheses
    "phone_numbers": r"\b(?:\+?\d{1,4}[-.\s]?)?(?:\(?\d{1,4}\)?[-.\s]?){1,2}\d{1,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b",

    # matches 13-19 digits, optional spaces/hyphens, and common credit card formats
    "credit_cards": r"\b(?:\d[ -]*?){13,19}\b",

    # matches 24h and 12h with AM/PM, prevents invalid time (minutes/hours)
    "times": r"\b((0?[1-9]|1[0-2]):[0-5]\d\s?[APap][Mm]|([01]?\d|2[0-3]):[0-5]\d)\b",

    # matches opening, closing, and self-closing tags, ignores invalid tags
    "html_tags": r"</?[a-zA-Z][a-zA-Z0-9]*(?:\s+[^<>]*)?/?>",

    # supports Unicode, avoids mid-word hashtags, and prevents trailing underscores
    "hashtags": r"(?<!\w)#\w*[A-Za-z_]+\w*",

    # matches $, €, £, or any 3-letter currency code (ISO 4217), with/without commas/decimals
    "currency": (
        r"(?<!\w)([\$€£])\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?"  # $, €, £
        r"|\b([\$€£])\s?\d+(?:\.\d{2})?\b"                   # $, €, £ (no comma)
        r"|\b([A-Z]{3})\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?\b"  # Any 3-letter currency code (e.g., USD, RWF, SSP)
    )
}

# Extract data.
def extract_data(text):
    """
    Extract data matching each regex pattern from the input text.
    Return a dictionary with keys as data types and values as lists of matches.
    """
    results = {}
    for category, pattern in patterns.items():
        print(f"Extracting {category.replace('_', ' ')}...")
        time.sleep(1)  # simulate processing delay
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        results[category] = matches
        print(f"  Found {len(matches)} matches.\n")
        time.sleep(1)
    return results

# Save the extracted data.
def save_to_files(data_dict):
    """
    Save extracted data to individual category files and a combined summary file.
    Handle tuple results from regex with capturing groups.
    """
    for category, items in data_dict.items():
        filename = f"{category}_extracted.txt"
        print(f"Saving {len(items)} {category.replace('_', ' ')} to {filename}...")
        with open(filename, 'w', encoding='utf-8') as f:
            for item in items:
                # Handle tuple results from regex with capturing groups.
                if isinstance(item, tuple):
                    line = ''.join([part for part in item if part])
                else:
                    line = item
                f.write(line + "\n")
        print("  Individual category save complete.\n")
        time.sleep(0.5)

    # Save all extracted data into a single summary file.
    combined_filename = "all_extracted_data.txt"
    print(f"Saving all extracted data to {combined_filename}...")
    with open(combined_filename, 'w', encoding='utf-8') as f:
        for category, items in data_dict.items():
            header = f"--- {category.replace('_', ' ').title()} ---\n"
            f.write(header)
            if items:
                for item in items:
                    if isinstance(item, tuple):
                        line = ''.join([part for part in item if part])
                    else:
                        line = item
                    f.write(f"{line}\n")
            else:
                f.write("No matches found\n")
            f.write("\n")
    print("  Combined category save complete.\n")
    time.sleep(0.5)

# Display the extracted data on the local machine's console.
def print_extracted_data(data_dict):
    """
    Print extracted data to the console.
    Handle tuple results from regex with capturing groups.
    """
    for category, items in data_dict.items():
        print(f"--- {category.replace('_', ' ').title()} ---")
        if items:
            for item in items:
                if isinstance(item, tuple):
                    line = ''.join([part for part in item if part])
                else:
                    line = item
                print(f"  • {line}")
        else:
            print("  • No matches found")
        print()

# Main program flow:
if __name__ == "__main__":
    # 1. Welcome user and get their name.
    user_name = welcome_user()
    # 2. Extract data from the sample text using regex patterns.
    extracted = extract_data(sample_text)
    # 3. Display the extracted data on the local machine's console.
    print_extracted_data(extracted)
    # 4. Save the extracted data to files.
    save_to_files(extracted)
    # 5. Print a completion message.
    print(f"Thank you for using the Regex Data Extraction Tool, {user_name}! All data extracted and saved successfully.\nList extracted data files for categorical verification/reference.")
