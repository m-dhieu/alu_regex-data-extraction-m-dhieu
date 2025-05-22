#!/usr/bin/env python3

import os
import stat
import sys
import re
import time

# Add execute permission to the file for Unix user(s).
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
    time.sleep(1)
    print("This tool extracts emails, URLs, phone numbers, credit cards, times(12h/24h), HTML tags, and currency amounts from text.")
    time.sleep(2)
    print("These data types are essential for web scraping, data validation, and information retrieval from diverse text sources.")
    time.sleep(2)
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
m.dhieu@alustudent.com                  # existing email on web with standard format
user..name@example.com                  # consecutive dots
user@example-.com                       # domain starts with hyphen
test@example.museum                     # Valid TLD

URLs:
https://www.example.com                 # standard HTTPS URL
https://subdomain.example.org/page      # URL with subdomain and path
http://example.net                      # HTTP URL
ftp://invalid.protocol.com              # malformed (unsupported protocol)
www.missingprotocol.com                 # URL without protocol
https://github.com/m-dhieu              # existing standard HTTPS URL
www.agasobanuyefilms.com                # existing URL on web
example.com                             # No protocol
https://example.com/with space          # URL with space
https://example.com?query=value         # URL with query string
https://example.com#fragment            # URL with fragment
https://user:password@example.com       # URL with authentication

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
+44 7700 900000                         # UK (country code +44)
447700900000                            # UK format (no plus)
07700 900000                            # UK format (no country code)
1-800-MONICA                            # US toll-free with letters

Credit card numbers:
1234 5678 9012 3456                     # standard 16-digit
1234-5678-9012-3456                     # 16-digit with dashes
1234567890123456                        # 16-digit plain
1234-5678-9012                          # malformed (too short)
1234 5678 9012 345                      # 15 digit
1234 5678 9012 34567                    # 17 digit
4111111111111111                        # Visa
341111111111111                         # American Express
5111111111111111                        # MasterCard
371111111111111                         # Amex another

Times:
14:30                                  # 24-hour format
23:10                                  # 24-hour format
2:30 PM                                # 12-hour format
11:59 PM                               # 12-hour format
25:61                                  # invalid time
13:60                                  # invalid time
00:00 AM                               # 12-hour midnight
00:00                                  # standard 24-hour midnight
00:00 PM                               # invalid time
00:0                                   # Invalid time
0:00                                   # no leading zero 24-hour midnight
00.00                                  # dot separator

HTML tags:
<p>                                    # simple tag
<div class="example">                  # tag with attribute
<img src="image.jpg" alt="description">  # tag with multiple attributes
<a href="https://example.com" target="_blank"> # tag with URL attribute
<123invalid>                           # malformed tag
<selfclosing/>                         # self-closing tag

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
1200                                   # no specific currency
"""

# Dictionary of regex patterns for each data type to extract.
patterns = {
    # allows longer TLDs, prevents leading/trailing/consecutive dots in local part
    "emails": r"\b[a-zA-Z0-9](?:[a-zA-Z0-9._%+-]{0,62}[a-zA-Z0-9])?@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",

    # matches http(s), www, and domain-only URLs, supports query/fragment, and IDNs
    "urls": r"\b(?:https?://|www\.)[a-zA-Z0-9\-._~%]+(?:\.[a-zA-Z0-9\-._~%]+)+(?:/[^\s]*)?\b",

    # supports optional country code (1-4 digits), various separators, and parentheses
    "phone_numbers": r"\b(?:\+?\d{1,4}[-.\s]?)?(?:\(?\d{1,4}\)?[-.\s]?){1,2}\d{1,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b",

    # matches 13-19 digits, optional spaces/hyphens, and common credit card formats (including Visa, MasterCard, American Express)
    "credit_cards": r"\b(?:4[0-9]{12}|5[1-5][0-9]{14}|3[47][0-9]{13})\b",

    # matches 24h and 12h with AM/PM, prevents invalid time (minutes/hours)
    "times": r"\b((0?[1-9]|1[0-2]):[0-5]\d\s?[APap][Mm]|([01]?\d|2[0-3]):[0-5]\d)\b",

    # matches opening, closing, and self-closing tags, ignores invalid tags
    "html_tags": r"</?[a-zA-Z][a-zA-Z0-9]*(?:\s+[^<>]*)?/?>",

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

# Allow user to test user-provided data.
def test_user_data(patterns):
    """Allow the user to input text and test it against the provided regex patterns."""
    user_last_results = None
    while True:
        user_input = input(
            "\nEnter text to test (or type 'exit' to see your saved sample extraction): "
        )
        if user_input.lower() == "exit":
            if user_last_results:
                return user_last_results
            else:
                return None
        if not user_input.strip():
            print("Please enter your text.")
            continue

        user_test_results = {}
        for category, pattern in patterns.items():
            matches = re.findall(pattern, user_input, flags=re.IGNORECASE)
            user_test_results[category] = matches

        print("\n--- User Test Results ---")
        print_extracted_data(user_test_results)

        user_last_results = user_test_results  # save user results

        another_test = input("Test again? (yes/no): ")
        if another_test.lower() != "yes":
            return user_last_results

# Main program flow:
if __name__ == "__main__":
    # 1. Welcome user and get their name.
    user_name = welcome_user()
    # 2. Show user the navigation menu.
    while True:
        print("\nWhat would you like to do?")
        print("1. Test your own data")
        print("2. See built-in sample extracted data")
        print("3. Exit")
        choice = input("Enter 1, 2, or 3: ").strip()

        if choice == "1":
            try:
                user_results = test_user_data(patterns)
                if user_results and any(user_results.values()) and any(len(v) > 0 for v in user_results.values()):
                    save_to_files(user_results)
                    print("\nYour extracted data has been saved to respective files in this directory:")
                    time.sleep(0.5)
                    for file in os.listdir():
                        if file.endswith("_extracted.txt") or file == "all_extracted_data.txt":
                            print(f"  • {file}")
                            time.sleep(0.5)
                            print("Exit and list the files in your current directory to view/verify/reference.")
                else:
                    print("No data was entered/extracted!")
            except Exception as e:
                print(f"An error occurred during data testing: {e}")
        elif choice == "2":
            try:
                # 4. Extract data from the sample text using regex patterns.
                extracted = extract_data(sample_text)
                # 5. Display the extracted data on the local machine's console.
                print_extracted_data(extracted)
                # 6. Save the extracted data to files.
                save_to_files(extracted)
                print(f"Thank you for using the Regex Data Extraction Tool, {user_name}!\nAll data was extracted and saved successfully.\n")
                # 7. Display saved files.
                print("Saved extracted data files in this directory:")
                for file in os.listdir():
                    if file.endswith("_extracted.txt") or file == "all_extracted_data.txt":
                        print(f"  • {file}")
                        time.sleep(0.5)
                print("Exit and list the files in your current directory to view/verify/reference.")
            except Exception as e:
                print(f"An error occurred during extraction/saving: {e}")
        elif choice == "3":
            # 8. Print a completion/exit message.
            print("List the files in your current directory to view/verify/reference saved extracted data.")
            time.sleep(0.5)
            print(f"Goodbye, {user_name}! 👋")
            break
        else:
            print("Invalid option. Please enter 1, 2, or 3.")
            
