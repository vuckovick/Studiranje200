from selenium import webdriver
from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


driver_path = 'C:/Users/Korisnik/Desktop/msedgedriver.exe'
service = Service(executable_path=driver_path)
driver = webdriver.Edge()

def testRegister():
    try:
        print("Test user register: ")
        driver.get('http://127.0.0.1:8000/register')

        driver.maximize_window()

        driver.find_element(By.NAME, 'fullname').send_keys('John Doe')

        d1 = driver.find_element(By.XPATH, '/html/body/main/div/div/div/div/form/div[1]/div[2]/input')
        d1.click()
        d2 = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[2]/div/span[16]')
        d2.click()

        time.sleep(1)

        driver.find_element(By.NAME, 'place').send_keys('Belgrade')

        gender_dropdown = driver.find_element(By.XPATH, '/html/body/main/div/div/div/div/form/div[1]/div[4]/div')
        gender_dropdown.click()

        time.sleep(1)

        g = driver.find_element(By.XPATH, '/html/body/main/div/div/div/div/form/div[1]/div[4]/div/div[2]/div/div[2]')
        g.click()

        time.sleep(1)

        driver.find_element(By.ID, 'nextStep').click()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'username')))

        driver.find_element(By.NAME, 'username').send_keys('john_doe')
        driver.find_element(By.NAME, 'email').send_keys('john@example.com')
        driver.find_element(By.NAME, 'password').send_keys('Password123!')
        driver.find_element(By.ID, 'confirm-psw-input').send_keys('Password123!')

        driver.find_element(By.ID, 'signIn').click()

        WebDriverWait(driver, 10).until(EC.url_to_be('http://127.0.0.1:8000/'))

        if driver.current_url == 'http://127.0.0.1:8000/':
            print("URL redirekcija je uspešna.")

            try:
                profile_dropdown = driver.find_element(By.ID, 'profileDropdown')
                if profile_dropdown:
                    print(
                        "Test uspešan: Korisnik je uspešno registrovan, preusmeren na početnu stranicu, i div sa ID-jem 'profileDropdown' postoji.")
            except NoSuchElementException:
                print("Test neuspešan: Div sa ID-jem 'profileDropdown' ne postoji.")
        else:
            print("Test neuspešan: Korisnik nije preusmeren na početnu stranicu.")

    except Exception as e:
        print(f"Test neuspešan: {e}")

    finally:
        driver.quit()


def testLogin():
    try:
        print("Test user login: ")
        driver = webdriver.Edge(service=service)

        driver.get('http://127.0.0.1:8000/login')

        driver.find_element(By.NAME, 'username').send_keys('john_doe')
        driver.find_element(By.NAME, 'password').send_keys('Password123!')

        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        WebDriverWait(driver, 10).until(EC.url_to_be('http://127.0.0.1:8000/'))
        if driver.current_url == 'http://127.0.0.1:8000/':
            print("URL redirekcija je uspešna.")

            try:
                profile_dropdown = driver.find_element(By.ID, 'profileDropdown')
                if profile_dropdown:
                    print(
                        "Test uspešan: Korisnik je uspešno prijavljen, preusmeren na početnu stranicu.")
            except NoSuchElementException:
                print("Test neuspešan.")
        else:
            print("Test neuspešan: Korisnik nije preusmeren na početnu stranicu.")

    except WebDriverException as e:
        print(f"Test neuspešan: {e}")

    finally:
        driver.quit()


def testProfileView():
    try:
        print("Test user profile view: ")
        driver = webdriver.Edge(service=service)

        driver.get('http://127.0.0.1:8000/login')

        driver.find_element(By.NAME, 'username').send_keys('john_doe')
        driver.find_element(By.NAME, 'password').send_keys('Password123!')

        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        WebDriverWait(driver, 10).until(EC.url_to_be('http://127.0.0.1:8000/'))

        dropdown_toggle = driver.find_element(By.ID, "profileDropdown")
        dropdown_toggle.click()

        time.sleep(1)

        dropdown_item = driver.find_element(By.XPATH,"//a[contains(text(), 'Moj profil')]")
        dropdown_item.click()

        user_name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'Vladimir Bogojevic')]")))
        print("Korisniku se prikazuje pregled njegovog profila.")

    except WebDriverException as e:
        print(f"Test neuspešan: {e}")

    finally:
        driver.quit()

