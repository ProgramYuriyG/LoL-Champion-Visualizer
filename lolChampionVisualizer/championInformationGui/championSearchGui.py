import lolChampionVisualizer.championInformationScraper.lolChampionScraper as championScraper
import lolChampionVisualizer.championInformationGui.championVisualizerGui as championGui
import kivy
import math
import os
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
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.tabbedpanel import TabbedPanelHeader



class ChampionSearchLayout(AnchorLayout):

    def __init__(self, sm=None, **kw):
        super().__init__(**kw)
        self.sm = sm

    def drawOverallLayout(self):
        layout = BoxLayout(orientation="vertical")
        label = Label(text="LoL Champion Visualizer", size_hint=(1, 0.1), font_size='40sp')
        scrollView = ScrollView(scroll_type=['bars'], bar_width=15, pos_hint ={'middle':1, 'middle':1}, do_scroll_x= False, do_scroll_y= True)
        scrollLayout = GridLayout(cols=1, spacing=10, size_hint=(0.5,None), pos_hint ={'center_x':.5})
        scrollLayout.bind(minimum_height=scrollLayout.setter('height'))

        championList = []
        if os.path.exists('Champions.txt'):
            championList = championScraper.getListOfChampions()
        
        for champName in championList:
            ''' This only puts the name of the last champion into the methods, fix this'''
            nameButton = Button(text=champName.capitalize(), font_size='22sp', size_hint=(0.5, None))
            # this method binds the button to the lambda method with early binding and then passes the button's text as the name
            nameButton.bind(on_press=lambda champName=champName:self.switchToChampionInformation(championName=champName.text))
            scrollLayout.add_widget(nameButton)

        scrollView.add_widget(scrollLayout)
        layout.add_widget(label)
        layout.add_widget(scrollView)
        return layout

    def switchToChampionInformation(self, championName):
        championDict = championScraper.getSpecificChampionInformation(championName.lower())
        self.sm.add_widget(championGui.buildChampionVisualizerGui(name="championInformation", statisticsContent=championDict, champion=championName, sm=self.sm))
        self.sm.current = 'championInformation'

        '''
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        #Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for i in range(30):
            btn = Label(text=str(i), size_hint_y=None, height=40)
            layout.add_widget(btn)
        root = ScrollView(size_hint=(None, None), size=(400, 400),pos_hint={'center_x':.5, 'center_y':.5})
        root.add_widget(layout)
        return root
        '''



class buildSearchGui(Screen):

    def __init__(self, sm=None, **kwargs):
        super(buildSearchGui, self).__init__(**kwargs)
        self.sm = sm
        self.add_widget(self.getLayout())

    def getLayout(self):
        searchLayout = ChampionSearchLayout(sm=self.sm).drawOverallLayout()
        return searchLayout
