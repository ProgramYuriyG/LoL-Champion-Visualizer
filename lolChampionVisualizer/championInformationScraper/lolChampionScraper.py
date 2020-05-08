from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import sys, traceback

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
def scrapeForChampionNames():
    # initializes our web driver
    driver = getChromeDriver()
    driver.get("https://na.leagueoflegends.com/en-us/champions/")

    # gets the container that holds the list of all of the champion's icons
    championContainer = driver.find_elements_by_xpath ('/html/body/div/div[1]/div/div[2]/section/div[2]/section[2]/div[2]/*')
    championList = []
    # iterates through the list and gets the champion's names
    for champion in championContainer:
        href = champion.get_attribute("href")
        championList.append(href.split("/")[-2])
    
    # puts the champions into a text file
    championFile = open("Champions.txt", "w")
    for championName in championList:
        championName = championName.replace("-", " ")
        championFile.write(championName+"\n")
    championFile.close()
    driver.quit()


# method used to get the statistics of each champion found in the Champions.txt file
def scrapeForChampionStatistics(championList):
    championStatistics = {}
    lastValidChampion = ""
    dataSortChampionValue = ""
    # initializes our web driver
    driver = getChromeDriver()

    #championList = ["ashe", "aurelion sol", "akali"]
    for championName in championList:
        championName = championName.replace("\n", "")
        championStatistics[championName] = {}
        try:
            try:
                driver.get("https://leagueoflegends.fandom.com/wiki/"+championName.replace(" ", "_"))
                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.ID, "infobox-champion-container")))
            except TimeoutException:
                try:
                    driver.get("https://leagueoflegends.fandom.com/wiki/List_of_champions")
                    championElements = driver.find_elements_by_xpath("/html/body/div[3]/section/div[2]/article/div[1]/div[1]/div[2]/table[2]/tbody/*")
                    foundChampion = False
                    for element in championElements:
                        # if we have found the champion then get its name from the attribute and go to the site
                        if foundChampion:
                            hrefLink = element.find_element_by_xpath('td[1]/span/span[2]/a').get_attribute("href")
                            dataSortChampionValue = element.find_elements_by_xpath("*")[0].get_attribute("data-sort-value").lower()
                            driver.get(hrefLink)
                            break
                        # if the champion who is above the searched for champion is found then go to the next champion
                        sortValue = element.find_elements_by_xpath("*")[0].get_attribute("data-sort-value")
                        if sortValue is not None and sortValue.lower() == lastValidChampion:
                            foundChampion = True
                            continue

                    WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.ID, "infobox-champion-container")))
                except TimeoutException:
                    continue

            # there are two aside containers, one is the champion image which comes first and then followed by the statistics content
            asideContainer = driver.find_elements_by_tag_name('aside')[1]
            # gets all of the children of the container
            statisticsContainer = asideContainer.find_elements_by_xpath("*")

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


                    first_label = first_label.replace("\n", "")
                    first_value = first_value.replace("\n", "")
                    second_label = second_label.replace("\n", "")
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


# method used to return a list of all current champions
def getListOfChampions():
    # opens the champions name list and gets all of our champion information
    championNameFile = open("Champions.txt", "r")
    championName = championNameFile.readline()
    championList = []
    while championName is not "":
        championList.append(championName)
        championName = championNameFile.readline()
    championNameFile.close()
    return championList


# method that converts the dictionary for each champion with stats into a json file
def writeChampionDictToJson(championDict):
    with open('championStatistics.json', 'w') as fp:
        json.dump(championDict, fp, indent=4)


# method used to collect all of the champion information, aggregate of all methods
def getAllChampionInformation():
    scrapeForChampionNames()
    championList = getListOfChampions()
    championDict = scrapeForChampionStatistics(championList)
    writeChampionDictToJson(championDict)