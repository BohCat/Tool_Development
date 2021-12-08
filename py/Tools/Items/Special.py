#Special Planet Item
import numpy as np
from numpy.random import randint
from py.Tools.Items import Planet as tip

vol_min = 20 
vol_max = 200 

class RockPlanet(tip.PlanetItem):
    itemType = 'RockPlanet' 
    def __init__(self, location = None, rotatespeed = 0):
        #随机生成一个特征符合设定的陨石
        mass = np.random.randint(tip.mass_range[0], tip.mass_breaks[0]) 
        tempr = np.random.randint(tip.tempr_breaks[0], tip.tempr_breaks[1]) 
        tip.PlanetItem.__init__(self, name = 'Rock', location = location, rotatespeed = rotatespeed, mass = mass, tempr = tempr) 
        
        self.update_size() 
    
    def interact(self, Object):
        if not tip.is_touch_round_item(self, Object):
            return 
        
        if Object.Mass.categorize() <= self.Mass.categorize():
            self.interact_both_crash(Object = Object) 

class IceRockPlanet(tip.PlanetItem):
    itemType = 'IceRockPlanet' 
    def __init__(self, location = None, rotatespeed = 0):
        #随机生成一个特征符合设定的陨石
        mass = np.random.randint(tip.mass_range[0], tip.mass_breaks[0]) 
        tempr = np.random.randint(tip.tempr_range[0], tip.tempr_breaks[0]) 
        tip.PlanetItem.__init__(self, name = 'IceRock', location = location, rotatespeed = rotatespeed, mass = mass, tempr = tempr) 
        
        self.update_size() 
    
    def interact(self, Object):
        if not tip.is_touch_round_item(self, Object):
            return 
        
        if Object.Mass.categorize() <= self.Mass.categorize():
            self.interact_both_crash(Object = Object) 

class HotRockPlanet(tip.PlanetItem):
    itemType = 'HotRockPlanet' 
    def __init__(self, location = None, rotatespeed = 0):
        #随机生成一个特征符合设定的陨石
        mass = np.random.randint(tip.mass_range[0], tip.mass_breaks[0]) 
        tempr = np.random.randint(tip.tempr_breaks[1], tip.tempr_range[1]) 
        tip.PlanetItem.__init__(self, name = 'HotRock', location = location, rotatespeed = rotatespeed, mass = mass, tempr = tempr) 
        
        self.update_size() 
    
    def interact(self, Object):
        if not tip.is_touch_round_item(self, Object):
            return 
        
        if Object.Mass.categorize() <= self.Mass.categorize():
            self.interact_both_crash(Object = Object) 

class IcePlanet(tip.PlanetItem):
    itemType = 'IcePlanet' 
    def __init__(self, location = None, rotatespeed = 0):
        #随机生成一个特征符合设定的冰冻球
        mass = np.random.randint(tip.mass_breaks[1], tip.mass_breaks[2]) 
        tempr = np.random.randint(tip.tempr_range[0], tip.tempr_breaks[0]) 
        tip.PlanetItem.__init__(self, name = 'Ice', location = location, rotatespeed = rotatespeed, mass = mass, tempr = tempr) 
        
        self.update_size() 
        for i in range(randint(2, 8)):
            self.get_clouds(HeightRate = randint(0, 4), RotateSpeed = randint(-20, 20), BeginAngle = randint(-180, 180)) 
        
    def interact(self, Object):
        if not tip.is_touch_round_item(self, Object):
            return 
        
        if Object.itemType in ['RockPlanet', 'HotRockPlanet', 'IceRockPlanet']:
            self.interact_give_crash(Object = Object) 
            Object.Ruins() 
                
        if Object.itemType == 'IcePlanet':
            self.interact_both_crash(Object = Object) 
            self.Ruins(True) 
            Object.Ruins(True) 
        
        if Object.itemType == 'HotPlanet':
            self.interact_both_crash(Object = Object) 

class MiddlePlanet(tip.PlanetItem):
    itemType = 'MiddlePlanet' 
    def __init__(self, location = None, rotatespeed = 0):
        #随机生成一个特征符合设定的中等质量, 中等温度的球(暂时归类为冰冻球)
        mass = np.random.randint(tip.mass_breaks[1], tip.mass_breaks[2]) 
        tempr = np.random.randint(tip.tempr_breaks[0], tip.tempr_breaks[1]) 
        tip.PlanetItem.__init__(self, name = 'Ice', location = location, rotatespeed = rotatespeed, mass = mass, tempr = tempr) 

        self.update_size() 
        
class HotPlanet(tip.PlanetItem):
    itemType = 'HotPlanet' 
    def __init__(self, location = None, rotatespeed = 0):
        #随机生成一个特征符合设定的熔融球
        mass = np.random.randint(tip.mass_breaks[1], tip.mass_breaks[2]) 
        tempr = np.random.randint(tip.tempr_breaks[1], tip.tempr_range[1]) 
        tip.PlanetItem.__init__(self, name = 'Hot', location = location, rotatespeed = rotatespeed, mass = mass, tempr = tempr) 
        
        self.update_size() 
        for i in range(randint(2, 4)):
            self.get_clouds(HeightRate = randint(0, 4), RotateSpeed = randint(-20, 20), BeginAngle = randint(-180, 180)) 
        
    def interact(self, Object):
        if not tip.is_touch_round_item(self, Object):
            return 
        
        if Object.itemType in ['RockPlanet', 'HotRockPlanet', 'IceRockPlanet']:
            Object.Hidden() 
        
        if Object.itemType == 'IcePlanet':
            self.interact_both_crash(Object = Object) 
        
        if Object.itemType == 'HotPlanet':
            self.interact_both_crash(Object = Object) 
            self.Ruins(True) 
            Object.Ruins(True) 


#<-----------------------------------------------------------------------------

PlanetCategories = {'Rock': RockPlanet, 'IceRock': IceRockPlanet, 'HotRock': HotRockPlanet, 'Ice': IcePlanet, 'Hot': HotPlanet} 

def get_PlanetClass(name):
    try:
        return PlanetCategories[name] 
    except KeyError:    return 
