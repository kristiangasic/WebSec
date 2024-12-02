#!/bin/bash

# Füge den Snap-Pfad zu den Umgebungsvariablen hinzu
export PATH=$PATH:/snap/bin

# Überprüfen und Installieren von SQLmap
echo "Überprüfe SQLmap..."
if ! command -v sqlmap &> /dev/null; then
    echo "SQLmap nicht gefunden. Installation wird gestartet..."
    sudo apt-get install -y sqlmap
    echo "SQLmap wurde erfolgreich installiert."
else
    echo "SQLmap ist bereits installiert."
fi

# Überprüfen und Installieren von WPScan
echo "Überprüfe WPScan..."
if ! command -v wpscan &> /dev/null; then
    echo "WPScan nicht gefunden. Installation wird gestartet..."
    sudo apt update
    sudo apt install -y ruby-full ruby-dev libcurl4-openssl-dev libffi-dev make zlib1g-dev
    sudo gem install wpscan
    echo "WPScan wurde erfolgreich installiert."
else
    echo "WPScan ist bereits installiert."
fi

# Überprüfen und Installieren von Amass
echo "Überprüfe Amass..."
if ! command -v amass &> /dev/null; then
    echo "Amass nicht gefunden. Installation wird gestartet..."
    # Überprüfen, ob snap installiert ist
    if ! command -v snap &> /dev/null; then
        echo "Snap ist nicht installiert. Installiere Snap..."
        sudo apt update
        sudo apt install -y snapd
        echo "Snap wurde erfolgreich installiert."
    fi
    echo "Installiere Amass mit Snap..."
    sudo snap install amass
    echo "Amass wurde erfolgreich installiert."
else
    echo "Amass ist bereits installiert."
fi

# Überprüfen und Installieren von Nmap
echo "Überprüfe Nmap..."
if ! command -v nmap &> /dev/null; then
    echo "Nmap nicht gefunden. Installation wird gestartet..."
    sudo apt-get install -y nmap
    echo "Nmap wurde erfolgreich installiert."
else
    echo "Nmap ist bereits installiert."
fi

# Überprüfen und Installieren von Nikto
echo "Überprüfe Nikto..."
if ! command -v nikto &> /dev/null; then
    echo "Nikto nicht gefunden. Installation wird gestartet..."
    sudo apt-get install -y nikto
    echo "Nikto wurde erfolgreich installiert."
else
    echo "Nikto ist bereits installiert."
fi

# Überprüfen und Installieren von Gobuster
echo "Überprüfe Gobuster..."
if ! command -v gobuster &> /dev/null; then
    echo "Gobuster nicht gefunden. Installation wird gestartet..."
    sudo apt-get install -y gobuster
    echo "Gobuster wurde erfolgreich installiert."
else
    echo "Gobuster ist bereits installiert."
fi

# Überprüfen und Installieren von FFUF
echo "Überprüfe FFUF..."
if ! command -v ffuf &> /dev/null; then
    echo "FFUF nicht gefunden. Installation wird gestartet..."
    sudo apt install -y ffuf
    echo "FFUF wurde erfolgreich installiert."
else
    echo "FFUF ist bereits installiert."
fi

echo "Alle Tools wurden überprüft und installiert, falls erforderlich."
