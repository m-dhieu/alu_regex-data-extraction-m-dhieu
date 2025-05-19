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
