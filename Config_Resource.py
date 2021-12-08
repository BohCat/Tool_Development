#init configuration for resources and windows
import pygame
import os
from py.Tools import Pre as tp

GravetyConstant = 1 

W, H=800,600                #初始窗口大小
FPS=30                      #每秒帧处理数量
Path_Graph="Data\Graph"     #图像资源路径

Path_Sound="Data\Sound"     #声音资源路径

default_bgp = "default_Space"        #备选图像名
default_empty = "Empty"
default_Planet = "default_Planet"
default_Cloud = "default_Planet.Clouds"
default_SS = "default_SpaceShip"
default_item_id = None 
default_image_id = None 
default_select = "default_select"
default_textbox = "default_textbox"

name_indicator = "INDICATOR"

pygame.init() 

IMAGES={}                   #加载图形资源
image_source=[]
for image in os.listdir(Path_Graph):
    name, extension = os.path.splitext(image)   #提取文件名，后缀（二者分离）
    image_source.append(name)                   #建立字典项
    path=os.path.join(Path_Graph, image)        #读图
    IMAGES[name]=pygame.image.load(path)        #存入字典
    

#<---------------------------------------------------->
# 加载声音资源
# pygame库中关于声音部分的官方文档链接：https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound
# 本部分主要灵感来自：https://github.com/Mio19/Pygame-Magical-Slime

#加载pygame中负责声音的模块
pygame.mixer.init() 
if not pygame.mixer or not pygame.mixer.get_init():
    print("Warning, sound disabled")

#定义两个控制声音的类，所有与声音有关的功能都在这两个类中实现
#游戏有两种声音，一种是背景音乐，需要不断循环播放，另一种是简单的短提示音，播放一遍即可。
class BackGroudMusic(pygame.mixer.Sound):#背景音乐类需要循环播放
    """
    Methods:
        __init__(name = "xxx.wav", volume = 10.0)
        play_music(volume = None) - 播放音乐 - 如果没有传入volume参数按照原定的音量播放
        stop_music() - 停止音乐
        change_volume(volume = None) - 调整音量
    """

    def __init__(self, name = "start.wav", volume = 10.0):#注意传入的volume值是float类型
        global Path_Sound
        fullname = os.path.join(Path_Sound, name)#文件的完整路径名
        pygame.mixer.Sound.__init__(self,file = fullname)
        if tp.is_number(volume):
            self.change_volume(volume)
        else:
            self.change_volume(10.0)

    # 播放音乐调用本函数
    def play_music(self, volume = None):#注意传入的volume值是float类型
        self.change_volume(volume)
        self.stop_music()
        pygame.mixer.Sound.play(self,loops=-1)
        # 根据pygame的官方文档，loops=-1时，声音将无限循环，直到调用self.stop_music()停止播放。
        # According to official documents, if loops is set to -1, the Sound will loop indefinitely。

    # 停止音乐调用本函数
    def stop_music(self):
        pygame.mixer.Sound.stop(self)

    #调整音量调用本函数
    def change_volume(self, volume = None):#注意传入的volume值是float类型
        if tp.is_number(volume):
            pygame.mixer.Sound.set_volume(self,float(volume))


class ShortMusic(pygame.mixer.Sound):#短提示音只需播放一次
    """
    Methods:
        __init__(name = "xxx.wav", volume = 10.0)
        play_music(volume = None) - 播放音乐 - 如果没有传入volume参数按照原定的音量播放
        stop_music() - 停止音乐
        change_volume(volume = None) - 调整音量
    """
    #初始化对象
    def __init__(self, name = "start.wav", volume = 10.0):#注意传入的volume值是float类型
        global Path_Sound
        fullname = os.path.join(Path_Sound, name)#文件的完整路径名
        pygame.mixer.Sound.__init__(self,file = fullname)
        if tp.is_number(volume):
            self.change_volume(volume)
        else:
            self.change_volume(10.0)

    # 播放音乐调用本函数
    def play_music(self, volume = None):#注意传入的volume值是float类型
        self.change_volume(volume)
        pygame.mixer.Sound.play(self,loops=0)
        # 根据pygame的官方文档，loops=0时,声音只播放一次

    # 停止音乐调用本函数
    def stop_music(self):
        pygame.mixer.Sound.stop(self)

    #调整音量调用本函数
    def change_volume(self, volume = None):
        if tp.is_number(volume):
            pygame.mixer.Sound.set_volume(self,float(volume))

#定义用到的声音对象
start_music = BackGroudMusic(name = "start.wav")
boom_sound = ShortMusic(name = "boom.wav")
main_bgm = BackGroudMusic(name = "main_bgm.wav")


#<------------------------------------------------------------------------------------------------->
    
#建立窗口
SCREEN=pygame.display.set_mode(size = (W,H)) 
pygame.display.set_caption("A testing program") 
pygame.display.set_icon(IMAGES["Icon"]) 
CLOCK=pygame.time.Clock()                       #建立定时器