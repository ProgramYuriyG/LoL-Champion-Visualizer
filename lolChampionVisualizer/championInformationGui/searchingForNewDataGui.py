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



class NewChampionSearchLayout(AnchorLayout):

    def __init__(self, sm=None, **kw):
        super().__init__(**kw)
        self.sm = sm 

    def drawOverallLayout(self):
        layout = GridLayout(rows=3, size_hint=(1, 0.8), pos_hint={'middle':1, 'top':1})
        label = Label(text="LoL Champion Visualizer", size_hint=(1.0, 1.0), font_size='40sp')
        searchingLabel = Label(text="Searching For New Data", size_hint=(1.0, 1.0), font_size='28sp')
        loadingGif = Image(source='images\\icons\\loading_icon.gif', size_hint=(1.0, 1.0), keep_ratio=True)
        layout.add_widget(label)
        layout.add_widget(searchingLabel)
        layout.add_widget(loadingGif)
        return layout


class buildDataSearchGui(Screen):    

    def __init__(self, sm=None, **kwargs):
        super(buildDataSearchGui, self).__init__(**kwargs)
        self.sm = sm
        self.add_widget(self.getLayout())

    def getLayout(self):
        searchLayout = NewChampionSearchLayout(sm=self.sm).drawOverallLayout()
        return searchLayout
