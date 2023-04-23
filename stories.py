from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


import os
from random import randint, shuffle
from time import sleep
from datetime import datetime, timedelta, timezone
import pickle
import requests
import json

py_filepath = os.getcwd()
archive_filepath = py_filepath+'\\archive\\'

list_of_stories = []
jsonData = []
cwd = os.getcwd()

start_time = ""
end_time = ""

def skipStory(driver):
    ## continue to the next story by finding the right arrow
    print('Skipping story . . .')
    if driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/button').get_attribute('aria-label') == 'Next':
        driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/button').click()
    else:
        driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/button[2]').click()

def pauseStory(driver):
        ## pause the stories from loading
    try:
        ## check if the aria-label of the button is Pause or Play
        ## if it is Play, means it is currently paused; hence do nothing
        ## else if it is Pause, it will throw TimeoutException
        WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/header/div[2]/div[2]/button[1]/div/*[name()="svg"][@aria-label="Play"]')))
    except TimeoutException as e:
        ## click on the button to pause the video
        driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/header/div[2]/div[2]/button[1]/div").click()

def locationToLonLat(address):

    user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    api = f'https://nominatim.openstreetmap.org/search.php?q={address.replace(" ", "+")}&format=jsonv2&limit=1'

    try:
        r = requests.get(api,headers=user_agent)
        data = json.loads(r.text)

        return [float(data[0]["lon"]),float(data[0]["lat"])]
    except Exception as e:
        return [None,None]

def readJsonData(fn):
    with open(fn,'r') as f:
        return json.load(f)

def saveJsonData(fn, data, new_data):
    t = {}
    for obj in new_data:

        dt = datetime.strptime(obj['time'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%d-%m-%Y")
        if dt in t:
            t[dt].append(obj)
        else:
            t[dt] = [obj]

    for dt in t:
        ## {"dt":[obj,obj], "dt2":[obj2,obj3]}
        if dt not in data[1]:
            ## if there is no data, add it
            data[1][dt] = t[dt]
        else:
            ## if there is data, append it
            data[1][dt] += t[dt]

    with open(fn,'w',encoding='utf-8') as f:
        json.dump(data,f,indent=4)

def convert_to_unix_time(date_string):
    dt = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    return int(dt.timestamp())

def downloadStories(list_of_stories):
    cwd = os.getcwd()
    temp = []

    for obj in list_of_stories:
        user = obj['username']

        static_filepath = f'{cwd}\\static'

        ## check if the folder to store data exists
        ## if not, create the "static" folder
        ## saving the file based on the user and date of story posted
        if not os.path.exists(static_filepath):
            os.makedirs(static_filepath)

        try:
            print(f"Downloading from {obj['download_url']}")
            r = requests.get(obj['download_url'])
            if r.status_code == 200:

                filename = f"{user}_{convert_to_unix_time(obj['time'])}"

                if obj['type'] == 'image':
                    filename+='.jpg'
                else:
                    filename+='.mp4'

                full_filepath = f'{static_filepath}\\{filename}'
                with open(full_filepath,'wb') as f:
                    f.write(r.content)
                    print(f'Downloaded story to {full_filepath}')

                obj['filename'] = filename
            else:
                print(f'Failed to download file')
                obj['filename'] = 'error'

        except Exception as e:
            print(e)
            obj['filename'] = 'error'

        temp.append(obj)

    return temp


## function to find location tag
def find_dialog_element(elements):
    for element in elements:
        if element.get_attribute("role") == "dialog":
            return element
        else:
            children = element.find_elements(By.CSS_SELECTOR,"*")
            if children:
                dialog_element = find_dialog_element(children)
                if dialog_element:
                    return dialog_element
    return None


## get list of network requests made by a driver then clear the existing requests
## looks through the list of network requests to find the request
## to the video resource indicated by "&bytestart=0" in the request
def getDownloadURLFromRequests(driver):
    network_logs = driver.execute_script("""
        var performance = window.performance || window.webkitPerformance || window.mozPerformance || window.msPerformance || {};
        var network = performance.getEntriesByType("resource");
        return network;
    """)
    driver.execute_script("window.performance.clearResourceTimings();")

    for log in network_logs:
        url = log['name']
        if '&bytestart=0' in url:
            return url.split('&bytestart=0')[0]


def scrapeStories(user_list, driver):

    global start_time
    global list_of_stories
    global end_time

    start_time = datetime.now()

    print(f'{datetime.now().strftime("%d %b %y %H:%M:%S")} - Program start at ' + start_time.strftime('%d %b %y %H:%M:%Shrs'))
    print(f'{datetime.now().strftime("%d %b %y %H:%M:%S")} - Scraping for stories since ' + end_time.strftime('%d %b %y %H:%M:%Shrs'))

    ## get list of urls to stories page of profiles
    list_of_profiles = [f"https://www.instagram.com/stories/{user}" for user in user_list]

    ## shuffle list of profiles to randomize scraping order
    ## shuffle(list_of_profiles)

    list_of_stories = []

    ## stories checker
    for url in list_of_profiles:

        location_count = 0
        story_count = 0

        ## opens the page of the instagram profile to be scraped
        ## to handle in try/except
        driver.get(url)

        try:
            view_story_xpath = "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[1]/div/div/div/div[3]/div"
            WebDriverWait(driver,8).until(EC.presence_of_element_located((By.XPATH, view_story_xpath)))
            driver.find_element(By.XPATH, view_story_xpath).click()
        except TimeoutException:
            try:
                view_story_xpath2 = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[1]/div/div/div/div[3]/div"
                WebDriverWait(driver,8).until(EC.presence_of_element_located((By.XPATH, view_story_xpath)))
                driver.find_element(By.XPATH, view_story_xpath2).click()
            except Exception as e:
                print(e)
                return
        try:
            print(f'Found stories from {url[34:]}')

            while "stories" in driver.current_url:

                ## pause the story to prevent it from loading
                pauseStory(driver)

                ## get timestamp of current story to check if it is still within scrape time
                timestamp_xpath = '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/header/div[2]/div[1]/div/div/div/div/time'
                story_timestamp = driver.find_element(By.XPATH, timestamp_xpath).get_attribute("datetime") #2023-04-21T12:46:12.000Z
                story_timestamp_obj = datetime.strptime(story_timestamp,"%Y-%m-%dT%H:%M:%S.%fZ")
                story_timestamp_gmt = story_timestamp_obj + timedelta(minutes=480)

                if story_timestamp_gmt >= end_time:
                    ## means that story was posted after the last scrape
                    ## hence we should process the story
                    print(f'Processing story - {story_timestamp}')
                    story_count += 1

                else:
                    skipStory(driver)
                    continue

                obj = {"username":url[34:]}
                obj["time"] = story_timestamp
                ## initialize location, lon and lat as empty first
                obj["location_name"] = ""
                obj["lon"] = None
                obj["lat"] = None
                obj["ig_location_url"] = ""

                ## check if story is an image or video
                try:
                    img_src_element = '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[1]/div/div/img'
                    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, img_src_element)))
                    download_url = driver.find_element(By.XPATH,img_src_element).get_attribute("src")
                    print(f'IMAGE - {download_url}')
                    obj["type"] = "image"
                    obj["download_url"] = download_url
                except TimeoutException:
                    download_url = getDownloadURLFromRequests(driver)
                    print(f'VIDEO - {download_url}')
                    obj["type"] = "video"
                    obj["download_url"] = download_url

                ## if there is a location tag in the story, location_tag will be the xpath of the tag
                location_tag = False

                xpaths = [
                            '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[1]/div/div/div/div/div[2]/div/div',
                            '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div[1]/div'
                         ]

                ## depending on the story (video vs static image)
                ## the xpath of the location tag will be different
                ## hence do some checks to find the correct xpath
                ## instead of XPATH, consider searching for aria-label="Cancel Pop-up" and looking for the first child element which is the location tag

                for xpath in xpaths:
                    ## once the correct location tag is found, break out of the loop
                    try:
                        WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, xpath)))
                        location_tag = xpath
                        location_count+=1
                        break
                    except TimeoutException:
                        pass

                ## if location tag is false, skip the story
                if not location_tag:
                    skipStory(driver)
                    list_of_stories.append(obj) ## no location_name, lon,lat,igloc
                    continue

                ## click on the location tag
                location_tag_elem = driver.find_element(By.XPATH, location_tag)
                driver.execute_script("arguments[0].click();", location_tag_elem)
                sleep(randint(1,2))

                ## find the "See Location" tag and click on it
                xp = '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]'
                element_list = driver.find_elements(By.XPATH,xp)

                if not element_list:
                    xp2 = '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[1]/div/div/div/div/div[2]'
                    element_list = driver.find_elements(By.XPATH,xp2)

                dialog_elem = find_dialog_element(element_list)
                dialog_elem.click()

                try:
                    location_name_tag = '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/article/header/div[2]/div/div/span'
                    WebDriverWait(driver,15).until(EC.presence_of_element_located((By.XPATH, location_name_tag)))
                    ig_location_url = driver.current_url
                    location_name = driver.find_element(By.XPATH,location_name_tag).text
                    lon_and_lat = locationToLonLat(location_name)

                    obj["location_name"] = location_name
                    obj["lon"] = lon_and_lat[0]
                    obj["lat"] = lon_and_lat[1]
                    obj["ig_location_url"] = ig_location_url

                    driver.back()
                    sleep(2)

                except TimeoutException as TE:
                    print(TE)

                list_of_stories.append(obj)

                skipStory(driver)

            print(f'Finished scraping {url[34:]} . . . Moving on to next profile . . .')
            print(f'Number of stories found: {story_count}')
            print(f'Number of stories with location tag found: {location_count}')

        except TimeoutException as TE:
            try:
                ## check if the "Sorry, this page isn't available." div exists which means the profile is invalid
                sorry_xpath = '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/span'
                driver.find_element(By.XPATH, sorry_xpath)
                print(f'The profile {url[34:]} does not exist')

            except NoSuchElementException as NSE:
                print(f'No stories from {url[34:]}')

        continue

    print('Finished scraping all profiles . . .')

    try:
        test = driver.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")
        with open('requests.txt','w',encoding='utf-8') as f:
            json.dump(test, f, indent=4)
    except:
        pass

    driver.quit()


def startBrowser():
    options = FirefoxOptions()
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36')
    driver = webdriver.Firefox(options=options,service=FirefoxService(GeckoDriverManager().install()))
    driver.maximize_window()
    return driver


def loginInstagram(filename, driver): ## need to handle exceptions ie. return or quit
    try:
        driver.get('https://www.instagram.com/')

        ## takes in filename of cookie file and driver
        cookies = pickle.load(open(filename, "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.refresh()

        WebDriverWait(driver,8).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[8]/div/div/a/div')))
    except FileNotFoundError as fnfe:
        print(f'Unable to find pickles file - {fnfe}')
    except TimeoutException as e:
        print(f'Failed to login - {e}')


def getListOfUsers(filename):
    ## reads list of instagram profiles to scrape from
    try:
        with open(filename) as users_file:
            ## returns a List containing IG profile URLs and strips of \n at the back
            return [line.strip() for line in users_file]
    except FileNotFoundError as FNFE:
        print(f'{datetime.now().strftime("%d %b %y %H:%M:%S")} - "igprofiles.txt" not found - {FNFE}')
        return

def startScraping():
    global start_time
    global end_time

    counter = 0
    end_time = ""

    while True:
        start_time = datetime.now()
        jsonData = readJsonData('data.json')

        frequency = jsonData[0]['parameters']['frequency']
        users_file = jsonData[0]['parameters']['users_file']
        pickle_file = jsonData[0]['parameters']['pickle_file']
        ## First iteration of scraping
        if counter == 0:
            end_time = start_time - timedelta(minutes=frequency)

        driver = startBrowser()
        list_of_users = getListOfUsers(users_file)
        loginInstagram(filename=pickle_file, driver=driver)
        scrapeStories(user_list=list_of_users, driver=driver)

        temp = downloadStories(list_of_stories=list_of_stories) #download the files and return new list of objects

        saveJsonData('data.json',jsonData, temp)

        end_time = datetime.now()
        print(f'{datetime.now().strftime("%d %b %y %H:%M:%S")} - Program end at ' + end_time.strftime('%d %b %y %H:%M:%Shrs'))

        sleepTime = round(((start_time + timedelta(minutes=frequency)) - end_time).total_seconds())

        print(f'{datetime.now().strftime("%d %b %y %H:%M:%S")} - Sleeping until ' + (end_time + timedelta(seconds=sleepTime)).strftime(('%d %b %y %H:%M:%Shrs')))
        print(f'{datetime.now().strftime("%d %b %y %H:%M:%S")} - Sleeping...\n')

        sleep(sleepTime)
        counter += 1



