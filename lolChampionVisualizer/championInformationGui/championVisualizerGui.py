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

'''
python -m pip install --upgrade pip wheel setuptools virtualenv
python -m virtualenv kivy_venv
kivy_venv\Scripts\activate
python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2==0.1.* kivy_deps.glew==0.1.*
python -m pip install kivy_deps.gstreamer==0.1.*
python -m pip install kivy==1.11.1
pip install selenium
'''

skinContainerSize = 0.35


class ChampionSkinContainer(RelativeLayout):

    def drawSkinContainer(self):
        visual_image = 'images\\championImages\\teemo-render.png'
        skinName = visual_image.split("\\")[-1].split(".")[0].replace("_", " ")

        skin_layout = RelativeLayout(size_hint=(skinContainerSize, 1), pos_hint ={'left':1, 'top':1})
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


class ChampionInformationContainer(BoxLayout):

    def drawInformationContainer(self):
        information_layout = BoxLayout(orientation='vertical', size_hint=(1-skinContainerSize, 1))

        infoSize = (Window.width)*(1-skinContainerSize)
        infoSize = math.floor(infoSize/5)
        
        championName = Label(text="Teemo", font_size='32sp', size_hint=(1, 0.15))
        tp = TabbedPanel(tab_pos='top_mid', padding=(dp(20), dp(2), dp(2), dp(2)), tab_width=infoSize, do_default_tab= False, size_hint=(1, 0.85))

        labelText = TabbedPanelItem(text="Statistics", background_color=(0, 0, 0, 0), halign="left", disabled_color=hex('#ffffff'), font_size=20)
        labelText.disabled = True
        defenseTab = TabbedPanelItem(id='defenseTab', background_color=hex('#5BBD80'), text='Defense', content=self.drawDefenseLayoutContent())
        offenseTab = TabbedPanelItem(background_color=hex('#C3403C'), text='Offensive', content=self.drawOffensiveLayoutContent())
        rangesTab = TabbedPanelItem(background_color=hex('#0988DB'), text='Ranges', content=self.drawRangesLayoutContent())
        abilitiesTab = TabbedPanelItem(background_color=hex('#E1E135'), text='Abilities', content=self.drawAbilitiesLayoutContent())
        
        tp.add_widget(labelText)
        tp.add_widget(defenseTab)
        tp.add_widget(offenseTab)
        tp.add_widget(rangesTab)
        tp.add_widget(abilitiesTab)

        #switches the tabbed panel to whatever we want to set as our default
        Clock.schedule_once(lambda dt: tp.switch_to(defenseTab), 0.1)
        information_layout.add_widget(championName)
        information_layout.add_widget(tp)
        return information_layout


    # defense resources: armor, heal and shield power, health, health regeneration, magic resistance, tenacity, slow resist
    def drawDefenseLayoutContent(self):
        defenseLayout = BoxLayout(orientation="vertical")

        # layouts for resources
        healthLayout = self.createResourceLayouts(image='images\\icons\\health.png', label="Health", value="110 - 200")
        healthRegenLayout = self.createResourceLayouts(image='images\\icons\\health.png', label="Health\nRegeneration", value="100 - 200")
        armorLayout = self.createResourceLayouts(image='images\\icons\\shield.png', label="Armor", value="100 - 200")
        magicResistanceLayout = self.createResourceLayouts(image='images\\icons\\shield.png', label="Magic\nResistance", value="100 - 200")
        manaLayout = self.createResourceLayouts(image='images\\icons\\shield.png', label="Mana", value="100 - 200")
        manaRegenLayout = self.createResourceLayouts(image='images\\icons\\shield.png', label="Mana\nRegeneration", value="100 - 200")

        row1 = self.combineBoxLayouts(healthLayout, healthRegenLayout)
        row2 = self.combineBoxLayouts(manaLayout, manaRegenLayout)
        row3 = self.combineBoxLayouts(armorLayout, magicResistanceLayout)

        defenseLayout.add_widget(row1)
        defenseLayout.add_widget(row2)
        defenseLayout.add_widget(row3)
        return defenseLayout

    # offense resources: abiity power, armor penetration, attack damage, attack speed, critical strike chance, critical strike damage, life steal, magic penetration, spell vamp
    def drawOffensiveLayoutContent(self):
        offensiveLayout = BoxLayout(orientation="vertical")

        # layouts for resources
        attackDamangeLayout = self.createResourceLayouts(image='images\\icons\\health.png', label="Attack\nDamage", value="110 - 200")
        criticalDamageLayout = self.createResourceLayouts(image='images\\icons\\health.png', label="Critical\nDamage", value="100 - 200")
        baseAttackSpeedLayout = self.createResourceLayouts(image='images\\icons\\shield.png', label="Base\nAttack Speed", value="100 - 200")
        attackSpeedRatioLayout = self.createResourceLayouts(image='images\\icons\\shield.png', label="Attack\nSpeed Ratio", value="100 - 200")
        bonusAttackSpeedLayout = self.createResourceLayouts(image='images\\icons\\shield.png', label="Bonus\nAttack Speed", value="100 - 200")
        attackWindupLayout = self.createResourceLayouts(image='images\\icons\\shield.png', label="Attack\nWindup", value="100 - 200")

        row1 = self.combineBoxLayouts(attackDamangeLayout, criticalDamageLayout)
        row2 = self.combineBoxLayouts(baseAttackSpeedLayout, bonusAttackSpeedLayout)
        row3 = self.combineBoxLayouts(attackWindupLayout, attackSpeedRatioLayout)

        offensiveLayout.add_widget(row1)
        offensiveLayout.add_widget(row2)
        offensiveLayout.add_widget(row3)
        return offensiveLayout


    # utility resources: cooldown reduction, energy, energy regeneration, mana, mana regeneration
    def drawRangesLayoutContent(self):
        rangesLayout = BoxLayout(orientation="vertical")

        # layouts for resources
        gameplayRadiusLayout = self.createResourceLayouts(image='images\\icons\\shield.png', label="Hit\nBox", value="100 - 200")
        pathingRadiusLayout = self.createResourceLayouts(image='images\\icons\\health.png', label="Pathing\nRadius", value="110 - 200")
        selectionRadiusLayout = self.createResourceLayouts(image='images\\icons\\health.png', label="Selection\nRadius", value="100 - 200")
        autoRadiusLayout = self.createResourceLayouts(image='images\\icons\\shield.png', label="Auto\nRadius", value="100 - 200")
        attackRangeLayout = self.createResourceLayouts(image='images\\icons\\shield.png', label="Attack\nRange", value="100 - 200")     
        blankLayout = GridLayout(cols=4, padding=[15,20,0,0], size_hint=(0.3, 1))

        row1 = self.combineBoxLayouts(attackRangeLayout, autoRadiusLayout)
        row2 = self.combineBoxLayouts(gameplayRadiusLayout, pathingRadiusLayout)
        row3 = self.combineBoxLayouts(selectionRadiusLayout, blankLayout)

        rangesLayout.add_widget(row1)
        rangesLayout.add_widget(row2)
        rangesLayout.add_widget(row3)
        return rangesLayout


    # other resources: experience, gold generation, movement speed, range
    def drawAbilitiesLayoutContent(self):
        otherLayout = RelativeLayout()
        btn = Label(text='Abilities Content Here')
        otherLayout.add_widget(btn)
        return otherLayout


    # creates the layout for the resources depicted in the tabs
    def createResourceLayouts(self, image, label, value):
        label = self.padLabelWidth(label)
        layout = GridLayout(cols=4, padding=[15,20,0,0], size_hint=(0.3, 1))
        icon = Image(source=image, keep_ratio=True, size_hint_x= 0.4, pos_hint ={'left':1, 'top':1})
        label = Label(text=label, font_size="24sp", halign="left", valign="middle", pos_hint ={'left':1, 'top':1})
        value = Label(text=value, font_size="20sp", halign="left", valign="middle", pos_hint ={'left':1, 'top':1})
        layout.add_widget(icon)
        layout.add_widget(label)
        layout.add_widget(value)
        return layout


    def padLabelWidth(self,labelText):
        if len(labelText) >= 10:
            return labelText
        while len(labelText) != 10:
            labelText += " "
        return labelText



    def combineBoxLayouts(self, layout1, layout2=BoxLayout()):
        rowDefenseLayout = BoxLayout(orientation="horizontal")
        rowDefenseLayout.add_widget(layout1)
        rowDefenseLayout.add_widget(layout2)
        return rowDefenseLayout



class buildChampionVisualizerGui(Screen):

    def __init__(self, **kwargs):
        super(buildChampionVisualizerGui, self).__init__(**kwargs)
        self.add_widget(self.getLayout())


    def getLayout(self):
        boxLayout = BoxLayout()
        skinLayout = ChampionSkinContainer().drawSkinContainer()
        informationLayout = ChampionInformationContainer().drawInformationContainer()
        boxLayout.add_widget(skinLayout)
        boxLayout.add_widget(informationLayout)
        return boxLayout