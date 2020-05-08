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
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.tabbedpanel import TabbedPanelHeader



class ChampionSearchLayout(AnchorLayout):

    def drawOverallLayout(self):
        layout = AnchorLayout(anchor_x='center', anchor_y='top')
        label = Label(text="LoL Champion Visualizer", size_hint=(0.1, 0.1), font_size='32sp')
        layout.add_widget(label)
        return layout



class buildSearchGui(Screen):

    def __init__(self, **kwargs):
        super(buildSearchGui, self).__init__(**kwargs)
        self.add_widget(self.getLayout())

    def getLayout(self):
        searchLayout = ChampionSearchLayout().drawOverallLayout()
        return searchLayout
