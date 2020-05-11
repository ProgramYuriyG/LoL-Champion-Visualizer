from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import sys, traceback
import urllib.request
import traceback
import os

'''
Website that champion names and pictures will be parsed from:
https://na.leagueoflegends.com/en-us/champions/

Website that champion base statistics and abilities will be parsed from:
https://leagueoflegends.fandom.com/wiki/
'''

def getChromeDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    return driver


# method to get a list of all of the champions that are currently in the game by name
def scrapeForChampionNames(writeToFile=True):
    # initializes our web driver
    driver = getChromeDriver()
    driver.get("https://na.leagueoflegends.com/en-us/champions/")

    # gets the container that holds the list of all of the champion's icons
    championContainer = driver.find_elements_by_xpath ('/html/body/div/div[1]/div/div[2]/section/div[2]/section[2]/div[2]/*')
    championList = []
    # iterates through the list and gets the champion's names
    for champion in championContainer:
        #gets the champions name and appends it to the list
        championName = champion.find_element_by_xpath("span[2]/span").get_attribute('innerHTML')
        championName = championName.replace("&amp;", "&")
        championList.append(championName)
        #gets the champions d
        try:
            championImage = champion.find_element_by_xpath("span[1]/img")
            filePath = "images\\championImages\\" + championName + "\\"

            if not os.path.exists(os.path.dirname(filePath)):
                try:
                    os.makedirs(os.path.dirname(filePath))
                except OSError as exc: # Guard against race condition
                    pass
            if not(os.path.exists(filePath + championName.lower().replace(" ", "_") + "_splash_art.png") or os.path.exists(filePath + championName.lower().replace(" ", "_") + "_splash_art.jpg")):
                urllib.request.urlretrieve(championImage.get_attribute('src'), filePath + championName.lower().replace(" ", "_") + "_splash_art.png")
        except:
            traceback.print_exc()
            pass
    
    # puts the champions into a text file
    if writeToFile:
        championFile = open("Champions.txt", "w")
        for championName in championList:
            championName = championName.replace("-", " ")
            championFile.write(championName+"\n")
        championFile.close()
    driver.quit()
    return championList


# method used to get the statistics of each champion found in the Champions.txt file
def scrapeForChampionStatistics(championList):
    championStatistics = {}
    lastValidChampion = ""
    dataSortChampionValue = ""
    # initializes our web driver
    driver = getChromeDriver()

    for championName in championList:
        championName = championName.replace("\n", "")
        championStatistics[championName] = {}
        try:
            try:
                urlTitle = championName.replace(" ", "_")
                if championName == "Jarvan IV":
                    pass
                else:
                    urlTitle = urlTitle.title()
                driver.get("https://leagueoflegends.fandom.com/wiki/"+(urlTitle))
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "infobox-champion-container")))
            except:
                continue

            # there are two aside containers, one is the champion image which comes first and then followed by the statistics content
            asideContainer = driver.find_elements_by_tag_name('aside')[1]
            # gets all of the children of the container
            statisticsContainer = asideContainer.find_elements_by_xpath("*")

            try:
                imageRenderContainer = driver.find_elements_by_tag_name('aside')[0]
                championImage = imageRenderContainer.find_elements_by_tag_name('img')[0]
                filePath = "images\\championImages\\" + championName + "\\"

                if not os.path.exists(os.path.dirname(filePath)):
                    try:
                        os.makedirs(os.path.dirname(filePath))
                    except OSError as exc: # Guard against race condition
                        pass
                
                imageSaveName = "origininal_" + championImage.get_attribute('data-image-key').lower()
                if imageSaveName == 'nunu_render.png':
                    imageSaveName = 'nunu_&_willump_render.png'
                urllib.request.urlretrieve(championImage.get_attribute('src'), filePath + imageSaveName)
            except:
                traceback.print_exc()
                pass
            # get the aside from inside of the container
            #statisticsContainer = contentWrapper.find_element_by_xpath('div[1]/aside[1]')
            #('/html/body/div[3]/section/div[2]/article/div[1]/div[2]/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/aside/section[1]/section[1]/section/div[1]/div/a[2]')

            # go through all of the stats that are listed for the champion but bypass the first and last one since therye not necessary
            for stat in statisticsContainer[1:-1]:
                for container in stat.find_elements_by_xpath('*'):
                    if container.tag_name != "section":
                        continue
                    first_object = container.find_element_by_xpath('section/div[1]')
                    second_object = container.find_element_by_xpath('section/div[2]')
                    first_label = "N/A"
                    second_label = "N/A"
                    label_options = ['div/a[2]', 'div/a', 'div/span/a', 'div/span/a[2]']
                    # gets the first label of the statistic based on the label options
                    for option in label_options:
                        try:
                            if first_label == "N/A" or first_label == "":
                                first_label = first_object.find_element_by_xpath(option).text
                        except:
                            continue

                    # gets the second label of the statistic based on the label options
                    for option in label_options:
                        try:
                            if second_label == "N/A" or second_label == "":
                                second_label = second_object.find_element_by_xpath(option).text
                        except:
                            continue

                    # gets the values of the labels
                    first_value = container.find_elements_by_xpath('section/div[1]')[-1].text.replace(first_label, "")
                    second_value = container.find_elements_by_xpath('section/div[2]')[-1].text.replace(second_label, "")


                    first_label = first_label.replace("\n", "").replace(".", "")
                    first_value = first_value.replace("\n", "")
                    second_label = second_label.replace("\n", "").replace(".", "")
                    second_value = second_value.replace("\n", "")
                    championStatistics[championName][first_label] = first_value
                    championStatistics[championName][second_label] = second_value
                    lastValidChampion = championName
                    if dataSortChampionValue != "":
                        lastValidChampion = dataSortChampionValue
                        dataSortChampionValue = ""
        
        except:
            #traceback.print_exc()
            continue

    driver.quit()
    return championStatistics
        

