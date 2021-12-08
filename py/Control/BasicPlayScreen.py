#PlayScreen
import pygame
import py.Screen.PlayScreen as sp

screenID = 'PlayScreen' 
bgpName = 'default_Space' 

def init_playscreen():
    global playscreen 
    
    playscreen = sp.PlayScreen() 
    playscreen.change_bgp(name = bgpName)                                       #设置界面背景
    
    #<-------------------------------------------------------------------------
    #增加指令
    playscreen.add_command(pygame.K_ESCAPE, "self.return_newcID('PauseScreen.Reset')")  #按esc切换至IndexScreen界面



def return_screen(win_screen, Reset = False):                                   #界面输出功能return_screen(win_screen,...)
    if Reset:                                                                   #将playscreen存入输入的win_screen(Screen_Basic.WinScreen)中
        init_playscreen()                                                      #自带playscreen初始化功能, 因此无需额外调用init_indexscreen() 
    else:                                                                       #Reset参数决定是否强制初始化playscreen
        try:
            playscreen 
        except NameError:
            init_playscreen() 
        
    try:
        win_screen.add_screens(playscreen, screen_id = screenID) 
    except AttributeError:
        pass 