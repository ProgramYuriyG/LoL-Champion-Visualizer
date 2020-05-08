# package imports
import lolChampionVisualizer.championInformationGui.championSearchGui as searchGui
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
from kivy.uix.screenmanager import Screen,ScreenManager,NoTransition
# widget imports
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem, TabbedPanelHeader


# class to make the starting screen when the app is loaded in
class StartScreenLayout(RelativeLayout):

    def drawOverallLayout(self):
        layout = RelativeLayout()
        title = Label(text="LoL Champion Visualizer", size_hint=(1, 0.2), font_size='32sp', pos_hint ={'middle':1, 'top':1})
        newDataButton = Button(text="Search For New Data", size_hint=(0.5, 0.8), font_size='32sp', pos_hint ={'left':1, 'middle':1})
        existingDataButton = Button(text="Use Existing Data", size_hint=(0.5, 0.8), font_size='32sp', pos_hint ={'right':1, 'middle':1})
        #on_press=self.changeToSearchGui()
        existingDataButton.bind(on_press = self.screen_transition)

        layout.add_widget(title)
        layout.add_widget(newDataButton)
        layout.add_widget(existingDataButton)
        return layout

    def screen_transition(self, *args):
        App.get_running_app().sm.current = 'championSearch'


class buildStartingScreenGui(Screen):

    def __init__(self, **kwargs):
        super(buildStartingScreenGui, self).__init__(**kwargs)
        self.add_widget(self.getLayout())

    def getLayout(self):
        startingLayout = StartScreenLayout().drawOverallLayout()
        return startingLayout