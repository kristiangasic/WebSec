#!/bin/bash

# Add Snap path to environment variables
export PATH=$PATH:/snap/bin

# Install Git if not already installed
echo "Checking if Git is installed..."
if ! command -v git &> /dev/null; then
    echo "Git not found. Installing Git..."
    sudo apt-get install -y git snapd snap python3 python3-pip
else
    echo "Git, python3 and pip3 is already installed."
fi

# Ensure pip3 is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 could not be found, please install pip3."
    exit 1
fi

# Install pyExploitDb
echo "Installing pyExploitDb..."
sudo pip3 install pyExploitDb --break-system-packages
sudo pip3 install pyExploitDb

# Verify pyExploitDb installation
if python3 -c "import pyExploitDb" &> /dev/null; then
    echo "pyExploitDb successfully installed."
else
    echo "Failed to install pyExploitDb."
fi

# Install other tools
echo "Checking and installing other security tools..."

# Check and install Nmap
if ! command -v nmap &> /dev/null; then
    echo "Nmap not found. Installing Nmap..."
    sudo apt-get update
    sudo apt-get install -y nmap
    echo "Nmap installed."
else
    echo "Nmap is already installed."
fi

# Verify Nmap installation
echo "Verifying Nmap installation..."
if command -v nmap &> /dev/null; then
    echo "Nmap version: $(nmap --version | head -n 1)"
else
    echo "Nmap installation failed."
    exit 1
fi

# Check and install SQLmap
if ! command -v sqlmap &> /dev/null; then
    sudo apt-get install -y sqlmap
    echo "SQLmap installed."
else
    echo "SQLmap is already installed."
fi

# Check and install WPScan
if ! command -v wpscan &> /dev/null; then
    sudo apt update
    sudo apt install -y ruby-full ruby-dev libcurl4-openssl-dev libffi-dev make zlib1g-dev
    sudo gem install wpscan
    echo "WPScan installed."
else
    echo "WPScan is already installed."
fi

# Install Amass using Snap
if ! command -v amass &> /dev/null; then
    sudo snap install amass
    echo "Amass installed."
else
    echo "Amass is already installed."
fi

# Install Gobuster
if ! command -v gobuster &> /dev/null; then
    sudo apt-get install -y gobuster
    echo "Gobuster installed."
else
    echo "Gobuster is already installed."
fi

# Install FFUF
if ! command -v ffuf &> /dev/null; then
    sudo apt-get install -y ffuf
    echo "FFUF installed."
else
    echo "FFUF is already installed."
fi

# Install Nikto
if ! command -v nikto &> /dev/null; then
    sudo apt-get install -y nikto
    echo "Nikto installed."
else
    echo "Nikto is already installed."
fi

# Install Dirbuster wordlist if it doesn't exist
if [ ! -f "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt" ]; then
    echo "Directory list wordlist not found. Downloading the wordlist..."
    sudo mkdir -p /usr/share/wordlists/dirbuster
    sudo curl -o /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt https://raw.githubusercontent.com/daviddias/node-dirbuster/refs/heads/master/lists/directory-list-2.3-medium.txt
    echo "Dirbuster wordlist downloaded."
else
    echo "Wordlist directory-list-2.3-medium.txt already exists."
fi

# Install SecLists (alternative wordlist collection)
#if [ ! -d "$HOME/SecLists" ]; then
#    echo "SecLists not found. Cloning SecLists repository..."
#    git clone https://github.com/danielmiessler/SecLists.git $HOME/SecLists
#    echo "SecLists cloned."
#else
#    echo "SecLists already exists."
#fi

echo "All required tools installed."
