# XSSploit

**XSSploit** is a Python-based tool designed to identify and test vulnerabilities related to Cross-Site Scripting (XSS) in web applications. The tool currently supports testing for three types of XSS vulnerabilities:

- **Reflected XSS**
- **Stored XSS**
- **DOM-based XSS**

XSSploit is in its **beta version** and is under active development, with more features planned for future releases.

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
