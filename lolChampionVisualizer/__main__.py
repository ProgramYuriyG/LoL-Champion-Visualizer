import lolChampionVisualizer.championInformationScraper.lolChampionScraper as championScraper
import lolChampionVisualizer.championInformationGui.applicationGui as guiApp


if __name__ == '__main__':
    #championScraper.checkForUpdates()
    #championScraper.getSpecificChampionInformation("annie")
    #championScraper.getAllChampionInformation()
    guiApp.ChampionVisualizerApp().run()