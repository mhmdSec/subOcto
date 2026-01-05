import requests
from bs4 import BeautifulSoup
import subprocess
import os
banner = r'''
 ██████  █    ██  ▄▄▄▄    ▒█████   ▄████▄  ▄▄▄█████▓ ▒█████  
▒██    ▒  ██  ▓██▒▓█████▄ ▒██▒  ██▒▒██▀ ▀█  ▓  ██▒ ▓▒▒██▒  ██▒
░ ▓██▄   ▓██  ▒██░▒██▒ ▄██▒██░  ██▒▒▓█    ▄ ▒ ▓██░ ▒░▒██░  ██▒
  ▒   ██▒▓▓█  ░██░▒██░█▀  ▒██   ██░▒▓▓▄ ▄██▒░ ▓██▓ ░ ▒██   ██░
▒██████▒▒▒▒█████▓ ░▓█  ▀█▓░ ████▓▒░▒ ▓███▀ ░  ▒██▒ ░ ░ ████▓▒░
▒ ▒▓▒ ▒ ░░▒▓▒ ▒ ▒ ░▒▓███▀▒░ ▒░▒░▒░ ░ ░▒ ▒  ░  ▒ ░░   ░ ▒░▒░▒░ 
░ ░▒  ░ ░░░▒░ ░ ░ ▒░▒   ░   ░ ▒ ▒░   ░  ▒       ░      ░ ▒ ▒░ 
░  ░  ░   ░░░ ░ ░  ░    ░ ░ ░ ░ ▒  ░          ░      ░ ░ ░ ▒  
      ░     ░      ░          ░ ░  ░ ░                   ░ ░  
                        ░          ░                          

                      Created by mhmdsec
_______________________________________________________________
'''
print(banner)
domain = input("Please add the domain > ")
file_name = f"{domain}_subs.txt"

def subDomainFinderWebsite(domain, file_name):
    print("First you should know the history in the website")
    today =input("Enter scan date (YYYY-MM-DD): ")
    print(f"[*] Running Subdomainfinder.c99.nl for: {domain}")
    url = f"https://subdomainfinder.c99.nl/scans/{today}/{domain}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    print("Connecting to subdomainfinder.c99.nl ......")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            found_tags = soup.find_all('a', class_="link sd")
            
            subdomains = []
            
            for tag in found_tags: 
                subDomain = tag.get_text().strip()
                if subDomain:
                    subdomains.append(subDomain)
            
            if subdomains:
                with open(file_name, "a") as f:
                    for sub in subdomains:
                        f.write(sub + "\n")
                print("Finished collecting subDomains successfully")
            else:
                print("No subdomains found on the page.")
        else:
            print(f"Failed to connect. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")


def subFinderTool(domain, file_name):
        print(f"[*] Running Subfinder for {domain}...")
        result = subprocess.run(['subfinder','-d',domain,"-silent"], capture_output=True ,text=True, check=True)
        subfinder_subs = result.stdout.strip()
        if subfinder_subs:
            with open(file_name,"a") as f:
                f.write(subfinder_subs+"\n")

def filter_results(file_path):
    if os.path.exists(file_path):
        print("[*] Filtering duplicates...")
        with open(file_path, "r") as f:
            lines = f.readlines()
        unique_lines = sorted(set(line.strip() for line in lines if line.strip()))
        with open(file_path, "w") as f:
            for line in unique_lines:
                f.write(line + "\n")
        print(f"[+] Done! Total unique subdomains: {len(unique_lines)}")

subDomainFinderWebsite(domain, file_name)
subFinderTool(domain, file_name)

filter_results(file_name)