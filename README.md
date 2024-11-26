# XSSploit

**XSSploit** is a Python-based tool designed to identify and test vulnerabilities related to Cross-Site Scripting (XSS) in web applications. The tool currently supports testing for three types of XSS vulnerabilities:

- **Reflected XSS**
- **Stored XSS**
- **DOM-based XSS**

XSSploit is in its **beta version** and is under active development, with more features planned for future releases.

![image](https://github.com/user-attachments/assets/cd339bbf-affe-4611-9a13-c948f0b915c9)

---

## Features

- **Web Crawling**: Crawls websites up to a user-defined depth to discover forms and input fields.
- **Targeted XSS Testing**: 
  - Reflected XSS detection
  - Stored XSS testing
  - DOM-based XSS manual testing
- **Payload Management**: Load payloads from a customizable text file for flexible testing.
- **Easy-to-Use Interface**: Simple prompts guide users through the process of testing vulnerabilities.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Binary-Assassin/XSSploit.git
   cd XSSploit
   pip install -r requirements.txt
   python xsstest.py

--- 

## Usage

1. **Launch the tool**:
   ```bash
   python xssploit.py
2. **Enter the required inputs when prompted:**

- **Base URL:** The starting URL for web crawling.
- **Crawling Depth:** Depth for crawling links and forms.


![image](https://github.com/user-attachments/assets/da76bfaa-4b27-42c8-a07d-d2a97534f6c6)

3. **Choose the type of XSS to test:**

- 1: Reflected XSS
- 2: Stored XSS
- 3: DOM-based XSS
- 4: Test all XSS types

![image](https://github.com/user-attachments/assets/dc0d5f6e-f8e7-474c-844e-8524ac53567f)
![image](https://github.com/user-attachments/assets/a0738c0d-114f-4d43-9ed4-e08356fbd606)


4. **Follow the results to analyze vulnerabilities:**
  - For Reflected and Stored XSS: The tool tests and outputs vulnerabilities found.
  - For DOM-based XSS: URLs are generated for manual testing in a browser.

5. **View the findings report**:
   - After running the tool, findings are saved in a file located in the `documentation` folder.
   - The file name is formatted as `findings_<timestamp>.txt`.
   - Open the file to analyze the detected vulnerabilities and generated test URLs.
  
---
## About


