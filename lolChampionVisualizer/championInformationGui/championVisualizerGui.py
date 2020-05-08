from kivy.app import App
from kivy.core.window import Window
# layout imports
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
# widget imports
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.tabbedpanel import TabbedPanelHeader

'''
python -m pip install --upgrade pip wheel setuptools virtualenv
python -m virtualenv kivy_venv
kivy_venv\Scripts\activate
python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2==0.1.* kivy_deps.glew==0.1.*
python -m pip install kivy_deps.gstreamer==0.1.*
python -m pip install kivy==1.11.1
pip install selenium
'''


class ChampionSkinContainer(RelativeLayout):

    def drawSkinContainer(self):
        visual_image = 'championImages\\higher-res-teemo.png'
        skinName = visual_image.split("\\")[-1].split(".")[0].replace("_", " ")

        skin_layout = RelativeLayout(size_hint=(0.45, 1), pos_hint ={'left':1, 'top':1})
        skin_utility_layout = GridLayout(cols=3, size_hint=(1, 0.2), pos_hint ={'left':1, 'bottom':1})

        skin_visual = Image(source=visual_image, size_hint=(1, 0.8), pos_hint ={'left':1, 'top':1})
        left_button = Button(text='<', size_hint=(0.1, 1))
        skin_text = Label(text=skinName, size_hint=(0.8, 1))
        right_button = Button(text='>', size_hint=(0.1, 1))

        skin_utility_layout.add_widget(left_button)
        skin_utility_layout.add_widget(skin_text)
        skin_utility_layout.add_widget(right_button)

        skin_layout.add_widget(skin_visual)
        skin_layout.add_widget(skin_utility_layout)

        return skin_layout


class ChampionInformationContainer(AnchorLayout):

    def drawInformationContainer(self):
        information_layout = AnchorLayout(anchor_x='right', anchor_y='center')
        #information_layout.add_widget(btn)
        tp = TabbedPanel(do_default_tab= False)
        tp.clear_widgets()
        defenseTab = TabbedPanelItem(text='Defense', content=self.drawDefenseLayoutContent())
        offenseTab = TabbedPanelItem(text='Offensive', content=self.drawOffensiveLayoutContent())
        utilityTab = TabbedPanelItem(text='Utility', content=self.drawUtilityLayoutContent())
        otherTab = TabbedPanelItem(text='Other', content=self.drawOtherLayoutContent())

        tp.add_widget(defenseTab)
        tp.add_widget(offenseTab)
        tp.add_widget(utilityTab)
        tp.add_widget(otherTab)

        information_layout.add_widget(tp)
        return information_layout


    def drawDefenseLayoutContent(self):
        defenseLayout = RelativeLayout()
        btn = Button(text='Defense Content Here')
        defenseLayout.add_widget(btn)
        return defenseLayout


    def drawOffensiveLayoutContent(self):
        offensiveLayout = RelativeLayout()
        btn = Button(text='Offensive Content Here')
        offensiveLayout.add_widget(btn)
        return offensiveLayout



    def drawUtilityLayoutContent(self):
        utilityLayout = RelativeLayout()
        btn = Button(text='Utility Content Here')
        utilityLayout.add_widget(btn)
        return utilityLayout



    def drawOtherLayoutContent(self):
        otherLayout = RelativeLayout()
        btn = Button(text='Other Content Here')
        otherLayout.add_widget(btn)
        return otherLayout




class ChampionVisualizerApp(App):

    def window_settings(self):
        Window.maximize()

    def build(self):
        self.window_settings()
        boxLayout = BoxLayout()
        skinLayout = ChampionSkinContainer().drawSkinContainer()
        informationLayout = ChampionInformationContainer().drawInformationContainer()
        boxLayout.add_widget(skinLayout)
        boxLayout.add_widget(informationLayout)
        return boxLayout