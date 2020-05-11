# overall imports
import lolChampionVisualizer.championInformationScraper.lolChampionScraper as championScraper
import lolChampionVisualizer.championInformationGui.championVisualizerGui as championGui
import kivy
import math
import os
from functools import partial ##import partial, wich allows to apply arguments to functions returning a funtion with that arguments by default.
# higher order imports
from kivy.app import App
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.metrics import dp
from kivy.clock import Clock
# layout imports
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen,ScreenManager,NoTransition
# widget imports
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem, TabbedPanelHeader
from kivy.uix.textinput import TextInput


# class to handle the search champions functionality
class ChampionSearchLayout(AnchorLayout):

    # initializer
    def __init__(self, sm=None, **kw):
        super().__init__(**kw)
        self.sm = sm

    # method to draw the whole layout
    def drawOverallLayout(self):
        # creates the layouts
        layout = BoxLayout(orientation="vertical")
        scrollLayout = GridLayout(cols=2, spacing=10, size_hint=(0.6, None))
        scrollView = ScrollView(scroll_type=['bars'], size_hint_x=0.71, bar_width=20, pos_hint ={'right':1}, do_scroll_x= False, do_scroll_y= True)
        scrollLayout.bind(minimum_height=scrollLayout.setter('height'))

        # title of the screen
        label = Label(text="LoL Champion Visualizer", size_hint=(1, 0.1), font_size='40sp')

        # creates the champion list and populates the scroll view with it
        championList = []
        if os.path.exists('Champions.txt'):
            championList = championScraper.getListOfChampions()
        self.totalChampionList = championList

        # creates the search bar
        searchBarLayout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 0.15))
        searchTextinput = TextInput(hint_text='Search For Champions', font_size='20sp', size_hint=(0.5, 0.6), background_color= [1, 1, 1, 0.5], hint_text_color=[1, 1, 1, 0.7], multiline=False, halign='center', padding_y=10)
        searchTextinput.bind(text=partial(self.on_text, scrollLayout=scrollLayout))
        
        # adds all the widgets to the layouts
        searchBarLayout.add_widget(searchTextinput)
        scrollView.add_widget(scrollLayout)

        layout.add_widget(label)
        layout.add_widget(searchBarLayout)
        layout.add_widget(scrollView)
        return layout
    
    # method used for the search Input when new text is added to it
    def on_text(self, instance, value, scrollLayout):
        champList = self.totalChampionList
        if bool(value):
            champList = [name for name in champList if value.lower() in name.lower()]

        scrollLayout.clear_widgets()
        self.addChampionsToScrollView(champList, scrollLayout)

    # method used to add champions to a scrollview
    def addChampionsToScrollView(self, championList, scrollLayout):
        for champName in championList:
            
            iconLayout = RelativeLayout(size_hint_x=0.1)
            champIcon = Image(size_hint_y=0.8, pos_hint ={'center_y':0.5}, allow_stretch=True, source="images\\championImages\\" + champName + "\\"+ champName.lower().replace(" ", "_") +"_icon.png")
            nameButton = Button(text=champName, font_size='22sp', height= 50, size_hint_x=0.9, size_hint_y=None)
            # this method binds the button to the lambda method with early binding and then passes the button's text as the name
            nameButton.bind(on_press=lambda champName=champName:self.switchToChampionInformation(championName=champName.text))
            iconLayout.add_widget(champIcon)
            scrollLayout.add_widget(iconLayout)
            scrollLayout.add_widget(nameButton)

    # method used to switch to the specific champion's information
    def switchToChampionInformation(self, championName):
        championDict = championScraper.getSpecificChampionInformation(championName)
        self.sm.add_widget(championGui.buildChampionVisualizerGui(name="championInformation", statisticsContent=championDict, champion=championName, sm=self.sm))
        self.sm.current = 'championInformation'


# method to create a screen that can be switched around based on the search class
class buildSearchGui(Screen):

    # initializer
    def __init__(self, sm=None, **kwargs):
        super(buildSearchGui, self).__init__(**kwargs)
        self.sm = sm
        self.add_widget(self.getLayout())

    # gets the search class's layout
    def getLayout(self):
        searchLayout = ChampionSearchLayout(sm=self.sm).drawOverallLayout()
        return searchLayout
