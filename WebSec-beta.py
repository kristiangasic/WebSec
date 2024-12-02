import os
import subprocess
import logging
import random
import requests
from urllib.parse import quote, urlparse
from bs4 import BeautifulSoup

# Logging-Konfiguration
logging.basicConfig(filename='done.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# SQLi und XSS Payloads
SQLI_PAYLOADS = ["' OR '1'='1", '" OR "1"="1', "' OR 1=1 --", '" OR 1=1 --']
XSS_PAYLOADS = ['<script>alert(1)</script>', '<img src="x" onerror="alert(1)">', '<svg onload=alert(1)>']

# Zufällige User-Agent- und Header-Manipulation
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

# Funktion zur Ausführung des Bash-Installationsskripts
def run_bash_setup():
    print("Starte das Installationsskript setup.sh...")
    try:
        subprocess.run(["sudo", "bash", "setup.sh"], check=True)
        print("Alle Tools wurden erfolgreich installiert!")
    except subprocess.CalledProcessError as e:
        logging.error(f"Fehler beim Ausführen von setup.sh: {e}")
        print(f"Fehler beim Ausführen von setup.sh: {e}")

# Funktion zum Abrufen von Exploits von Exploit-DB für WordPress
def get_exploits_for_wordpress():
    url = "https://www.exploit-db.com/search?q=wordpress"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise an exception for HTTP errors
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            exploits = []  # Liste der Exploits
            for link in soup.find_all('a', href=True):
                exploit_url = link['href']
                if "exploit" in exploit_url:
                    exploits.append(exploit_url)
            return exploits
    except requests.exceptions.RequestException as e:
        logging.error(f"Fehler beim Abrufen der Exploits von {url}: {e}")
        return []

# Funktion zur Überprüfung, ob es sich um eine WordPress-Seite handelt
def is_wordpress_site(url):
    # Einige typische WordPress-Dateien, die auf das Vorhandensein von WordPress hinweisen
    indicators = [
        "/wp-login.php",  # Login-Seite
        "/wp-admin/",      # Admin-Verzeichnis
        "/wp-content/",    # Inhalte von WordPress
    ]

    for indicator in indicators:
        test_url = url + indicator
        try:
            response = requests.get(test_url, timeout=10)
            if response.status_code == 200:
                logging.info(f"WordPress erkannt auf: {url}")
                return True
        except requests.RequestException:
            continue  # Wenn die Seite nicht erreichbar ist, überspringen

    return False

# WPScan zum Scannen von WordPress-Schwachstellen
def run_wpscan(domain):
    print(f"Starte WPScan für: {domain}")
    subprocess.run(["wpscan", "--url", domain, "--enumerate", "u", "--random-user-agent"])

# Amass zum Scannen von Subdomains
def run_amass(domain):
    subprocess.run(["/snap/bin/amass", "enum", "-d", domain])

# Nikto zum Überprüfen auf allgemeine Sicherheitslücken
def run_nikto(domain):
     subprocess.run(["nikto", "-h", domain, "-C", "all"])

# Gobuster zum Brute-Forcing von Verzeichnissen und Dateien
def run_gobuster(domain):
    subprocess.run(["gobuster", "dir", "-u", f"http://{domain}", "-w", "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"])

# Ffuf zum Brute-Forcing von Verzeichnissen und Dateien
def run_ffuf(domain):
    subprocess.run(["ffuf", "-u", f"http://{domain}/FUZZ", "-w", "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"])

# SQLMap zur Überprüfung auf SQL-Injection-Schwachstellen
def run_sqlmap(url):
    subprocess.run(["sqlmap", "-u", url, "--batch", "--risk=3", "--level=5"])

# Funktion zur Durchführung der vollständigen Sicherheitsprüfung
def scan_domain(domain):
    print(f"Starte den vollständigen Scan für: {domain}")

    # Überprüfen, ob es sich um eine WordPress-Seite handelt
    if is_wordpress_site(domain):
        # Holen der Exploits von Exploit-DB speziell für WordPress
        exploits = get_exploits_for_wordpress()
        if exploits:
            print(f"Gefundene Exploits für WordPress: {exploits}")
        else:
            print(f"Keine Exploits für WordPress gefunden.")
    else:
        print(f"Keine WordPress-Seite gefunden auf {domain}. Überspringe Exploit-Suche.")

    # Weitere Scans durchführen
    run_amass(domain)
    run_wpscan(domain)
    run_nikto(domain)
    run_gobuster(domain)
    run_ffuf(domain)

# Funktion zur Überprüfung von SQLi-Schwachstellen auf einer Webseite (mit sqlmap)
def check_sql_injection_with_sqlmap(url):
    try:
        result = subprocess.run(['sqlmap', '-u', url, '--batch', '--risk=3', '--level=5'], capture_output=True, text=True)
        if "sqlmap identified the following injection point" in result.stdout.lower():
            logging.info(f"SQLi Schwachstelle gefunden auf: {url}")
            return True
        return False
    except Exception as e:
        print(f"Fehler bei sqlmap: {e}")
        return False

# Funktion zur Überprüfung von XSS-Schwachstellen auf einer Webseite
def check_xss(url):
    for payload in XSS_PAYLOADS:
        encoded_payload = quote(payload)  # URL-Encoding
        response = requests.get(url + encoded_payload, headers=randomize_headers())
        if encoded_payload in response.text:
            logging.info(f"XSS Schwachstelle gefunden auf: {url} mit Payload: {encoded_payload}")
            return True
    return False

# Funktion zur Validierung und Ergänzung der URL
def validate_and_format_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    return url

# Menü und Benutzerinteraktion
def show_menu():
    while True:
        print("\nWähle eine Option aus:")
        print("1. Alle Tools installieren")
        print("2. Alle Sicherheitsprüfungen ausführen")
        print("3. Nur SQLi überprüfen")
        print("4. Nur XSS überprüfen")
        print("5. Subdomain-Scan durchführen")
        print("6. Verzeichnisscan durchführen (Gobuster/Ffuf)")
        print("7. Beenden")
        choice = input("Deine Wahl: ")

        if choice == "1":
            run_bash_setup()
        elif choice == "2":
            domain = input("Gib die zu scannende Domain ein: ")
            domain = validate_and_format_url(domain)  # URL validieren und formatieren
            scan_domain(domain)
        elif choice == "3":
            url = input("Gib die URL zum Überprüfen auf SQLi ein: ")
            url = validate_and_format_url(url)  # URL validieren und formatieren
            check_sql_injection_with_sqlmap(url)
        elif choice == "4":
            url = input("Gib die URL zum Überprüfen auf XSS ein: ")
            url = validate_and_format_url(url)  # URL validieren und formatieren
            check_xss(url)
        elif choice == "5":
            domain = input("Gib die zu scannende Domain ein: ")
            domain = validate_and_format_url(domain)  # URL validieren und formatieren
            run_amass(domain)
        elif choice == "6":
            domain = input("Gib die zu scannende Domain ein: ")
            domain = validate_and_format_url(domain)  # URL validieren und formatieren
            run_gobuster(domain)
            run_ffuf(domain)
        elif choice == "7":
            print("Beende das Skript.")
            break
        else:
            print("Ungültige Wahl, bitte versuche es erneut.")

# Skript starten
if __name__ == "__main__":
    show_menu()
