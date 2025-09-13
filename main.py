#!/usr/bin/env python3
import ftplib
import socket
from urllib.parse import urlparse

def normalize_host(raw):
    parsed = urlparse(raw)
    if parsed.scheme:  # kalau ada http/https
        return parsed.hostname
    return raw.strip().replace("/", "")

def check_ftp(host):
    try:
        ftp = ftplib.FTP()
        ftp.connect(host, 21, timeout=5)
        ftp.login("anonymous", "anonymous@example.com")
        print(f"[+] Anonymous FTP login allowed: {host}")
        ftp.quit()
        return True
    except ftplib.error_perm as e:
        print(f"[-] Not allowed: {host} ({e})")
    except (socket.error, socket.gaierror, ConnectionRefusedError) as e:
        print(f"[!] Connection failed: {host} ({e})")
    return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Check subdomains for anonymous FTP login")
    parser.add_argument("input", help="File containing live subdomains (e.g., live.txt)")
    parser.add_argument("-o", "--output", default="ftp_anonymous.txt", help="Output file")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        hosts = [normalize_host(line) for line in f if line.strip()]

    results = []
    for host in hosts:
        if check_ftp(host):
            results.append(host)

    with open(args.output, "w") as out:
        for r in results:
            out.write(r + "\n")

    print(f"\n[✓] Scan finished. Results saved in {args.output}")

if __name__ == "__main__":
    main()
