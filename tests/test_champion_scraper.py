import lolChampionVisualizer.championInformationScraper.lolChampionScraper as scraper

import json
import unittest
import os

# python -m unittest discover -s tests -v
#class TestScraping(unittest.TestCase):


class TestChampions(unittest.TestCase):

    # method used to test getting the champion Names from the official league website
    def test1_scraping_names(self):
        scraper.scrapeForChampionNames()
        self.assertTrue(os.path.exists('Champions.txt'))

    # method to test to see if the text 
    def test2_champions_text(self):
        champList = scraper.getListOfChampions()
        self.assertIsInstance(champList, list)
        self.assertTrue(bool(champList))
   
    # method to test whether scraping for test statistics returns the correct dict or not
    def test3_scraping_statistics(self):
        championList = scraper.getListOfChampions()
        returnedDict = scraper.scrapeForChampionStatistics(championList)
        scraper.writeChampionDictToJson(returnedDict)
        self.assertTrue(any(returnedDict.values()))
        self.assertTrue(os.path.exists('championStatistics.json'))

    # method to test the writing to json
    def test4_champions_json(self):
        with open('championStatistics.json') as f:
            data = json.load(f)
        self.assertTrue(all(data.values()))


if __name__ == '__main__':
    unittest.main()