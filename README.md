# WebSec: Automated Web Security Scanner

WebSec is a Python3-based web security scanner designed to identify common vulnerabilities like SQL Injection (SQLi) and Cross-Site Scripting (XSS) on websites. It also includes tools for performing subdomain enumeration, directory brute-forcing, and other security checks.

The project comes with a `setup.sh` script that automates the installation of all necessary tools like SQLmap, WPScan, Amass, Nmap, Nikto, Gobuster, and FFUF.

## Features

- **SQL Injection Check**: Detects SQL injection vulnerabilities using SQLmap.
- **XSS Check**: Detects Cross-Site Scripting (XSS) vulnerabilities.
- **Subdomain Enumeration**: Uses Amass to discover subdomains of a domain.
- **Directory Bruteforce**: Uses Gobuster and FFUF for directory and file brute-forcing.
- **WordPress Exploit Search**: Retrieves exploits for WordPress websites from Exploit-DB.
- **Automated Tool Installation**: The `setup.sh` script installs all required tools automatically.

## Prerequisites

- **Python 3** (version 3.6 or higher)
- **Ubuntu/Debian** or a compatible Linux distribution
- **Snap** (for installing Amass via Snap)

## Installation

### 1. **Run the Setup Script** (Installs all required tools)

Before using the Python script, make sure all necessary tools are installed. Run the `setup.sh` script to handle the installation process.

```bash
chmod +x setup.sh
./setup.sh
```

The `setup.sh` script will check for and install the following tools (if they are not already installed):

- **SQLmap**
- **WPScan**
- **Amass**
- **Nmap**
- **Nikto**
- **Gobuster**
- **FFUF**

If `snap` is not already installed, the script will also install `snapd` to allow the installation of Amass via Snap.

### 2. **Run the Python Script**

After the necessary tools have been installed, you can run the Python3 script to perform web security checks.

```bash
python3 WebSec-Beta.py
```

### 3. **Usage**

Once the script is running, you will be prompted to choose from the following options:

1. **Install all tools**: Installs all required tools.
2. **Run all security checks**: Runs all security checks on a specified domain.
3. **Check for SQLi vulnerabilities**: Checks a website for SQL-Injection vulnerabilities.
4. **Check for XSS vulnerabilities**: Checks a website for XSS vulnerabilities.
5. **Run Subdomain Scan**: Performs subdomain enumeration on the specified domain.
6. **Run Directory Scan**: Performs a directory brute-force scan using Gobuster and FFUF.
7. **Exit**: Exits the script.

### Example Workflow:

```bash
Choose an option:
1. Install all tools
2. Run all security checks
3. Check for SQLi vulnerabilities
4. Check for XSS vulnerabilities
5. Run subdomain scan
6. Run directory scan (Gobuster/FFUF)
7. Exit
Your choice: 2
Enter the domain to scan: example.com
Starting full scan for: http://example.com
No WordPress exploits found.
```

### 4. **Troubleshooting**

If you encounter any issues while running the script, ensure that:

- All dependencies are correctly installed.
- The path to `amass` is correct. If `amass` is not found, check that you are running the script with proper permissions, or that `snap` is properly installed on your system.

## License

This project is licensed under the [MIT License](LICENSE).

---

Thank you for using WebSec! If you have any questions or suggestions for improvements, feel free to create an [Issue](https://github.com/kristiangasic/WebSec/issues) on GitHub.

