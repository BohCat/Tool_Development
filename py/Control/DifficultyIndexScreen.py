#关卡选择界面
import pygame
from py.Screen import IndexScreen as si

screenID = 'DifficultyScreen' 
bgpName = 'Space1' 

def init_indexscreen():                                                         #界面初始化脚本init_indexscreen() 
    winrect = pygame.display.get_surface().get_rect() 
    
    global indexscreen 
    
    indexscreen = si.IndexScreen(size= winrect.size, scale_rate=1) 
    
    icon_image = si.Icon_Image(name = 'Index.Select.Start', Command_ID = 'PlayScreen.Reset')      #创建选项
    indexscreen.add_images(icon_image, imageSetID='icon') 
    icon_image = si.Icon_Image(name = 'Index.Select.Others', Command_ID = 'None') 
    indexscreen.add_images(icon_image, imageSetID='icon') 
    icon_image = si.Icon_Image(name = 'Index.Select.Others', Command_ID = 'None') 
    indexscreen.add_images(icon_image, imageSetID='icon') 
    icon_image = si.Icon_Image(name = 'Index.Select.Others', Command_ID = 'None') 
    indexscreen.add_images(icon_image, imageSetID='icon') 
    indexscreen.set_icon_location(ShowMode='|')                                 #|-设置选项排列模式
    
    indexscreen.set_indicator(indicator_name='Select_Icon')                     #初始化选项箭头
    indexscreen.change_bgp(name = bgpName)                                       #设置界面背景
    
    #<-------------------------------------------------------------------------
    #增加指令
    indexscreen.add_command(pygame.K_ESCAPE, "self.return_newcID('IndexScreen')")  #按esc切换至IndexScreen界面

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