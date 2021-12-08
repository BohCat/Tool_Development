#test displaying
import pygame
import os
import Config_Resource as cr
from py.Screen import Basic as sb
from py.Control import HeadIndexScreen as ch
from py.Control import DifficultyIndexScreen as cd
from py.Control import BasicPlayScreen as cb
from py.Control import PauseScreen as cp

IMAGES=cr.IMAGES 
SCREEN=cr.SCREEN 
w_SCREEN=pygame.display.get_surface() 

def showplanet():   #演示窗口
    #<---------------------------此部分应被打包成一个独立的界面类型
    while True:
        for event in pygame.event.get([pygame.QUIT,pygame.KEYDOWN,pygame.KEYUP,pygame.VIDEORESIZE,pygame.USEREVENT]):
            if event.type == pygame.QUIT:
                pygame.quit() 
            if event.type == pygame.KEYDOWN:
                win_screen.get_command(event.key)                               #用win_screen指令结构监听键盘输入
            if event.type == pygame.KEYUP:
                win_screen.get_command(pygame.KEYUP) 
            if event.type == pygame.VIDEORESIZE:                                #当窗口大小变化时
                win_screen.update(UpSize=True) 
            if event.type == pygame.USEREVENT:
                if event.name == 'win_screen_command':
                    win_screen.get_command(event.value) 
                    win_screen.update(UpSize=True)                              #界面大小更新防止当窗口非初始尺寸时界面切换露馅(补丁)
                if event.name == 'default_command':                             #确认subcscreen Command_ID绑定效果
                    win_screen.get_command(event.value) 

        

        
        #sub_screen1.move_camera(location = PItem2.moveimage.center, Center=True)     #将界面镜头中心与PItem2中心绑定
        #sub_screen1.change_scale(scalecenter = PItem2.moveimage.center)              #将放缩中心与PItem2中心绑定
        
        win_screen.update(UpItems=True, item_ids='planet')                      #在win_screen层面管理更新, 仅更新显示的界面
        
        win_screen.show() 
        
        pygame.display.update() 
        cr.CLOCK.tick(cr.FPS) 
        #<----------------------------



if __name__ == "__main__":
    
    imb=IMAGES[cr.default_bgp]                                      #背景图
    winrect=pygame.display.get_surface().get_rect()                 #窗口Surface

    win_screen = sb.WinScreen(show_id = 'IndexScreen') 
    #<------
    
    #<------生成标题界面
    ch.return_screen(win_screen)                                                #生成标题界面
    cd.return_screen(win_screen)                                                #生成关卡界面
    cb.return_screen(win_screen)                                                #生成游戏界面
    cp.return_screen(win_screen)                                                #生成暂停界面
    #<------
    
    #开始播放背景音乐
    cr.main_bgm.play_music()

    win_screen.get_command(command_key = 'IndexScreen')                        #验证利用内置指令集显示切换功能
    #ch.indexscreen.return_cID()                                               #确认subscreen Command_ID绑定效果
    showplanet() 