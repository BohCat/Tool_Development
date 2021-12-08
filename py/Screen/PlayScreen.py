#PlayScreen
from numpy.random import randint
from Player import IndicatorPlanet
from Config_Resource import default_item_id, FPS
import pygame
import py.Screen.Basic as sb
import py.Tools.Pre as tp
import py.Tools.Items.Special as tis



class PlayScreen(sb.SubScreen):
    def __init__(self, scale_rate = None):
        sb.SubScreen.__init__(self, scale_rate = scale_rate) 
        #self.indicator                                                         #indicator 由self.restart()定义
        self.restart() 
        
        self.BasicSpeed = -100 
        self.MaxItem = 1 
        self.spawn_list = ['Rock', 'HotRock', 'IceRock']*3+['Ice','Hot'] 
        
        self.update_screen_speed() 
        #<---------------------------------------------------------------------
        #Indicator类:增加重设指令
        self.add_command('Reset', 'self.restart()') 
    
    def restart(self):
        #将界面重设至初始状态
        self.items.remove_all() 
        self.indicator = IndicatorPlanet(rotatespeed = 20) 
    
    def change_spawn_rate(self, new_list):
        #重设随机概率(在list中随机挑选一个名字以生成星球)
        self.spawn_list = new_list 
    
    def get_planet(self, name = None, spawn_rect = None):
        #目前可以根据输入的名字生成星球类型
        #应当由spawn_range来指定生成的范围
        #若不输入则默认在全屏生成
        PlanetClass = tis.get_PlanetClass(name) 
        if PlanetClass == None:     PlanetClass = tis.RockPlanet 
        
        if not isinstance(spawn_rect, pygame.rect.Rect):
            spawn_rect = self.camera_rect 
        else:
            correct = tp.dot_tuple(self.camera_rect.topleft,-1) 
            spawn_rect.topleft = tp.add_location_tuple(spawn_rect.topleft, correct) 
        
        while True:
            #判断新生成的item是否与现有item重叠 
            location = randint(spawn_rect.x, spawn_rect.right), randint(spawn_rect.y, spawn_rect.bottom) 
            PItem = PlanetClass(location = location, rotatespeed = randint(-40, 40)) 
            temp_dict = self.items.get_show_index() 
            if temp_dict == None:   temp_dict = {} 
            flag = True 
            for item in temp_dict:
                if PItem.moveimage.rect.colliderect(temp_dict[item].moveimage.rect):
                    flag = False 
                    break 
            if flag: break 
        
        PItem.update_speed(speed = (self.BasicSpeed + randint(-10,10), randint(-10,10))) 
        self.add_items(PItem, itemSetID = 'planet') 
        
        #print(PItem.moveimage.rect) 
        #print(PItem.move.speed.location) 
    
    def get_planets(self, num, name = None, spawn_rect = None):
        #批量生成星球
        if type(num) != int:
            return 
        for i in range(num):
            self.get_planet(name = name, spawn_rect = spawn_rect) 
    
    def update(self, UpSize = False, size = None, center = None, rect = None, UpItems = False, item_ids = default_item_id):
        try:
            iter(item_ids) 
            if 'planet' not in item_ids:    item_ids += ['planet'] 
            if 'deadplanet' not in item_ids:item_ids += ['deadplanet'] 
        except TypeError:
            item_ids = ['planet', 'deadplanet'] if (default_item_id in ['planet', 'deadplanet'] or default_item_id == None) else [default_item_id] + ['planet', 'deadplanet'] 
        sb.SubScreen.update(self, UpSize = UpSize, size = size, center = center, rect = rect, UpItems = UpItems, item_ids = item_ids) 
        self.indicator.update() 
        y = self.indicator.moveimage.center[1]                                  #限制indicator的y轴位置
        if y < self.camera_rect.y + self.camera_rect.h//10:
            y = self.camera_rect.y + self.camera_rect.h//10 
        if y > self.camera_rect.y + (self.camera_rect.h - self.camera_rect.h//10):
            y = self.camera_rect.y + (self.camera_rect.h - self.camera_rect.h//10) 
        
        dy = (self.camera_rect.midleft[1] - y)/FPS 
        flag = 1 if dy >= 0 else -1 
        if dy != 0:
            y += dy if abs(dy) > 1 else flag                                    #y自动回到中点
        
        center = (self.camera_rect.x + self.camera_rect.w//10, y) 
        self.indicator.move_to(location = center, Center = True) 
        #
        #<---------------------------------------------------------------------
        #item交互检测部分:
        temp_dict = self.items.get_show_index() 
        if temp_dict == None:   temp_dict = {} 
        for item in temp_dict:
            self.indicator.interact(temp_dict[item]) 
        
        for item1 in temp_dict:
            for item2 in temp_dict:
                if item1 == item2:  continue 
                temp_dict[item1].interact(temp_dict[item2]) 
        #
        #<---------------------------------------------------------------------
        #地图速度更新:
        self.update_screen_speed() 
        #
        #<---------------------------------------------------------------------
        #item显示更新、生成与移除部分:
        """
        此处为管理生成密度的关键代码
        """
        temp_rect1 = pygame.rect.Rect(tp.add_location_tuple(self.camera_rect.topleft, (-200, -200)), tp.add_location_tuple(self.camera_rect.size, (400, 400))) 
        #temp_rect1 为边界范围, 超出此边界的所有item都会被移除
        temp_rect2 = pygame.rect.Rect(self.camera_rect.topright, (400, self.camera_rect.h)) 
        #temp_rect2 为额外生成检测范围, 只有当此范围或生成范围(temp_rect3)内item数量小于一定值(分布密度足够小)时才会生成item
        temp_rect3 = pygame.rect.Rect(self.camera_rect.topright, (200, self.camera_rect.h)) 
        #temp_rect3 为生成范围, 在此范围内生成item
        
        temp_dict = self.items.get_show_index()                                 #维护self.items的'show_index'集合
        if temp_dict == None:   temp_dict = {}                                  #|
        count = 0                                                               #初始化count
        for item in temp_dict.copy():
            if temp_dict[item].skip:                                            #转移死亡物体
                self.items.add_elem(temp_dict[item], elemSetID = 'deadplanet') 
                self.items.indexes['deadplanet'] 
                self.items.remove_elem(item, elemSetID = 'planet') 
                continue 
            if not temp_rect1.colliderect(temp_dict[item].moveimage.rect):      #移除temp_rect1范围外物体
                self.items.remove_elem(item) 
                continue 
            if temp_dict[item].move.speed.distance((0, 0)) <= 20/FPS:           #移除低速物体
                self.items.remove_elem(item, elemSetID = 'planet') 
                continue 
            if temp_rect2.colliderect(temp_dict[item].moveimage.rect
                                      ) or temp_rect3.colliderect(
                                          temp_dict[item].moveimage.rect):      #检测是否需要生成item, flag为检测范围内item的数量
                count += 1 
        
        if count < self.MaxItem:                                                #根据flag的标注生成item
            name = self.spawn_list[randint(0, len(self.spawn_list))] 
            self.get_planet(name = name, spawn_rect = temp_rect3) 
        #<-----------------------------维护其它item集合
        try:                                                                    #维护self.items的'deadplanet'集合
            temp_dict = self.items.indexes['deadplanet'] 
        except KeyError:    temp_dict = {}                           
        for item in temp_dict.copy():
            if temp_dict[item].move.speed.distance((0, 0)) <= 20/FPS:           #移除低速物体
                self.items.remove_elem(item, elemSetID = 'deadplanet') 
                continue 
            if not temp_rect1.colliderect(temp_dict[item].moveimage.rect):      #移除temp_rect1范围外物体
                self.items.remove_elem(item, elemSetID = 'deadplanet') 
                continue 
    
    def update_screen_speed(self, speed = None, map_speed = None):
        if not tp.is_number(speed):
            speed = self.camera_rect.h/(1.5 + self.indicator.Mass.categorize()) + (self.camera_rect.h//8) * (self.indicator.Tempr.categorize() - 1) 
        
        self.indicator.add_command(pygame.K_LEFT, f'self.update_speed((0, {-speed}))') 
        self.indicator.add_command(pygame.K_UP, f'self.update_speed((0, {-speed}))') 
        self.indicator.add_command(pygame.K_RIGHT, f'self.update_speed((0, {speed}))') 
        self.indicator.add_command(pygame.K_DOWN, f'self.update_speed((0, {speed}))') 
        self.indicator.add_command(pygame.KEYUP, 'self.update_speed((0, 0))') 
        
        if not tp.is_number(map_speed):
            map_speed = -100 - 30 * self.indicator.Mass.categorize() 
        self.BasicSpeed = map_speed 
    
    def show(self):
        sb.SubScreen.show(self, ['deadplanet']) 
        try:
            correct = tp.dot_tuple(self.camera_rect.topleft,-1) 
            self.indicator.draw(self.screen, correct = correct) 
        except AttributeError:  pass 