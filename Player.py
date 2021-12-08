#Indicator item
import numpy as np
import py.Tools.Items.Planet as tip
import py.Tools.Items.General as tig
from py.Tools.Indicator import Indicator

class IndicatorPlanet(tip.PlanetItem, Indicator):
    def __init__(self, rotatespeed = 0):
        #随机生成一个特征符合设定的主角, 初始为(低温)陨石状态
        Indicator.__init__(self) 
        mass = np.random.randint(tip.mass_range[0], tip.mass_breaks[0]) 
        tempr = np.random.randint(tip.tempr_breaks[0], tip.tempr_breaks[1]) 
        tip.PlanetItem.__init__(self, name = 'Rock', rotatespeed = rotatespeed, mass = mass, tempr = tempr) 
        
        self.itemType = 'RockPlanet' 
        self.update_size() 
        
        rocket = tig.GeneralItem(name = 'Rocket') 
        rocket.scale_to(size=self.moveimage.rect.size) 
        rocket.move_to(self.moveimage.center, Center = True) 
        self.clouds.add(rocket) 
    
    def update_situation(self):
        Categories = {(0,0):'IceRock', (0,1):'Rock', (0,2):'HotRock', (1,0):'IceRock', (1,1):'Rock', (1,2):'HotRock', (2,0):'Ice', (2,1):'Ice', (2,2):'Hot'} 
        if self.skip:   return 
        try: 
            image_name = Categories[self.categorize()] 
        except KeyError: return 
        
        if image_name == self.moveimage.name:
            return 
        
        self.update_image(image_name) 
        self.itemType = image_name + 'Planet' 
        self.Tempr.update(devalue = 2 * (1 - self.Tempr.categorize())) 
    
    def interact(self, Object):
        if not tip.is_touch_round_item(self, Object):
            return 
        
        if self.itemType in ['RockPlanet', 'HotRockPlanet', 'IceRockPlanet']:

            if Object.Mass.categorize() <= self.Mass.categorize():
                #当Object(分类)质量小于自身时, 进行碰撞与质量转移
                self.interact_give_crash(Object, rate = 0.9) 
                
                self.Mass.add(0.5 * Object.Mass.value) 
                Object.Mass.update(value = 0.5 * Object.Mass.value) 
                self.update_size() 
                Object.update_size() 
                
                self.Tempr.update(value = self.Tempr.value * 0.75 + Object.Tempr.value * 0.25) 
                Object.Ruins() 
                
                return 
                
            if Object.Mass.categorize() > self.Mass.categorize():
                #当Object质量大于自身时, 死亡
                self.suicide() 
                return 
        
        if self.itemType == 'IcePlanet':
            
            if Object.Mass.categorize() <= self.Mass.categorize():
                #当Object(分类)质量小于自身时, 根据物体不同而做出不同的判断
                if Object.itemType == 'RockPlanet':
                    self.Mass.add(Object.Mass.value) 
                    Object.Hidden() 
                    
                if Object.itemType == 'HotRockPlanet':
                    self.Mass.add(-Object.Mass.value) 
                    Object.Ruins() 
                    
                self.update_size() 
                return 
            
    
    def suicide(self):
        self.Ruins() 
        self.itemType = 'DeadPlanet' 
    
    def update(self):
        tip.PlanetItem.update(self) 
        self.update_situation() 
    
    def update_size(self):
        size_rate = self.moveimage.rect.size[0] 
        tip.PlanetItem.update_size(self) 
        size_rate = self.moveimage.rect.size[0]/size_rate 
        for item in self.clouds:
            item.scale_to(rate = size_rate) 