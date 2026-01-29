import wocabee
import datetime
import traceback
import threading
from time import sleep
from selenium.webdriver.common.by import By
import getpass

# Sem zadaj používateľov ako tuples: ("username", "password")
# Príklad: users = [("meno", "heslo"), ("meno2", "heslo2")]
users = []

# Počet lekcií ktoré sa majú urobiť naraz v jednom balíku
POCET_LEKCII = 3

def vsetky_baliky(woca):
    while woca.get_packages(woca.DOPACKAGE):
        woca.pick_package(0,woca.get_packages(woca.DOPACKAGE))
        
        # Urob POCET_LEKCII lekcií naraz
        for lekcia in range(POCET_LEKCII):
            print(f"[*] Robím lekciu {lekcia + 1}/{POCET_LEKCII}")
            while True:
                try:
                    woca.do_package()
                except Exception as e:
                    print(traceback.format_exception(e))
                else:
                    break
            sleep(2)
            
            # Po každej lekcii klikni na Continue ak existuje
            if woca.exists_element(woca.driver, By.ID, "continueBtn"):
                woca.get_element(By.ID, "continueBtn").click()
                sleep(1)
            
            # Skontroluj či ešte môžeme pokračovať v ďalšej lekcii
            try:
                woca.wait_for_element(3, By.ID, "backBtn")
                back_text = woca.get_element_text(By.ID, "backBtn")
                if back_text == "Uložiť a odísť":
                    # Balík dokončený, ukončíme loop
                    print(f"[*] Balík dokončený po {lekcia + 1} lekciách")
                    woca.get_element(By.ID, "backBtn").click()
                    break
            except:
                # Ak nie je backBtn, skúsime pokračovať
                pass
        
        sleep(2)
        # Finálna kontrola po všetkých lekciách
        if woca.exists_element(woca.driver, By.ID, "continueBtn"):
            woca.get_element(By.ID, "continueBtn").click()
        try:
            woca.wait_for_element(5, By.ID, "backBtn")
            if woca.get_element_text(By.ID, "backBtn") == "Uložiť a odísť":
                woca.get_element(By.ID, "backBtn").click()
        except:
            pass

def do_wocabee(user):
    woca = wocabee.wocabee(user)
    woca.init()
    print(woca.name)
    for x in range(len(woca.get_classes())):
        woca.pick_class(x,woca.get_classes())
        vsetky_baliky(woca)
        woca.leave_class()
    woca.quit()

#while True:
    #if datetime.datetime.now().weekday() == 0 or 6: # if today is monday or sunday
if not users:
    username = input("username:")
    password = getpass.getpass("password:")
    users.append((username,password))
for x in users:
    print(x[0]) # display username
    thread = threading.Thread(target=do_wocabee,args=(x,))
    thread.start()
thread.join()
