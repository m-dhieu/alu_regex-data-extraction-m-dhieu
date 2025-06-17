# Regex Data Extraction Tool

This tool extracts various data types from text using Regular Expressions (regex). It supports extracting email addresses, URLs, phone numbers, credit card numbers, times (12h/24h), HTML tags, and currency amounts. These data types are essential for web scraping, data validation, and information retrieval from diverse text sources. The tool provides interactive prompts and progress updates, allows the user to view sample data or test their own data, and saves extracted data into separate files and a combined summary file.

---

## Table of Contents

- [Setup Instructions](#setup-instructions)
- [Usage Instructions](#usage-instructions)
- [Directory Structure](#directory-structure)
- [Tool Features](#tool-features)
- [Contributing](#contributing)
- [License](#license)
- [Resources](#resources)
- [Contact Information](#contact-information)

---

## Setup Instructions

### Step 1: Clone the repository in your local machine (Linux terminal). Use:
```
git clone https://github.com/m-dhieu/alu_regex-data-extraction-m-dhieu.git
```

### Step 2: Navigate to the cloned repository. Use:
```
cd alu_regex-data-extraction-m-dhieu
```

### Step 3: Run the data extraction script. Use:
```
python3 regex_data_extraction.py
```

---

## Usage Instructions

- Enter your name when prompted to personalize your experience.
- Read the progress messages to be informed on the data extraction progress.
- Navigate the menu to test your data or view sample extracted data.
- View saved extracted data in their respective individual text files (e.g., `emails_extracted.txt`) or the combined summary file, `all_extracted_data.txt`, in your console.
- Modify the `sample_text` variable in the data extraction script to test data that suits you (This data is in-built and not the same as the one that you enter on your console for testing).
- **Note:** Once you exit the tool, you have to run the script again to view the navigation menu. You will have to test new data, as you will automatically have no saved extracted data at this point.

---

## Directory Structure

```
alu_regex-data-extraction-m-dhieu/
├── README.md                      # project documentation
├── regex_data_extraction.py       # main Python script  
├── .gitignore                     # file tracker
└── (name)_extracted_data.txt      # separate extracted data files and a combined all extracted data file
```

---

## Tool Features

- **Data Extraction:** Data is extracted using regex patterns that handle multiple formats and common edge cases.
- **Interactive Experience:** The user's name with greetings and progress updates personalize the user's interaction with the tool.
- **File Output:** Extracted data are saved to separate files and a combined summary file for verification or reference.
- **Customizable:** Sample text or regex patterns can be modified to test different data.
- **Lightweight:** Pure built-in Python libraries(`os`, `stat`, `sys`, `re` and,  `time`) are used; thus,  no external dependencies need to be installed. 
-Python's `re` module with case-insensitive regex patterns handles data search/extraction. Python's `time` module manages the console output's interactive timing and pacing, thus enhancing readability. Python's `os`, `stat`, and `sys` modules track the absolute path of the script and handle permission changes.

---

## Contributing

Welcome to contribute:

1. Fork the repository.

2. Create a new branch for your feature or bug fix.

3. Commit your changes with clear, concise messages.

4. Push to your fork and open a pull request.

Thank you for considering to contribute. Feel free to open issues for questions, suggestions, or bug reports.

---

## License

This project is under the MIT License.

---

## Resources

- [Regular Expressions (Regex) Tutorial - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions)
- [Python `re` Module Documentation](https://docs.python.org/3/library/re.html)
- [Regex101 - Online Regex Tester](https://regex101.com/)
- [Automate the Boring Stuff with Python - Regex Chapter](https://automatetheboringstuff.com/2e/chapter7/)
- [Python File I/O - Real Python](https://realpython.com/read-write-files-python/)

---

## Contact Information

For any queries or feedback, reach out to:

**Monica Dhieu**  
Email: [m.dhieu@alustudent.com](mailto:m.dhieu@alustudent.com)  
GitHub: [https://github.com/m-dhieu](https://github.com/m-dhieu)  

---

*Monday, May 19, 2025*
