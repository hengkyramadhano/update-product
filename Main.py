import pandas as pd
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from variable import cat_slug
# from variableSKU import skuJakPus
from fromSKU import sku_item


service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
# driver = webdriver.Chrome('/Users/fdn-hengky/Learn/Add SKU/chromedriver')


def test_driver_manager_chrome():

    driver.get("https://www.jakartanotebook.com/auth/login")

    imel = driver.find_element(by=By.NAME, value="username")
    imel.send_keys("hengkyramadhano@gmail.com")
    pwd = driver.find_element(by=By.NAME, value="password")
    pwd.send_keys("Jakarta48@")

    submit_button = driver.find_element(by=By.XPATH, value="//*[@id='__next']/div/div[2]/div[1]/div/div[2]/div/form/div[3]/button")
    submit_button.click()

    # Button Mengerti
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='headlessui-popover-panel-:r1:']/div/div[2]/button"))).click()

    # -----------------------------------------------------------------------------------------------------------

    # ambil dari cat_slug
    pick_SKU = []

    for link in cat_slug:
        driver.get(f"https://www.jakartanotebook.com/{link}")
        driver.get(driver.current_url + "?show=100&sort=name&branch%5B0%5D=jz23mo")
        skuJakPus = search_sku(pick_SKU)
        
    # -----------------------------------------------------------------------------------------------------------

    # ambil dari ambilSKU
    # skuJakPus = sku_item

    # -----------------------------------------------------------------------------------------------------------
        

    with open("variableSKU.json", "w") as fp:
        json.dump(skuJakPus, fp)

    addSKU(skuJakPus)

    driver.quit()


def search_sku(pick_SKU) :
    
    total_sku = driver.find_elements(by=By.XPATH, value="//div[@class='product-list-wrapper']/div/div[1]")
    print(f"Total SKU per-page: {len(total_sku)}")

    # Ambil text dari hasil seluruh SKU yg ditemukan
    result_sku = driver.find_element(by=By.XPATH, value="//*[@id='form-list-item']/div/div[1]").text

    first_word = result_sku.split()[0]
    print(f"Seluruh SKU: {first_word}")

    # Penentuan jumlah halaman
    jumlah_halaman = (int(first_word) // 100)
    sisa_bagi = (int(first_word) % 100)

    print(f"Jumlah Halaman : {jumlah_halaman}\nSisa Bagi : {sisa_bagi}")

    if jumlah_halaman != 0 :
        # perulangan halaman
        for i in range(2,(jumlah_halaman+2)):
            # perulangan ambil SKU
            print("perulangan ambil SKU")
            for j in range(len(total_sku)):
                sku = driver.find_element(by=By.XPATH, value=f"//div[@class='product-list-wrapper']/div[{j+1}]/div[1]").get_attribute("textContent")
                # print(f"getSKU: {sku}")
                pick_SKU.append(sku)

            if (i == jumlah_halaman+1) :
                if (sisa_bagi >= 0):
                    driver.get(driver.current_url + f"?show=100&sort=name&branch%5B0%5D=jz23mo&page={i}")
                    print(f"Page ke - {i}")
                    for j in range(sisa_bagi):
                        sku = driver.find_element(by=By.XPATH, value=f"//div[@class='product-list-wrapper']/div[{j+1}]/div[1]").get_attribute("textContent")
                        # print(f"getSKU: {sku}")
                        pick_SKU.append(sku)
                print("Panggil Break!")
                break
            driver.get(driver.current_url + f"?show=100&sort=name&branch%5B0%5D=jz23mo&page={i}")
            print(f"Page ke - {i}")
    else :
        for j in range(len(total_sku)):
            sku = driver.find_element(by=By.XPATH, value=f"//div[@class='product-list-wrapper']/div[{j+1}]/div[1]").get_attribute("textContent")
            # print(f"getSKU: {sku}")
            pick_SKU.append(sku)
    
    print(f"Total SKU : {pick_SKU}")

    return pick_SKU

def addSKU(skuJakPus) :
    driver.get("https://www.jakmall.com/login")
    title = driver.title
    print(title + driver.current_url)

    # Button Cancel
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='onesignal-slidedown-cancel-button']"))).click()


    usrnme = driver.find_element(by=By.ID, value="email")
    usrnme.send_keys("hengkyramadhano@gmail.com")
    password = driver.find_element(by=By.ID, value="password")
    password.send_keys("Jakarta48@")
    submit_button = driver.find_element(by=By.XPATH, value="//*[@id='member']/div/form/fieldset/div[5]/div[2]/input")
    submit_button.click()

    for item in skuJakPus:
        driver.get(f"https://www.jakmall.com/search?q={item}")

        try :
            inventory = driver.find_element(by=By.XPATH, value="//div[@class='pi__inventory__exist']")
        except :
            print(f"New Master Product for {item}")
            inventory = driver.find_element(by=By.XPATH, value="//div[@class='flex--simple flex--center']")

        status = inventory.get_attribute("textContent")
        print(f"Status Label Inventory: {status}\nSKU: {item}")

        div_element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='product-list']/form/div[1]/div[2]/div[2]/div/div")))
        hover = ActionChains(driver).move_to_element(div_element)
        hover.perform()

        # getHarga
        getHarga = driver.find_element(by=By.XPATH, value="//*[@id='product-list']/form/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[1]").text
        harga = getHarga.replace("Rp ","").replace(".","")
        print(f"Harga : {harga}\n")

        if ((status == "Master Produk") & (int(harga) <= 300000)):
            # driver.find_element(by=By.XPATH, value="//button[@class='button button--cta button--full']").click()

            button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='button button--cta button--full']")))
            hover = ActionChains(driver).move_to_element(button)
            hover.perform()

            button.click()

test_driver_manager_chrome()