def testChangeBio():
    try:
        print("Test change user bio: ")
        driver = webdriver.Edge(service=service)

        driver.get('http://127.0.0.1:8000/login')

        driver.find_element(By.NAME, 'username').send_keys('john_doe')
        driver.find_element(By.NAME, 'password').send_keys('Password123!')

        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        WebDriverWait(driver, 10).until(EC.url_to_be('http://127.0.0.1:8000/'))

        dropdown_toggle = driver.find_element(By.ID, "profileDropdown")
        dropdown_toggle.click()

        time.sleep(1)

        dropdown_item = driver.find_element(By.XPATH,"//a[contains(text(), 'Moj profil')]")
        dropdown_item.click()

        changeButton = driver.find_element(By.CLASS_NAME, "btn-danger-soft")
        changeButton.click()
        time.sleep(1)

        bioTextarea = driver.find_element(By.NAME, "bio")
        bioTextarea.clear()
        new_bio = "Nova biografija."
        bioTextarea.send_keys(new_bio)

        button2 = driver.find_element(By.XPATH, "//button[text()='Sačuvaj promene']")
        button2.click()

        time.sleep(1)

        old = driver.find_element(By.XPATH, "//div[@class='rounded border px-3 py-2 mb-3']//p")
        oldBio = old.text

        if(oldBio == "Nova biografija."):
            print("Uspesno promenjena biografija korisnika")

    except WebDriverException as e:
        print(f"Test neuspešan: {e}")

    finally:
        driver.quit()

def testBecomeOrganizer():
    try:
        print("Test become organizer: ")
        driver = webdriver.Edge(service=service)

        driver.get('http://127.0.0.1:8000/login')
        driver.maximize_window()

        driver.find_element(By.NAME, 'username').send_keys('john_doe')
        driver.find_element(By.NAME, 'password').send_keys('Password123!')

        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        WebDriverWait(driver, 10).until(EC.url_to_be('http://127.0.0.1:8000/'))

        dropdown_toggle = driver.find_element(By.ID, "profileDropdown")
        dropdown_toggle.click()

        time.sleep(1)

        dropdown_item = driver.find_element(By.XPATH,"//a[contains(text(), 'Moj profil')]")
        dropdown_item.click()

        WebDriverWait(driver, 10).until(EC.url_to_be('http://127.0.0.1:8000/my-profile/'))
        changeButton = driver.find_element(By.CLASS_NAME, "btn-danger-soft")
        changeButton.click()

        time.sleep(1)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(3)

        button2 = driver.find_element(By.XPATH, "//button[text()='Postani organizator']")
        button2.click()

        time.sleep(1)

        dropdown_toggle = driver.find_element(By.ID, "profileDropdown")
        dropdown_toggle.click()

        time.sleep(1)

        dropdown_item = driver.find_element(By.XPATH, "//a[contains(text(), 'Odjavi se')]")
        dropdown_item.click()

        time.sleep(1)

        dropdown_item = driver.find_element(By.XPATH, "//a[contains(text(), 'Prijavi se')]")
        dropdown_item.click()

        time.sleep(1)

        driver.find_element(By.NAME, 'username').send_keys('kole')
        driver.find_element(By.NAME, 'password').send_keys('123')

        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        WebDriverWait(driver, 10).until(EC.url_to_be('http://127.0.0.1:8000/'))

        nav = driver.find_element(By.ID, "notifDropdown")
        nav.click()

        time.sleep(1)

        nav = driver.find_element(By.XPATH, "/html/body/header/nav/div/ul/li[1]/div/div/div[3]/a")
        nav.click()

        time.sleep(1)

        accept = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div/div[2]/ul/li[1]/div/div[2]/div/button[1]")
        accept.click()

        time.sleep(1)

        dropdown_toggle = driver.find_element(By.ID, "profileDropdown")
        dropdown_toggle.click()

        time.sleep(1)

        dropdown_item = driver.find_element(By.XPATH, "//a[contains(text(), 'Odjavi se')]")
        dropdown_item.click()

        time.sleep(1)

        dropdown_item = driver.find_element(By.XPATH, "//a[contains(text(), 'Prijavi se')]")
        dropdown_item.click()

        time.sleep(1)

        driver.find_element(By.NAME, 'username').send_keys('john_doe')
        driver.find_element(By.NAME, 'password').send_keys('Password123!')

        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        WebDriverWait(driver, 10).until(EC.url_to_be('http://127.0.0.1:8000/'))

        dropdown_toggle = driver.find_element(By.ID, "profileDropdown")
        dropdown_toggle.click()

        time.sleep(1)

        dropdown_item = driver.find_element(By.XPATH, "//a[contains(text(), 'Moj profil')]")
        dropdown_item.click()

        WebDriverWait(driver, 10).until(EC.url_to_be('http://127.0.0.1:8000/my-profile/'))

        try:
            element = driver.find_element(By.CLASS_NAME, "bi-patch-check-fill")
            print('Test uspesan, korisnik postao organizator')
        except NoSuchElementException:
            print('Test neuspesan')

    except WebDriverException as e:
        print(f"Test neuspešan: {e}")

    finally:
        driver.quit()

