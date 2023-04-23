import pickle
from time import sleep
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

def loginIG(username,password):
    options = FirefoxOptions()
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36')

    if not username or not password:
        return(0)
    driver = webdriver.Firefox(options=options,service=FirefoxService(GeckoDriverManager().install()))
    website = (f'https://www.instagram.com/accounts/login/?next=%2Flogin%2F&source=desktop_nav')

    driver.get(website)
    driver.maximize_window()

    try:
        WebDriverWait(driver,8).until(EC.presence_of_element_located((By.NAME,'username')))
        sleep(2)
    except TimeoutException:
        print(f'{datetime.now().strftime("%d %b %y %H:%M:%S")} - Could not load Instagram; please check your Internet connection')
        driver.quit()
        return(0)

    try:
        driver.find_element(By.NAME,'username').send_keys(username)
        sleep(1)
        driver.find_element(By.NAME,'password').send_keys(password)
        sleep(1)
        driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[3]/button').click() #login btn
    except Exception as e:
        print(f'Did not manage to login - {e}')
        driver.quit()
        return(0)
    try:
        ## Wait until profile button is present before continuing
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[8]/div/div/a/div')))
    except TimeoutException:
        try:
            ## Wait until "more" button is present before continuing
            WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/section/div/button')))
        except TimeoutException:
            print(f'{datetime.now().strftime("%d %b %y %H:%M:%S")} - Failed to save cookies file; check login details.')
            driver.quit()
            return(0)

    ## Opens a file named 'cookies.pickle' and saves the cookies from the driver into the pickle file
    with open(f'{username}.pickle', 'wb') as file:
        pickle.dump(driver.get_cookies(),file)

    driver.quit()
    print(f'{datetime.now().strftime("%d %b %y %H:%M:%S")} - Cookies saved successfully.')
    return(1)

