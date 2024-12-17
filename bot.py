import requests
import time
from datetime import datetime, timezone
import json
from colorama import Fore, Style, init
import signal
import sys

# Initialize colorama
init(autoreset=True)

# URL target
contribute_url = "https://api.hivera.org/engine/contribute"
powers_url = "https://api.hivera.org/users/powers"
auth_url = "https://api.hivera.org/auth"  # Endpoint to check username

# Log file for errors
error_log_file = "error.log"

# Banner
def display_banner():
    banner = """
 █████╗ ██╗██████╗ ██████╗ ██████╗  ██████╗ ██████╗      █████╗ ███████╗ ██████╗
██╔══██╗██║██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗    ██╔══██╗██╔════╝██╔════╝
███████║██║██████╔╝██║  ██║██████╔╝██║   ██║██████╔╝    ███████║███████╗██║     
██╔══██║██║██╔══██╗██║  ██║██╔══██╗██║   ██║██╔═══╝     ██╔══██║╚════██║██║     
██║  ██║██║██║  ██║██████╔╝██║  ██║╚██████╔╝██║         ██║  ██║███████║╚██████╗
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝         ╚═╝  ╚═╝╚══════╝ ╚═════╝
                                                                                
====================================================
     BOT                : Hivera Minning 
     Telegram Channel   : @airdropasc
     Telegram Group     : @autosultan_group
====================================================
"""
    print(Fore.GREEN + banner)
    time.sleep(2)

# Graceful exit handler
def exit_handler(sig, frame):
    print(f"\n{Fore.YELLOW}Thank you for using Hivera Bot!{Style.RESET_ALL}")
    sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)

auth_data_file = "data.txt"
auth_data_list = []

try:
    with open(auth_data_file, "r") as file:
        auth_data_list = [line.strip() for line in file.readlines() if line.strip()]
    print(f"{Fore.YELLOW}Loaded {len(auth_data_list)} accounts.{Style.RESET_ALL}")
except FileNotFoundError:
    print(f"{Fore.RED}Error: The file {auth_data_file} was not found.{Style.RESET_ALL}")

proxies = []
use_proxy = False
config_file = "config.json"
try:
    with open(config_file, "r") as f:
        config = json.load(f)
        min_power = config.get("min_power", 500)  # Default
        use_proxy = config.get("use_proxy", False)
except FileNotFoundError:
    print(f"{Fore.RED}Config file not found. Using default configuration.{Style.RESET_ALL}")
    min_power = 500

if use_proxy:
    try:
        with open("proxy.txt", "r") as proxy_file:
            proxies = [line.strip() for line in proxy_file.readlines() if line.strip()]
        print(f"{Fore.GREEN}Loaded {len(proxies)} proxies.{Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.RED}Proxy file not found. Proceeding without proxies.{Style.RESET_ALL}")

# Log errors
def log_error(message):
    with open(error_log_file, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

def get_username(auth_data):
    try:
        response = requests.get(f"{auth_url}?auth_data={auth_data}", headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            result = response.json().get("result", {})
            username = result.get("username", "Unknown")
            return username
        else:
            print(f"{Fore.RED}Error fetching username.{Style.RESET_ALL}")
            return "Unknown"
    except Exception as e:
        log_error(f"Error fetching username: {e}")
        return "Unknown"

def check_power(auth_data, username, proxy=None):
    try:
        if proxy:
            response = requests.get(f"{powers_url}?auth_data={auth_data}", headers={"Content-Type": "application/json"}, proxies={"http": proxy, "https": proxy})
        else:
            response = requests.get(f"{powers_url}?auth_data={auth_data}", headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            power_data = response.json().get("result", {})
            current_power = power_data.get("POWER", 0)
            power_capacity = power_data.get("POWER_CAPACITY", 0)
            hivera = power_data.get("HIVERA", 0)

            if current_power >= min_power:
                return True, current_power, power_capacity
            else:
                return False, current_power, power_capacity
        else:
            return False, 0, 0
    except Exception as e:
        log_error(f"Error checking power: {e}")
        return False, 0, 0

def post_request(auth_data, username, proxy=None):
    from_date = int(datetime.now(timezone.utc).timestamp() * 1000)
    payload = {
        "from_date": from_date,
        "quality_connection": 100
    }

    try:
        if proxy:
            response = requests.post(f"{contribute_url}?auth_data={auth_data}", json=payload, headers={"Content-Type": "application/json"}, proxies={"http": proxy, "https": proxy})
        else:
            response = requests.post(f"{contribute_url}?auth_data={auth_data}", json=payload, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.text
    except Exception as e:
        log_error(f"Error sending request: {e}")
        return False, "Error occurred"

def print_header(title):
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{title}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'-' * (len(title) + 2)}{Style.RESET_ALL}")

# Main
if __name__ == "__main__":
    display_banner()
    proxy_index = 0
    while True:
        print_header("Account Processing")
        for auth_data in auth_data_list:
            username = get_username(auth_data)
            print(f"\n{Fore.CYAN}Processing account: {username}...{Style.RESET_ALL}")
            
            proxy = None
            if use_proxy:
                proxy = proxies[proxy_index % len(proxies)] if proxies else None
                print(f"{Fore.YELLOW}Using proxy: {proxy}{Style.RESET_ALL}")
            
            power_ok, current_power, power_capacity = check_power(auth_data, username, proxy)
            if power_ok:
                print(f"{Fore.GREEN}Power is sufficient: {current_power}/{power_capacity}{Style.RESET_ALL}")
                success, response = post_request(auth_data, username, proxy)
                if success:
                    hivera_balance = response.get('result', {}).get('profile', {}).get('HIVERA', 0)
                    print(f"{Fore.GREEN}Ping successful! Balance: {hivera_balance}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Request failed.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Power is low: {current_power}/{power_capacity}{Style.RESET_ALL}")
            
            time.sleep(5)

            if use_proxy and len(proxies) > 1:
                proxy_index += 1

        print(f"\n{Fore.YELLOW}Waiting 60 seconds before retrying all accounts...{Style.RESET_ALL}")
        time.sleep(60)