def testConnection():
    try:
        print("Test new connection: ")
        driver = webdriver.Edge(service=service)

        driver.get('http://127.0.0.1:8000/login')

        driver.find_element(By.NAME, 'username').send_keys('stefan')
        driver.find_element(By.NAME, 'password').send_keys('123')

        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        WebDriverWait(driver, 10).until(EC.url_to_be('http://127.0.0.1:8000/'))
        driver.maximize_window()

        driver.get('http://127.0.0.1:8000/organizations')

        time.sleep(1)

        link = driver.find_element(By.XPATH, "/html/body/main/section[2]/div/div/div/div/div[2]/div/div/div/div[1]/div/div[2]/div[2]/h5/a")
        link.click()

        time.sleep(1)

        addButton = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div[1]/div[1]/a/i")
        addButton.click()

        time.sleep(1)

        dropdown_toggle = driver.find_element(By.ID, "profileDropdown")
        dropdown_toggle.click()

        time.sleep(1)

        dropdown_item = driver.find_element(By.XPATH, "//a[contains(text(), 'Odjavi se')]")
        dropdown_item.click()

        time.sleep(1)

        dropdown_item = driver.find_element(By.XPATH, "//a[contains(text(), 'Prijavi se')]")
        dropdown_item.click()

        time.sleep(1)

        driver.find_element(By.NAME, 'username').send_keys('vanja031')
        driver.find_element(By.NAME, 'password').send_keys('123')

        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        WebDriverWait(driver, 10).until(EC.url_to_be('http://127.0.0.1:8000/'))

        nav = driver.find_element(By.ID, "notifDropdown")
        nav.click()

        time.sleep(1)

        nav = driver.find_element(By.XPATH, "/html/body/header/nav/div/ul/li[1]/div/div/div[3]/a")
        nav.click()

        time.sleep(1)

        accept = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div/div[2]/ul/li[1]/div/div[2]/div/button[1]")
        accept.click()

        time.sleep(1)

        dropdown_toggle = driver.find_element(By.ID, "profileDropdown")
        dropdown_toggle.click()

        time.sleep(1)

        dropdown_item = driver.find_element(By.XPATH, "//a[contains(text(), 'Odjavi se')]")
        dropdown_item.click()

        time.sleep(1)

        dropdown_item = driver.find_element(By.XPATH, "//a[contains(text(), 'Prijavi se')]")
        dropdown_item.click()

        time.sleep(1)

        driver.find_element(By.NAME, 'username').send_keys('stefan')
        driver.find_element(By.NAME, 'password').send_keys('123')

        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        WebDriverWait(driver, 10).until(EC.url_to_be('http://127.0.0.1:8000/'))

        dropdown_toggle = driver.find_element(By.ID, "profileDropdown")
        dropdown_toggle.click()

        time.sleep(1)

        dropdown_item = driver.find_element(By.XPATH, "//a[contains(text(), 'Moj profil')]")
        dropdown_item.click()

        WebDriverWait(driver, 10).until(EC.url_to_be('http://127.0.0.1:8000/my-profile/'))

        conn = driver.find_element(By.XPATH, "/html/body/main/div[1]/div/div[2]/div/div[3]/div/div[1]/h5/span")
        if (conn.text=="1"):
            print("Test uspesan, napravljena konekcija")

    except WebDriverException as e:
        print(f"Test neuspešan: {e}")

    finally:
        driver.quit()


