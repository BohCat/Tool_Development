#暂停界面
import pygame
from py.Screen import IndexScreen as si

screenID = 'PauseScreen' 
bgpScreenID = 'PlayScreen' 
bgpName = 'Space1' 

def init_indexscreen(win_screen = None):                                        #界面初始化脚本init_indexscreen() 
    winrect = pygame.display.get_surface().get_rect() 
    
    global indexscreen 
    
    indexscreen = si.IndexScreen(size= winrect.size, scale_rate=1) 
    
    icon_image = si.Icon_Image(name = 'Index.Select.Continue', Command_ID = 'PlayScreen')      #创建选项
    indexscreen.add_images(icon_image, imageSetID='icon') 
    icon_image = si.Icon_Image(name = 'Index.Select.Config', Command_ID = 'ConfigScreen') 
    indexscreen.add_images(icon_image, imageSetID='icon') 
    icon_image = si.Icon_Image(name = 'Index.Select.Restart', Command_ID = 'PlayScreen.Reset') 
    indexscreen.add_images(icon_image, imageSetID='icon') 
    icon_image = si.Icon_Image(name = 'Index.Select.Back', Command_ID = 'IndexScreen') 
    indexscreen.add_images(icon_image, imageSetID='icon') 
    indexscreen.set_icon_location(ShowMode='|')                                 #|-设置选项排列模式
    
    indexscreen.set_indicator(indicator_name='Select_Icon')                     #初始化选项箭头
    
    try:
        indexscreen.change_bgp(win_screen = win_screen, bgpScreenID = bgpScreenID) #尝试以win_screen中bgpScreenID界面为背景设置界面背景
    except NameError:
        indexscreen.change_bgp(name = bgpName)                                  #以静态图片bgpName为背景设置界面背景
    
    #<-------------------------------------------------------------------------
    #增加指令
    indexscreen.add_command(pygame.K_ESCAPE, "self.return_newcID('PlayScreen')")  #按esc切换至PlayScreen界面

def return_screen(win_screen, Reset = False):                                   #界面输出功能return_screen(win_screen,...)
    if Reset:                                                                   #将indexscreen存入输入的win_screen(Screen_Basic.WinScreen)中
        init_indexscreen(win_screen)                                            #自带indexscreen初始化功能, 因此无需额外调用init_indexscreen() 
    else:                                                                       #Reset参数决定是否强制初始化indexscreen
        try:
            indexscreen
        except NameError:
            init_indexscreen(win_screen) 
        
    try:
        win_screen.add_screens(indexscreen, screen_id = screenID) 
    except AttributeError:
        pass 