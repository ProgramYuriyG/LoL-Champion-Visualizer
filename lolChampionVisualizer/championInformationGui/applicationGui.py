# package imports
import lolChampionVisualizer.championInformationGui.championVisualizerGui as championGui
import lolChampionVisualizer.championInformationGui.championSearchGui as searchGui
import lolChampionVisualizer.championInformationGui.startingApplicationGui as startingGui
import lolChampionVisualizer.championInformationGui.searchingForNewDataGui as newDataGui
#disables multitouch with right click
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
# regular imports
import kivy
import math
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
from kivy.uix.screenmanager import Screen,ScreenManager,NoTransition, FadeTransition
# widget imports
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem, TabbedPanelHeader


class ChampionVisualizerApp(App):

    def window_settings(self):
        Window.maximize()

    def __init__(self,**kwargs):
        super(ChampionVisualizerApp,self).__init__(**kwargs)
        self.sm = ScreenManager(transition=FadeTransition())

        self.sm.add_widget(startingGui.buildStartingScreenGui(name="startingScreen", sm=self.sm))
        self.sm.add_widget(newDataGui.buildDataSearchGui(name="newDataSearch", sm=self.sm))

        self.sm.current = "startingScreen"

    def build(self):
        self.window_settings()
        return self.sm