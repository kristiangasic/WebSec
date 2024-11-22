### `README.md`
## **Author : Kristian Gasic**
## Status  :  **BETA**
```markdown
# 🔒 **Web Security Scanner** 🚀

An easy-to-use Python script that integrates various tools for web security testing. This script uses popular open-source tools like **WPScan**, **sqlmap**, **Nikto**, **Gobuster**, **Amass**, and more to identify vulnerabilities on websites.

## ⚙️ **Features**
- **WordPress Vulnerabilities:** WPScan checks for known vulnerabilities in WordPress websites.
- **SQL Injection (SQLi):** Tests for SQL injection vulnerabilities using **sqlmap**.
- **Cross-Site Scripting (XSS):** Checks for potential XSS vulnerabilities.
- **Subdomain Scanning:** **Amass** is used to find subdomains of a target domain.
- **Directory Scanning:** Brute-forces directories and files using **Gobuster** and **Ffuf**.
- **General Security Scan:** **Nikto** is used to scan for common security flaws.

## 📋 **Requirements**
- **Python 3.x**: You need Python 3 to run the script.
- **Tools**: Some tools need to be installed for the script to work. The script will help you install them.

## 🚀 **Installation**

### 1. **Clone the Repository**
First, you need to clone the repository. Open a terminal and run the following commands:

```bash
git clone https://github.com/kristiangasic/WebSec.git
cd WebSec
```

### 2. **Install Dependencies**
Install all the Python dependencies (like `requests` and `beautifulsoup4`) required for the script. Make sure you have **pip** installed:

```bash
pip3 install requests bs4
```

### 3. **Install the Tools**

The script can help you install the required tools. If they're not installed yet, you can install them with the following commands:

#### 1. **WPScan** (for WordPress Vulnerabilities)
WPScan is a tool specifically designed to scan WordPress sites for vulnerabilities. To install WPScan, follow these steps:

```bash
# Update apt and install required dependencies
sudo apt update
sudo apt install -y ruby-full ruby-dev libcurl4-openssl-dev libffi-dev make zlib1g-dev

# Install WPScan using gem (Ruby package manager)
sudo gem install wpscan
```

#### 2. **sqlmap** (for SQL Injection Testing)
**sqlmap** is a popular tool for detecting and exploiting SQL injection vulnerabilities:

```bash
# Install sqlmap using apt
sudo apt update
sudo apt install -y sqlmap
```

#### 3. **Nikto** (for General Security Scanning)
**Nikto** is an open-source web scanner that looks for various security issues:

```bash
# Install Nikto using apt
sudo apt update
sudo apt install -y nikto
```

#### 4. **Amass** (for Subdomain Enumeration)
**Amass** is a tool used for subdomain enumeration:

```bash
# Install Golang (Go) and Amass
sudo apt update
sudo apt install -y golang-go
apt-get update
apt-get install amass
```

#### 5. **Gobuster** (for Directory Scanning)
**Gobuster** is a tool used for brute-forcing directories and filenames:

```bash
# Install Gobuster using apt
sudo apt update
sudo apt install -y gobuster
```

#### 6. **Ffuf** (for Directory Scanning)
Alternatively to Gobuster, you can use **ffuf** for directory scanning:

```bash
# Install ffuf using apt
sudo apt update
sudo apt install -y ffuf
```

### 4. **Run the Script**
Once all the tools are installed, you can run the script:

```bash
python3 WebSec-Beta.py
```

You will then be prompted to choose an option:

- **Option 1**: Installs all the required tools
- **Option 2**: Performs all security checks
- **Option 3**: Checks for SQL Injection (SQLi) only
- **Option 4**: Checks for Cross-Site Scripting (XSS) only
- **Option 5**: Performs a subdomain scan
- **Option 6**: Performs a directory scan (Gobuster/Ffuf)
- **Option 7**: Exits the script

### 5. **Tools Used in the Script**

- **WPScan**: Used to scan for known vulnerabilities in WordPress sites.
- **sqlmap**: A tool for detecting SQL injection vulnerabilities.
- **Nikto**: An open-source web scanner for common security flaws.
- **Amass**: A tool for subdomain enumeration.
- **Gobuster/Ffuf**: Tools for brute-forcing directories and filenames.
- **requests and BeautifulSoup**: Used for XSS testing and fetching exploits from Exploit-DB.

### 6. **Example of a Full Scan**

Here's an example of how you can run the script:

```bash
Choose an option:
1. Install all tools
2. Run all security checks
3. Check for SQLi only
4. Check for XSS only
5. Run subdomain scan
6. Run directory scan (Gobuster/Ffuf)
7. Exit
Your choice: 2
Enter the domain to scan: example.com
Starting full scan for: example.com
```

## 🔐 **Important Notes**

- **Legality**: Ensure you have permission to scan the websites before using this script. Scanning websites without permission could be illegal.
- **Performance**: Some tools, such as **Gobuster** and **Amass**, can be resource-intensive. Ensure your system has enough resources.

## 📜 **License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

🤖 **Happy Scanning! Stay safe and secure!** 🔐
```
