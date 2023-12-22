import requests
from bs4 import BeautifulSoup
# Sono tutte le variabili universali
USERNAME = "admin"     # SARÀ L'USERNAME USATA PER ENTRARE DENTRO DVWA/LOGIN
PASSWORD = "password"  # SARÀ LA PASSWORD USATA PER ENTRARE DENTRO DVWA/LOGIN
#PHP_ID = None   
DIFFICULTY = "low"
BASE_URL = "http://192.168.1.85/dvwa"   # CAMBIARE IP CON QUELLO DEL TUO BRUTERFORD
USERNAME_WORDLISTS  = "/home/kali/Desktop/Build_week/nome1.txt" # cambiare il percorso del file
PASSWORD_WORDLISTS  = "/home/kali/Desktop/Build_week/pass.txt" # cambiare il percorso del file
proxies = {"http": "http://127.0.0.1:8080"}
 

def main():
    init_app()
              
def init_app():
    global USERNAME, PASSWORD, BASE_URL, PHP_ID
    #va a prendere il cookie 
    url = BASE_URL + "/login.php"
    r = requests.get(url, proxies=proxies)  # MANDA LA PRIMA RICHIESTA GET AL SITO
    try:
        cookies = r.headers['Set-Cookie']    # PRENDE TUTTO IL SET COOKIE DALLA RICHIESTA 
    except KeyError as e:
        print("[ERROR] - Server did not send PHPSESSID cookie, need to init DVWA") #
        exit()       
    PHP_ID = cookies.split(";")[0].split("=")[1]  # PRENDE IL PHPSESSID DAL SET COOKIE, 
    #################################################FINISCE IL PRIMO GET PRENDENDO PHPSESSID
    
    custom_headers = {
        "Content-Type": "application/x-www-form-urlencoded",      #INSERIAMO IL MESSAGGIO CHE DEVE MANDARE
        "Cookie": f"security=high; PHPSESSID={PHP_ID}",
        "Upgrade-Insecure-Requests": "1",
    }
    post_data = f"username={USERNAME}&password={PASSWORD}&Login=Login"  ### INSERIAMO LA PARTE FINALE, CIOÈ LA DATA CON USERNAME E PASSWORD CORETTE
    r = requests.post(url, headers=custom_headers, data=post_data, proxies=proxies, allow_redirects=False)  #MANDA LA RICHIESTA POST,PER ENTRARE DENTRO DVWA
    ###################################################FINITO 2 RICHIESTA
    
    # MANDA IL GET
    custom_headers = {
        "Referer": url,
        "Cookie": f"security=high; PHPSESSID={PHP_ID}", ##### INSERIAMO IL MESSAGGIO CHE DEVE MANDARE
        }
    r = requests.get(url, headers=custom_headers, proxies=proxies) ### MANDA LA RICHIESTA GET, PER VERIFICARE SE È ENTRATO 
    soup = BeautifulSoup(r.text, "html.parser")
    risultato = soup.find("You have logged in as 'admin'")
    if risultato:
        print("Siamo entrati")
    ###############################RIUSCITOOOOOOOOOO
    
    ############################# ENTRIAMO NELLA pagina principale di INDEX
    url1 = BASE_URL + "/index.php"
    custom_headers = {
        "Referer": "http://192.168.1.85/dvwa/login.php",       ## cambia IP
        "Cookie": f"security=high; PHPSESSID={PHP_ID}", 
        "Upgrade-Insecure-Requests": "1"
   
    }
    r = requests.get(url1, headers=custom_headers, proxies=proxies)
    
   #######CAMBIARE DA HIGH A LOW
   
   url2 = BASE_URL + "/dvwa/js/dvwaPage.js"
   custom_headers = {
        "Referer": "http://192.168.1.85/dvwa/index.php",   # cambia IP
        "Cookie": f"security=high; PHPSESSID={PHP_ID}", 
    }
    r = requests.get(url2, headers=custom_headers, proxies=proxies)
    
    return "Database has been created." in r.text
    
   
    
if __name__ == "__main__":
    main()