# method to scrape for the champions 3d models and then download them to specific folders
# remove background with: https://photoscissors.com or https://www.remove.bg/upload
# get the 3d model from https://teemo.gg/model-viewer
def scrapeForChampionModels():
    pass


# method used to scrape https://leagueoflegends.fandom.com/wiki/List_of_champions for every champion's icons and save them
# higher res can be scraped from https://www.op.gg/champion/kled/statistics/top in a new version
def scrapeForChampionIcons():
    driver = getChromeDriver()
    driver.get('https://leagueoflegends.fandom.com/wiki/List_of_champions')
    championContainer = driver.find_elements_by_tag_name('tbody')[1].find_elements_by_xpath('*')

    for champion in championContainer:
        championName = champion.find_elements_by_tag_name('td')[0].get_attribute('data-sort-value')
        imageSaveName = championName.replace(" ", "_").lower() + "_icon.png"

        # src does not work past aurelion sol so use data-src
        imageSrc = champion.find_element_by_xpath('td[1]/span/span[1]/a/img').get_attribute('data-src')
        filePath = "images\\championImages\\" + championName + "\\"

        if championName == 'Nunu':
            filePath = "images\\championImages\\Nunu & Willump\\"
            imageSaveName = 'nunu_&_willump_icon.png'
        
        try:
            if not os.path.exists(os.path.dirname(filePath)):
                print("Icon Link Broken- ", championName, " ", imageSrc)
            else:
                print(championName, imageSrc)
                #os.remove(filePath + imageSaveName)
                urllib.request.urlretrieve(imageSrc, filePath + imageSaveName)
        except:
            continue


# method used to return a list of all current champions
def getListOfChampions():
    # opens the champions name list and gets all of our champion information
    championNameFile = open("Champions.txt", "r")
    championName = championNameFile.readline()
    championList = []
    while championName is not "":
        championName = championName.replace("\n", "")
        championList.append(championName)
        championName = championNameFile.readline()
    championNameFile.close()
    return championList


# method that converts the dictionary for each champion with stats into a json file
def writeChampionDictToJson(championDict):
    if os.path.exists('championStatistics.json'):
        with open('championStatistics.json', 'r') as fp:
            originalChampionDict = json.load(fp)
        
        combinedDict = {**originalChampionDict, **championDict}
    else:
        combinedDict = championDict
    
    with open('championStatistics.json', 'w') as fp:
        json.dump(combinedDict, fp, indent=4)


def getSpecificChampionInformation(championName):
    with open('championStatistics.json', 'r') as fp:
        championDict = json.load(fp)
    if championName in championDict:
        return championDict[championName]
    else:
        return None


def checkForUpdates():
    if os.path.exists('Champions.txt'):
        oldList = getListOfChampions()
        newList = scrapeForChampionNames(True)
        #newList = [name.replace('-', ' ') for name in newList]
        set_difference = set(newList) - set(oldList)
        list_difference = list(set_difference)
        if list_difference:            
            championDict = scrapeForChampionStatistics(list_difference)
            writeChampionDictToJson(championDict)
        return True
    else:
        getAllChampionInformation()

# method used to collect all of the champion information, aggregate of all methods
def getAllChampionInformation():
    scrapeForChampionNames()
    championList = getListOfChampions()
    championDict = scrapeForChampionStatistics(championList)
    writeChampionDictToJson(championDict)
