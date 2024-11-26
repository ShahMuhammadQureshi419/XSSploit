import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from art import *
from datetime import datetime

# Function to create a findings report
def create_documentation_file():
    if not os.path.exists("documentation"):
        os.makedirs("documentation")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"documentation/findings_{timestamp}.txt"
    return file_path

# Function to write findings to the report
def write_to_documentation(file_path, content):
    with open(file_path, "a") as file:
        file.write(content + "\n")

# Load payloads from a file
def load_payloads(file_path):
    if not os.path.exists(file_path):
        print(f"[-] Payload file not found: {file_path}")
        return []
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Crawl website for forms and links
def web_crawler(base_url, max_depth=2):
    print("[+] Starting Web Crawler...")
    visited = set()
    to_visit = [(base_url, 0)]  # (url, depth)
    forms = []

    while to_visit:
        url, depth = to_visit.pop(0)
        if depth > max_depth or url in visited:
            continue

        print(f"[Crawling] {url} (Depth: {depth})")
        visited.add(url)

        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract forms
            for form in soup.find_all('form'):
                action = form.get('action')
                method = form.get('method', 'get').lower()
                inputs = form.find_all('input')
                form_data = {"action": urljoin(url, action), "method": method, "inputs": inputs}
                forms.append(form_data)

            # Extract links for further crawling
            for link in soup.find_all('a', href=True):
                link_url = urljoin(url, link['href'])
                if link_url not in visited:
                    to_visit.append((link_url, depth + 1))
        except Exception as e:
            print(f"[-] Error crawling {url}: {e}")

    print(f"[+] Finished crawling. {len(forms)} forms discovered.")
    return forms

# Test forms for Reflected and Stored XSS
def test_forms(forms, payloads, xss_type, doc_file):
    print("\n[+] Testing Forms for XSS...")
    for form in forms:
        url = form['action']
        method = form['method']
        inputs = form['inputs']

        for payload in payloads:
            form_data = {}
            for input_field in inputs:
                input_name = input_field.get('name')
                if input_name:
                    form_data[input_name] = payload

            try:
                if method.lower() == 'post':
                    response = requests.post(url, data=form_data, timeout=10)
                else:
                    response = requests.get(url, params=form_data, timeout=10)

                if payload in response.text:
                    finding = f"[+] {xss_type.capitalize()} XSS Detected! URL: {url}, Payload: {payload}"
                    print(finding)
                    write_to_documentation(doc_file, finding)
                else:
                    safe_message = f"[-] Payload safe for URL: {url}, Payload: {payload}"
                    print(safe_message)
                    write_to_documentation(doc_file, safe_message)
            except Exception as e:
                error_message = f"[-] Error testing form at {url}: {e}"
                print(error_message)
                write_to_documentation(doc_file, error_message)

# Test DOM-based XSS
def test_dom_xss(base_url, payloads, doc_file):
    print("\n[+] Testing for DOM-based XSS...")
    for payload in payloads:
        test_url = f"{base_url}?input={payload}"
        finding = f"[!] Test manually: {test_url}\n   - Check browser console for execution."
        print(finding)
        write_to_documentation(doc_file, finding)

# Main function
def main():
    print(text2art("XSS Tester"))
    print("Welcome to the XSS Testing Tool!")
    base_url = input("Enter the base URL: ").strip()
    max_depth = int(input("Enter the crawling depth: "))
    payload_file = "payloads.txt"

    # Load payloads from file
    payloads = load_payloads(payload_file)
    if not payloads:
        print("[-] No payloads loaded. Exiting.")
        return

    # Crawl the website
    forms = web_crawler(base_url, max_depth)

    # Create documentation file
    doc_file = create_documentation_file()
    print(f"\n[+] Documentation will be saved in: {doc_file}\n")

    # Choose the type of XSS testing
    print("Choose the type of XSS to test:")
    print("1. Reflected XSS")
    print("2. Stored XSS")
    print("3. DOM-based XSS")
    print("4. Test all XSS types")
    choice = int(input("Enter your choice (1-4): "))

    # Run tests based on user choice
    if choice == 1:
        test_forms(forms, payloads, "reflected", doc_file)
    elif choice == 2:
        test_forms(forms, payloads, "stored", doc_file)
    elif choice == 3:
        test_dom_xss(base_url, payloads, doc_file)
    elif choice == 4:
        test_forms(forms, payloads, "reflected", doc_file)
        test_forms(forms, payloads, "stored", doc_file)
        test_dom_xss(base_url, payloads, doc_file)
    else:
        print("[-] Invalid choice. Exiting.")

    print(f"\n[+] Documentation saved in: {doc_file}")

if __name__ == "__main__":
    main()
