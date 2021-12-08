#Spwanning the HeadIndex, 生成标题界面
#含有生成/重置方法以及输出界面实例的方法
#起脚本作用
import numpy as np
import pygame
from py.Screen import IndexScreen as si
from py.Tools.Items import Special as tis

screenID = 'IndexScreen' 
bgpName = 'Space1' 

def init_indexscreen():                                                         #界面初始化脚本init_indexscreen() 
    winrect = pygame.display.get_surface().get_rect() 
    
    global indexscreen 
    
    indexscreen = si.IndexScreen(size= winrect.size, scale_rate=1) 
    
    icon_image = si.Icon_Image(name = 'Index.Select.Start', Command_ID = 'DifficultyScreen')      #创建选项
    indexscreen.add_images(icon_image, imageSetID='icon') 
    icon_image = si.Icon_Image(name = 'Index.Select.Continue', Command_ID = 'PlayScreen') 
    indexscreen.add_images(icon_image, imageSetID='icon') 
    icon_image = si.Icon_Image(name = 'Index.Select.Config', Command_ID = 'ConfigScreen') 
    indexscreen.add_images(icon_image, imageSetID='icon') 
    icon_image = si.Icon_Image(name = 'Index.Select.Others', Command_ID = 'Groups') 
    indexscreen.add_images(icon_image, imageSetID='icon') 
    icon_image = si.Icon_Image(name = 'Index.Select.Others', Command_ID = 'Quit') 
    indexscreen.add_images(icon_image, imageSetID='icon') 
    indexscreen.set_icon_location(ShowMode='O')                                 #|-设置选项排列模式
    
    """
    for i in range(3):                                                          #(旧代码)创建(模拟)选项
        icon_image = si.Icon_Image(name = 'Icon1', Command_ID = 'PlayScreen')   #|-赋予选项输出指令
                                                                                #|-给模拟选项添加应答逻辑
        indexscreen.add_images(icon_image, imageSetID='icon')                   #|-将选项存入界面, 显示编号为'icon'
    indexscreen.set_icon_location(ShowMode='O')                                 #|-设置选项排列模式
    """
    
    indexscreen.set_indicator(indicator_name='Select_Icon')                     #初始化选项箭头
    
    BGPItem = tis.IceRockPlanet(rotatespeed = -40) 
    indexscreen.add_items(BGPItem, itemSetID = 'planet') 
    for name in ['Rock', 'Rock', 'Ice', 'HotRock', 'HotRock', 'Hot']:
        PlanetClass = tis.get_PlanetClass(name) 
        BGPItem = PlanetClass(location = (np.random.randint(winrect.x,winrect.right), np.random.randint(winrect.y, winrect.bottom)), rotatespeed = np.random.randint(-40,40)) 
        BGPItem.update_speed(speed = (np.random.randint(-20, 20), np.random.randint(-20, 20))) 
        BGPItem.update_speed_limit(MaxSpeed = 50) 
        indexscreen.add_items(BGPItem, itemSetID = 'planet') 
    
    indexscreen.change_bgp(name = bgpName)                                       #设置界面背景

def return_screen(win_screen, Reset = False):                                   #界面输出功能return_screen(win_screen,...)
    if Reset:                                                                   #将indexscreen存入输入的win_screen(Screen_Basic.WinScreen)中
        init_indexscreen()                                                      #自带indexscreen初始化功能, 因此无需额外调用init_indexscreen() 
    else:                                                                       #Reset参数决定是否强制初始化indexscreen
        try:
            indexscreen
        except NameError:
            init_indexscreen() 
        
    try:
        win_screen.add_screens(indexscreen, screen_id = screenID) 
    except AttributeError:
        pass 