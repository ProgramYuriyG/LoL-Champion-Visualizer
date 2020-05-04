from selenium import webdriver
import json

'''
Website that champion names and pictures will be parsed from:
https://na.leagueoflegends.com/en-us/champions/

Website that champion base statistics and abilities will be parsed from:
https://leagueoflegends.fandom.com/wiki/
'''

# method to get a list of all of the champions that are currently in the game by name
def getAllChampions():
    # initializes our web driver
    driver = webdriver.Chrome()
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
def getChampionStatistics(championList):
    championStatistics = {}
    print(championList)
    # initializes our web driver
    driver = webdriver.Chrome()
    for championName in championList:
        championName = championName.replace("\n", "")
        driver.get("https://leagueoflegends.fandom.com/wiki/"+championName.replace(" ", "_"))
        statisticsContainer = driver.find_elements_by_xpath("/html/body/div[3]/section/div[2]/article/div[1]/div[2]/div[2]/div[4]/div[2]/div[1]/aside[1]/*")
        
        # if this is the incorrect container then get the other one
        if len(statisticsContainer) <= 0 or statisticsContainer[0].tag_name != "h2" or statisticsContainer[0].find_element_by_xpath('a').text != "Base statistics":
            statisticsContainer = driver.find_elements_by_xpath("/html/body/div[3]/section/div[2]/article/div[1]/div[1]/div[2]/div[3]/div[2]/div[1]/aside[1]/*")
        championStatistics[championName] = {}
        print(championName)
        for stat in statisticsContainer[1:-1]:
            for container in stat.find_elements_by_xpath('*'):
                if container.tag_name != "section":
                    continue
                first_object = container.find_element_by_xpath('section/div[1]')
                second_object = container.find_element_by_xpath('section/div[2]')
                first_label = "N/A"
                first_value = "N/A"
                second_label = "N/A"
                second_value = "N/A"
                label_options = ['div/a[2]', 'div/a', 'div/span/a', 'div/span/a[2]']
                
                for option in label_options:
                    try:
                        if first_label == "N/A" or first_label == "":
                            first_label = first_object.find_element_by_xpath(option).text
                    except:
                        continue
                
                for option in label_options:
                    try:
                        if second_label == "N/A" or second_label == "":
                            second_label = second_object.find_element_by_xpath(option).text
                    except:
                        continue
                
                first_value =  (container.find_elements_by_xpath('section/div[1]')[-1].text).replace(first_label, "")
                second_value =  container.find_elements_by_xpath('section/div[2]')[-1].text.replace(second_label, "")


                first_label = first_label.replace("\n", "")
                first_value = first_value.replace("\n", "")
                second_label = second_label.replace("\n", "")
                second_value = second_value.replace("\n", "")
                championStatistics[championName][first_label] = first_value
                championStatistics[championName][second_label] = second_value

                if championName.lower() == "caitlyn":
                    driver.quit()
                    return championStatistics

    driver.quit()
    return championStatistics
        

# method used to return a list of all current champions
def getChampionList():
    # opens the champions name list and gets all of our champion information
    championNameFile = open("Champions.txt", "r")
    championName = championNameFile.readline()
    championList = []
    while championName is not "":
        championList.append(championName)
        championName = championNameFile.readline()
    return championList


# method that converts the dictionary for each champion with stats into a json file
def writeChampionsToJSON(championDict):
    with open('championStatistics.json', 'w') as fp:
        json.dump(championDict, fp, indent=4)


# method used to collect all of the champion information, aggregate of all methods
def getAllChampionInformation():
    #getAllChampions()
    championList = getChampionList()
    championDict = getChampionStatistics(championList)
    writeChampionsToJSON(championDict)