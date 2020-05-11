import kivy
import math
from os import listdir
from os.path import isfile, join
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
from kivy.uix.behaviors import ButtonBehavior 
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.graphics.svg import Svg


skinContainerSize = 0.35


class ChampionSkinContainer(RelativeLayout):

    def __init__(self, champion, sm=None, **kw):
        super().__init__(**kw)
        self.sm = sm
        self.championName = champion

    def drawSkinContainer(self):
        skinDirectory = 'images\\championImages\\'+self.championName
        skinList = [f for f in listdir(skinDirectory) if (isfile(join(skinDirectory, f)) and 'icon' not in f)]
        self.skinIndex = 0
        self.skinDirectory = skinDirectory
        self.skinList = skinList

        renderList = []
        for skin in skinList:
            if "render" in skin.lower():
                renderList.append(skin)
        visual_image = skinDirectory + "\\" + renderList[0]
        skinName = visual_image.split("\\")[-1].replace(".png", "").replace("_", " ").replace("%27", "'").title()
        if "Iv" in skinName:
            skinName = skinName.replace("Iv", "IV")

        skin_layout = RelativeLayout(size_hint=(skinContainerSize, 1), pos_hint ={'left':1, 'top':1})
        skin_utility_layout = GridLayout(cols=3, size_hint=(1, 0.2), pos_hint ={'left':1, 'bottom':1})
        leftButtonLayout = AnchorLayout(anchor_x='left')
        rightButtonLayout = AnchorLayout(anchor_x='right')

        skin_visual = Image(source=visual_image, size_hint=(0.8, 0.7), pos_hint ={'right':0.93, 'top':0.95}, keep_ratio=True, allow_stretch=True)
        skin_text = Label(text=skinName, size_hint=(0.8, 1), font_size=20)
        left_button = Button(on_press=lambda l:self.rotateChampionSkin("left", skin_visual, skin_text), background_normal='images\\icons\\left-arrow-white.png', background_down ='images\\icons\\left-arrow-white_pressed.png', size_hint=(0.3, 0.3), pos_hint ={'x':0.5, 'y':0.5}, border=(0, 0, 0, 0))
        right_button = Button(on_press=lambda r:self.rotateChampionSkin("right", skin_visual, skin_text), background_normal='images\\icons\\right-arrow-white.png', background_down ='images\\icons\\right-arrow-white_pressed.png', size_hint=(0.3, 0.3), pos_hint ={'x':0.5, 'y':0.5}, border=(0, 0, 0, 0))

        leftButtonLayout.add_widget(left_button)
        rightButtonLayout.add_widget(right_button)

        skin_utility_layout.add_widget(leftButtonLayout)
        skin_utility_layout.add_widget(skin_text)
        skin_utility_layout.add_widget(rightButtonLayout)

        skin_layout.add_widget(skin_visual)
        skin_layout.add_widget(skin_utility_layout)

        return skin_layout
    
    def rotateChampionSkin(self, direction, displayedImage, skinName):
        index = self.skinIndex
        directory = self.skinDirectory
        skinList = self.skinList
        if direction == "left":
            index -= 1
        else:
            index += 1
        index = index % len(skinList)
        # sets the skinIndex
        if index == -1:
            self.skinIndex = index = len(skinList) - 1
        else:
            self.skinIndex = index
        # changes the skin
        displayedImage.source = directory + "\\" + skinList[index]
        skinName.text = skinList[index].replace("_", " ").replace(".png", "").replace(".jpg", "").replace(".jpeg", "").replace("%27", "'").title()
        if "Iv" in skinName.text:
            skinName.text = skinName.text.replace("Iv", "IV")
            


