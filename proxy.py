import requests
import threading
import time
import os
import socket
from colorama import Fore, Style, init
import platform
from bs4 import BeautifulSoup

init(autoreset=True)

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
}

def display_banner():
    print(Fore.RED + Style.BRIGHT + """
          ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗
          ██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝
          ██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝ 
          ██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝  
          ██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║   
          ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝
          Proxy Tool v1.0
          https://t.me/Humanpv
    """ + Style.RESET_ALL)

os.system('cls' if platform.system() == 'Windows' else 'clear')

def check_proxy(proxy, lock, live_proxies):
    ip, port = proxy.split(":")
    url = "http://www.google.com"
    try:
        start_time = time.time()
        response = requests.get(url, proxies={"http": f"http://{ip}:{port}", "https": f"http://{ip}:{port}"}, headers=headers, timeout=10)
        if response.status_code == 200:
            end_time = time.time()
            country = get_proxy_country(ip)
            response_time = round(end_time - start_time, 2)
            lock.acquire()
            live_proxies.append(f"{ip}:{port} - {country} - {response_time}s")
            print(Fore.GREEN + f"[+] Live Proxy: {ip}:{port} - Country: {country} - Time: {response_time}s")
            lock.release()
    except requests.RequestException:
        pass

def get_proxy_country(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            data = response.json()
            return data.get("country", "Unknown")
    except requests.RequestException:
        return "Unknown"
    return "Unknown"

def proxy_scrape():
    proxy_urls = [
        'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all',
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
        'https://www.proxy-list.download/api/v1/get?type=http',
        'https://api.openproxylist.xyz/http.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
        'https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt',
        'https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt',
        'https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt',
        'https://raw.githubusercontent.com/almroot/proxylist/master/list.txt',
        'https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt',
        'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
        'https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt',
        'https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt',
        'https://raw.githubusercontent.com/RX4096/proxy-list/main/online/http.txt',
        'https://raw.githubusercontent.com/saisuiu/uiu/main/free.txt',
        'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt',
        'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt'
        'https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all',
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all',
        'https://api.openproxylist.xyz/socks4.txt',
        'https://www.proxy-list.download/api/v1/get?type=socks4',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt',
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt',
        'https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks4.txt',
        'https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks4.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt',
        'https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS4.txt',
        'https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/socks4.txt',
        'https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt',
        'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt',
        'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt'
        'https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all',
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all',
        'https://www.proxy-list.download/api/v1/get?type=socks5',
        'https://api.openproxylist.xyz/socks5.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt',
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt',
        'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt',
        'https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt',
        'https://raw.githubusercontent.com/hyperbeats/proxy-list/main/socks5.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks5.txt',
        'https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt',
        'https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/socks5.txt',
        'https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt',
        'https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt',
        'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt',
        'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt'
    ]

    proxies = []
    for url in proxy_urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                proxy_list = response.text.splitlines()
                proxies.extend(proxy_list)
                print(Fore.GREEN + f"[+] Fetched {len(proxy_list)} proxies from {url}")
        except requests.RequestException:
            print(Fore.RED + f"[!] Failed to fetch proxies from {url}")

    if proxies:
        with open("proxy_list.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(proxies))
        print(Fore.GREEN + f"[+] Saved {len(proxies)} proxies to 'proxy_list.txt'")
    else:
        print(Fore.RED + "[!] No proxies fetched.")

def proxy_check():
    proxy_file = input(Fore.RED + "Enter the proxy file path (e.g., proxy_list.txt): " + Style.RESET_ALL)

    try:
        with open(proxy_file, "r", encoding="utf-8") as file:
            proxies = file.readlines()
    except FileNotFoundError:
        print(Fore.RED + f"[!] {proxy_file} not found.")
        return

    thread_count = int(input(Fore.RED + "threads [ 300 ]: " + Style.RESET_ALL))
    lock = threading.Lock()
    live_proxies = []

    threads = []
    for proxy in proxies:
        proxy = proxy.strip()
        if proxy:
            thread = threading.Thread(target=check_proxy, args=(proxy, lock, live_proxies))
            threads.append(thread)
            thread.start()
        
        if len(threads) >= thread_count:
            for t in threads:
                t.join()
            threads = []
    
    for t in threads:
        t.join()

    with open("Live.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(live_proxies))
    
    print(Fore.GREEN + f"[+] {len(live_proxies)} live proxies saved to 'Live.txt'")

def main():
    display_banner()

    while True:
        print("              1 Proxy Scrape")
        print("              2 Checker Prox")
        print("              3 Exit")
        choice = input(Fore.RED + "=> " + Style.RESET_ALL)

        if choice == '1':
            proxy_scrape()
        
        elif choice == '2':
            proxy_check()

        elif choice == '3':
            print(Fore.GREEN + "Exiting program.")
            break

        else:
            print(Fore.RED + "Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
