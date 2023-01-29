import re
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from urllib.error import URLError

# Apertura del file txt contenente gli URL
with open('urls.txt', 'r') as f:
    urls = f.readlines()

# Inizializzazione del webdriver
driver = webdriver.Chrome()

# Apertura del file txt per scrivere le email trovate
with open('email_found.txt', 'w') as f:
    for url in urls:
        try:
            # Apertura dell'URL
                    # Apertura dell'URL
            driver.get("https://"+url)
        except URLError as e:
            f.write("Impossibile contattare l'URL: " + url + " Errore: " + str(e))
            continue
        except Exception as e:
            # gestione di qualsiasi altro errore
            f.write("Errore generico su: " + url + " : " + str(e))
            continue
            # Ricerca della email
            email = None
            start_time = time.time()
            while not email and time.time() - start_time < 5:
                email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', driver.page_source)
                time.sleep(1)
            # Scrittura della email trovata nel file txt
            if email:
                f.write(email[0] + '\n')
            else:
                f.write("nessuna email trovata su: " + url)
        except TimeoutException:
            # Passa al prossimo URL in caso di timeout
            f.write("timeout su: " + url)
            continue
        except WebDriverException as e:
            # Gestione degli errori del webdriver
            f.write("Errore WebDriver su: " + url + " : " + str(e))
            continue
        except Exception as e:
            # Gestione di qualsiasi altro errore
            f.write("Errore generico su: " + url + " : " + str(e))
            continue

# Chiudi il webdriver
driver.quit()
