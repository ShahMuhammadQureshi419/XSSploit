import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from art import *

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
def test_forms(forms, payloads, xss_type):
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
                if method == 'post':
                    response = requests.post(url, data=form_data, timeout=10)
                else:
                    response = requests.get(url, params=form_data, timeout=10)

                if payload in response.text:
                    if xss_type == "reflected":
                        print(f"[+] Reflected XSS Detected! URL: {url}, Payload: {payload}")
                    elif xss_type == "stored":
                        print(f"[+] Stored XSS Detected! URL: {url}, Payload: {payload}")
                else:
                    print(f"[-] Payload safe: {payload}")
            except Exception as e:
                print(f"[-] Error testing form at {url}: {e}")

# Test DOM-based XSS
def test_dom_xss(base_url, payloads):
    print("\n[+] Testing for DOM-based XSS...")
    for payload in payloads:
        test_url = f"{base_url}?input={payload}"
        print(f"[!] Test manually: {test_url}")
        print("   - Check browser console for execution.")

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

    # Choose XSS type
    print("\nSelect the type of XSS to test:")
    print("1. Reflected XSS")
    print("2. Stored XSS")
    print("3. DOM-based XSS")
    print("4. All")
    choice = input("Enter your choice (e.g., 1, 2, 3, or 4): ").strip()

    # Test based on choice
    if choice == "1":
        print("\n[+] Testing for Reflected XSS...")
        test_forms(forms, payloads, "reflected")
    elif choice == "2":
        print("\n[+] Testing for Stored XSS...")
        test_forms(forms, payloads, "stored")
    elif choice == "3":
        print("\n[+] Testing for DOM-based XSS...")
        test_dom_xss(base_url, payloads)
    elif choice == "4":
        print("\n[+] Testing for All XSS Types...")
        print("[*] Reflected XSS:")
        test_forms(forms, payloads, "reflected")
        print("[*] Stored XSS:")
        test_forms(forms, payloads, "stored")
        print("[*] DOM-based XSS:")
        test_dom_xss(base_url, payloads)
    else:
        print("[-] Invalid choice. Exiting.")

if __name__ == "__main__":
    main()

