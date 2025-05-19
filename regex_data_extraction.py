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