class ChampionInformationContainer(BoxLayout):

    def __init__(self, screen, statisticsContent, champion, sm=None, **kw):
        super().__init__(**kw)
        self.sm = sm
        self.screen = screen
        self.championName = champion
        self.content = statisticsContent

    def drawInformationContainer(self):
        information_layout = BoxLayout(orientation='vertical', size_hint=(1-skinContainerSize, 1))
        championNameLayout = RelativeLayout(size_hint=(1, 0.15))

        infoSize = (Window.width)*(1-skinContainerSize)
        infoSize = math.floor(infoSize/5)
        
        championName = Label(text=self.championName, font_size='32sp', pos_hint={'middle': 1, 'top': 1})
        back_button = Button(on_press=lambda back:self.returnToSearch(), background_normal='images\\icons\\back-arrow-white.png', background_down ='images\\icons\\back-arrow-white_pressed.png', size_hint=(0.03, 0.2), pos_hint={'right': 0.98, 'y': 0.75}, border=(0, 0, 0, 0))
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
        championNameLayout.add_widget(championName)
        championNameLayout.add_widget(back_button)
        information_layout.add_widget(championNameLayout)
        information_layout.add_widget(tp)
        return information_layout

    # method to return to the searchGui
    def returnToSearch(self):
        self.sm.current = 'championSearch'
        self.sm.remove_widget(self.screen)

    # defense resources: armor, heal and shield power, health, health regeneration, magic resistance, tenacity, slow resist
    def drawDefenseLayoutContent(self):
        defenseLayout = BoxLayout(orientation="vertical")

        # layouts for resources
        healthLayout = self.createResourceLayouts(image='images\\icons\\health.png', label="Health", value=self.content['Health'])
        healthRegenLayout = self.createResourceLayouts(image='images\\icons\\health_regeneration.png', label="Health\nRegeneration", value=self.content['Health regen'])
        armorLayout = self.createResourceLayouts(image='images\\icons\\armor.png', label="Armor", value=self.content['Armor'])
        magicResistanceLayout = self.createResourceLayouts(image='images\\icons\\magic_resistance.png', label="Magic\nResistance", value=self.content['Magic resist'])

        if 'Energy' in self.content:
            resourceLayout = self.createResourceLayouts(image='images\\icons\\energy.png', label="Energy", value=self.content['Energy'])
            resourceRegenLayout = self.createResourceLayouts(image='images\\icons\\energy_regeneration.png', label="Energy\nRegeneration", value=self.content['Energy regen'])
        elif 'Mana' in self.content:
            resourceLayout = self.createResourceLayouts(image='images\\icons\\mana.png', label="Mana", value=self.content['Mana'])
            resourceRegenLayout = self.createResourceLayouts(image='images\\icons\\mana_regeneration.png', label="Mana\nRegeneration", value=self.content['Mana regen'])
        else: 
            resourceLayout = self.createResourceLayouts(image='images\\icons\\resource.png', label="Resource", value=self.content['Resource'])
            try:
                resourceRegenLayout = self.createResourceLayouts(image='images\\icons\\resource_regeneration.png', label="Resource\nRegeneration", value=self.content['Resource regen'])
            except:
                resourceRegenLayout = self.createResourceLayouts(image='images\\icons\\secondary_bar.png', label="Secondary\Bar", value=self.content['Secondary Bar'])    

        row1 = self.combineBoxLayouts(healthLayout, healthRegenLayout)
        row2 = self.combineBoxLayouts(resourceLayout, resourceRegenLayout)
        row3 = self.combineBoxLayouts(armorLayout, magicResistanceLayout)

        defenseLayout.add_widget(row1)
        defenseLayout.add_widget(row2)
        defenseLayout.add_widget(row3)
        return defenseLayout

    # offense resources: abiity power, armor penetration, attack damage, attack speed, critical strike chance, critical strike damage, life steal, magic penetration, spell vamp
    def drawOffensiveLayoutContent(self):
        offensiveLayout = BoxLayout(orientation="vertical")

        # layouts for resources
        attackDamangeLayout = self.createResourceLayouts(image='images\\icons\\attack_damage.png', label="Attack\nDamage", value=self.content['Attack damage'])
        criticalDamageLayout = self.createResourceLayouts(image='images\\icons\\critical_strike.png', label="Critical\nDamage", value=self.content['Crit damage'])
        baseAttackSpeedLayout = self.createResourceLayouts(image='images\\icons\\attack_speed.png', label="Base\nAttack Speed", value=self.content['Base AS'])
        attackSpeedRatioLayout = self.createResourceLayouts(image='images\\icons\\attack_speed_ratio.png', label="Attack\nSpeed Ratio", value=self.content['AS ratio'])
        bonusAttackSpeedLayout = self.createResourceLayouts(image='images\\icons\\bonus_attack_speed.png', label="Bonus\nAttack Speed", value=self.content['Bonus AS'])
        attackWindupLayout = self.createResourceLayouts(image='images\\icons\\attack_windup.png', label="Attack\nWindup", value=self.content['Attack windup'])

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
        gameplayRadiusLayout = self.createResourceLayouts(image='images\\icons\\hit_box_radius.png', label="Hit\nBox", value=self.content['Gameplay radius'])
        pathingRadiusLayout = self.createResourceLayouts(image='images\\icons\\pathing_radius.png', label="Pathing\nRadius", value=self.content['Pathing radius'])
        selectionRadiusLayout = self.createResourceLayouts(image='images\\icons\\selection_radius.png', label="Selection\nRadius", value=self.content['Selection radius'])
        autoRadiusLayout = self.createResourceLayouts(image='images\\icons\\auto_radius.png', label="Auto\nRadius", value=self.content['Auto radius'])
        attackRangeLayout = self.createResourceLayouts(image='images\\icons\\attack_range.png', label="Attack\nRange", value=self.content['Attack range'])   
        movementSpeedLayout = self.createResourceLayouts(image='images\\icons\\movement_speed.png', label="Movement\nSpeed", value=self.content['Move speed'])  

        row1 = self.combineBoxLayouts(attackRangeLayout, autoRadiusLayout)
        row2 = self.combineBoxLayouts(gameplayRadiusLayout, pathingRadiusLayout)
        row3 = self.combineBoxLayouts(movementSpeedLayout, selectionRadiusLayout)

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
        icon = Image(source=image, keep_ratio=True, size_hint_x= 0.2, pos_hint ={'left':1, 'top':1})
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

    def __init__(self, statisticsContent, champion, sm=None, **kwargs):
        super(buildChampionVisualizerGui, self).__init__(**kwargs)
        self.sm = sm
        self.add_widget(self.getLayout(champion, content=statisticsContent))


    def getLayout(self, givenChampionName, content):
        boxLayout = BoxLayout()
        skinLayout = ChampionSkinContainer(champion=givenChampionName, sm=self.sm).drawSkinContainer()
        informationLayout = ChampionInformationContainer(champion=givenChampionName, statisticsContent=content, screen=self, sm=self.sm).drawInformationContainer()
        boxLayout.add_widget(skinLayout)
        boxLayout.add_widget(informationLayout)
        return boxLayout