def testZainteresovan():
    try:
        print("Test become interested for an event: ")
        driver = webdriver.Edge(service=service)

        driver.get('http://127.0.0.1:8000/login')

        driver.find_element(By.NAME, 'username').send_keys('john_doe')
        driver.find_element(By.NAME, 'password').send_keys('Password123!')

        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        WebDriverWait(driver, 10).until(EC.url_to_be('http://127.0.0.1:8000/'))
        driver.maximize_window()

        driver.get('http://127.0.0.1:8000/events')

        time.sleep(1)

        link = driver.find_element(By.XPATH, "/html/body/main/section[2]/div/div/div/div/div[2]/div/div/div/div[1]/div/div[2]/div/h5/a")
        link.click()

        time.sleep(1)

        addButton = driver.find_element(By.XPATH, "/html/body/main/section/div/div/div[1]/div/div[2]/div[2]/label")
        addButton.click()

        time.sleep(1)

        dropdown_toggle = driver.find_element(By.ID, "profileDropdown")
        dropdown_toggle.click()

        time.sleep(1)

        dropdown_item = driver.find_element(By.XPATH, "//a[contains(text(), 'Moj profil')]")
        dropdown_item.click()

        time.sleep(1)

        try:
            nav = driver.find_element(By.XPATH, "/html/body/main/div[1]/div/div[1]/div[3]/div[2]/div[1]/strong")
            print("Uspesno uradjen test")
        except NoSuchElementException:
            print('Test neuspesan')


    except WebDriverException as e:
        print(f"Test neuspešan: {e}")

    finally:
        driver.quit()


def testKomentarOcena():
    #Potrebno je da u bazi pomerimo datum prethodnog eventa da bude neki datum pre danas, tj da je prosao, kako bi user mogao da komentarise
    try:
        print("Test comment and rate event: ")
        driver = webdriver.Edge(service=service)

        driver.get('http://127.0.0.1:8000/login')

        driver.find_element(By.NAME, 'username').send_keys('john_doe')
        driver.find_element(By.NAME, 'password').send_keys('Password123!')

        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        WebDriverWait(driver, 10).until(EC.url_to_be('http://127.0.0.1:8000/'))
        driver.maximize_window()

        dropdown_toggle = driver.find_element(By.ID, "profileDropdown")
        dropdown_toggle.click()

        time.sleep(1)

        dropdown_item = driver.find_element(By.XPATH, "//a[contains(text(), 'Moj profil')]")
        dropdown_item.click()

        time.sleep(1)

        nav = driver.find_element(By.XPATH, "/html/body/main/div[1]/div/div[1]/div[3]/div[2]/div[2]/div/div[2]/h5/a")
        nav.click()

        time.sleep(1)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(3)

        nav = driver.find_element(By.XPATH, "/html/body/main/section/div/div/div[3]/div[2]/div/div/form/input")
        nav.click()

        time.sleep(1)

        driver.find_element(By.NAME, 'comment').send_keys('Moj komentar')

        nav = driver.find_element(By.XPATH, "/html/body/main/div[1]/div/div/div[2]/div/form/div/div[1]/div/label[1]")
        nav.click()

        nav = driver.find_element(By.XPATH, "/html/body/main/div[1]/div/div/div[2]/div/form/div/div[2]/button")
        nav.click()

        time.sleep(1)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(3)

        try:
            comment = driver.find_element(By.XPATH, "/html/body/main/section/div/div/div[3]/div[2]/div/div[2]/p")
            print(comment.text)
            if comment.text=='Moj komentar':
                print("Test uspesan")
        except NoSuchElementException:
            print('Test neuspesan')

    except WebDriverException as e:
        print(f"Test neuspešan: {e}")

    finally:
        driver.quit()

testRegister()
#testLogin()
#testProfileView()
#testChangeBio()
#testBecomeOrganizer()
#testConnection()
#testZainteresovan()
#testKomentarOcena()