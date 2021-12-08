#Modified drawing function & Data structure (IndexScreen), 针对菜单界面专门适配的MoveImage, ID_Set, InteractImage与SubScreen
#除python第三方包外仅调用Tools, Item, Camera层以及Config_Resource
import pygame
import numpy as np
from Config_Resource import default_item_id, default_select, name_indicator, default_bgp
from py.Screen import Basic as sb
from py.Tools import Pre as tp

class Icon_Image(sb.InteractImage):
    #与InteractImage相同, 但不再向下传递指令
    #内置基本操作指令
    #增加了将自身Command_ID借助pygame.USEREVENT传出的功能
    def __init__(self, name = "Item", orimage = None, Command_ID = None):
        sb.InteractImage.__init__(self, name = name, orimage = orimage, Command_ID = Command_ID) 
        self.add_command(pygame.K_SPACE, 'self.return_select()') 
        self.add_command(pygame.K_RETURN, 'self.return_select()') 
    
    def get_command(self, command_key):
        try:
            sb.InteractImage.get_command(self, command_key) 
        except KeyError:
            pass 
    def return_select(self):
        #将自身Command_ID借助pygame.USEREVENT传出
        temp_event = pygame.event.Event(pygame.USEREVENT, name = 'win_screen_command', creater = 'Icon_Image', value = self.Command_ID) 
        pygame.event.post(temp_event) 

class Icon_Set(sb.ID_Set):
    #针对Screen_Basic.InteractImage数据类型专门编写的ID_Set子类
    #唯一地绑定一个SubScreen类型
    """
    Data:
        (Camera_Basic.ID_Set)
        ShowMode_str - list[str]
        loce_screen - Camera_Basic.SubScreen
        ShowMode - str
    Function:
        (Camera_Basic.ID_Set)
        __init__
        __str__
        list_ShowMode
        is_locked
        lock
        set_icon_location
    """
    ShowMode_str = ['|', '||', 'O'] 
    def __init__(self, show_id = None):
        sb.ID_Set.__init__(self, Elemtype = sb.InteractImage, show_id = None) 
        self.lock_screen = None              #绑定记录自己的SubScreen
        self.ShowMode = '|' 
    
    def __str__(self):
        return sb.ID_Set.__str__(self) + f"lock_screen = {self.lock_screen}\nShowMode = {self.ShowMode}\n" 
    
    def list_ShowMode(self):
        print(f"ShowModeList:\n{self.ShowMode_str}\n")
    
    def is_locked(self):
        return isinstance(self.lock_screen, sb.SubScreen) 
    
    def lock(self, subscreen):
        #输入并绑定一个SubScreen
        if isinstance(subscreen, sb.SubScreen) and not self.is_locked():
            self.lock_screen = subscreen 
    
    def set_icon_location(self, ShowMode = None):
        #根据绑定的SubScreen 尺寸与输入的icon排列模式重新排列当前的显示icon集
        if not self.is_locked():
            return 
        
        if ShowMode in self.ShowMode_str:
            self.ShowMode = ShowMode 
        else:
            ShowMode = self.ShowMode 
        
        temp_icons = self.get_show_index() 
        temp_rect = self.lock_screen.draw_rect 
        
        if ShowMode == '|':
            dh = temp_rect.h//(len(temp_icons) + 3) 
            height = 2 * dh 
            for icon in temp_icons:
                temp_icons[icon].move_to(location = (temp_rect.center[0], height), Center = True) 
                height += dh 
        
        if ShowMode == '||':
            dh = temp_rect.h//(len(temp_icons)//2 + 3) 
            dw = temp_rect.w//3 
            height = 2 * dh 
            width = dw 
            
            for icon in temp_icons:
                temp_icons[icon].move_to(location = (width, height), Center = True) 
                if width > temp_rect.center[0]:
                    width = dw 
                    height += dh 
                else:   width = 2 * dw 
        
        if ShowMode == 'O':
            center = pygame.display.get_surface().get_rect().center 
            radius = min((min(pygame.display.get_surface().get_rect().size)-150)//2, 250) 
            angle = 0 
            for icon in temp_icons:
                temp_icons[icon].move_to(location = tp.add_location_tuple(center,(np.sin(angle) * radius, -np.cos(angle) * radius)), Center = True) 
                angle += (np.pi * 2) / len(temp_icons)

class Indicator_Image(sb.InteractImage, sb.Indicator):
    #显示选项的箭头, 继承自Screen_Basic.InteractImage类型, 充当IndexScreen类型的indicator
    """
    Data:
        (Screen_Basic.InteractImage)
        select_icon_set - dict{Screen_Basic.InteractImage}
        select_icon - Screen_Basic.InteractImage
        select_index - int
        select_length - int
        
        add_command( pygame.K_LEFT: ..., pygame.K_RIGHT: ..., pygame.K_UP: ..., pygame.K_DOWN: ... )
    Function:
        (Screen_Basic.InteractImage)
        __init__
        __bool__
        change_select_set
        switch_select
        get_command
        draw
    """
    def __init__(self, name = default_select, orimage = None):
        sb.InteractImage.__init__(self, name = name, orimage = orimage, Command_ID = name_indicator) 
        
        self.select_icon_set = None     #记录显示选项icon的集合与当前选项在集合中的下标(list化), 初始为空
        self.select_icon = None         #
        self.select_index = None        #仅能被内置操作修改
        self.select_length = None       #记录所有icon选项的个数, 仅在select_icon_set变更时变更
    
    def __bool__(self):
        #当self.select_index非int时返回False
        return type(self.select_index) == int 
    
    def change_select_set(self, icons):
        #更改选项icons的集合
        if isinstance(icons, Icon_Set):
            self.select_icon_set = icons.get_show_index() 
            self.select_index = None 
            self.select_length = len(self.select_icon_set) 
    
    def switch_select(self, switch_dire = None):
        #当select_icon_set记录了一组icons时(即成功执行了一次change_select_set), 根据switch_dire的值计算箭头指向的新选项, 并同步箭头位置
        if type(self.select_icon_set) == dict:
            switch_dire = 0 if type(switch_dire) != int else switch_dire % self.select_length 
            self.select_index = 0 if self.select_index == None else (self.select_index + switch_dire) % self.select_length 
            
            self.select_icon = self.select_icon_set[list(self.select_icon_set)[self.select_index]] 
            
            self.move_to(location = self.select_icon.get_center(), Center=True) 
    
    def get_command(self, command_key):
        #在原始函数的基础上增加忽略无效输入的功能
        #此函数仅作为指令链的尾部而被使用
        try:
            sb.InteractImage.get_command(self, command_key) 
        except KeyError:
            if isinstance(self.select_icon, sb.Indicator):
                self.select_icon.get_command(command_key) 
        """def hidden(self):
        #隐藏indicator
        #暂时无用
        self.select_icon, self.select_index = None, None """
    
    def draw(self, SCREEN):
        #当self.select_index非int时不显示图像
        if self.__bool__():
            sb.InteractImage.draw(self, SCREEN) 

class IndexScreen(sb.SubScreen):
    #针对菜单界面专门编写的SubScreen子类
    """
    Data:
        (Camera_Basic.SubScreen)
        images - Icon_Set
        indicator - InteractImage (with command set)
    Function:
        (Camera_Basic.SubScreen)
        __init__
        set_icon_location
        update
    """
    def __init__(self, size = None, center = None, rect = None, scale_rate = None, scale_center = None):
        #生成类似SubScreen, 但self.images更改为存储Icon_Set数据类型
        sb.SubScreen.__init__(self, size = size, center = center, rect = rect, scale_rate = scale_rate, scale_center = scale_center) 
        self.images = Icon_Set() 
        self.images.lock(self) 
        #<---------------------------------------------------------------------
        #Indicator类:增加重设指令
        self.add_command('Reset', 'self.restart()') 
    
    def change_bgp(self, name = None, bgp_image = None, win_screen = None, bgpScreenID = None):
        #更改背景图片并记录此次更改
        #优先检测win_screen与bgpScreenID参数, 若win_screen是WinScreen且含有SetID为bgpScreenID的界面, 则将此集合内的界面作为背景使用
        #若上述检测失败但self记录了可用的win_screen以及bgpScreenID, 则将记录的界面作为背景使用
        #若上述检测失败, 则使用bgpName, bgpImage参数进行默认的sb.SubScreen.change_bgp()更改, 并记录bgpName, bgpImage
        try:
            temp_set = win_screen.sub_screens.indexes[bgpScreenID] 
            temp_image = pygame.Surface(size = win_screen.screen.get_rect().size) 
            [temp_set[screen].draw(temp_image) for screen in temp_set] 
            sb.SubScreen.change_bgp(self, bgp_image = temp_image) 
            self.store_WinScreen = win_screen 
            self.store_bgpScreenID = bgpScreenID 
            return 
        except AttributeError:  pass 
        except: print('UnknownError1') 
        
        try:
            self.change_bgp(win_screen = self.store_WinScreen, bgpScreenID = self.store_bgpScreenID) 
            return 
        except AttributeError:  pass 
        
        try:
            sb.SubScreen.change_bgp(self, name, bgp_image) 
            self.store_bgpName = name 
            self.store_bgpImage = bgp_image 
            return 
        except AttributeError:  pass 
        except: print('UnknownError2') 
        
        try:
            self.change_bgp(name = self.store_bgpName, bgp_image = self.store_bgpImage) 
            return 
        except AttributeError:  pass 
    
    def restart(self):
        #将界面重设至初始状态
        self.indicator.change_select_set(self.images) 
        self.change_bgp() 
    
    def set_indicator(self, indicator_name = default_select, orimage = None):
        #创建箭头, 仅在选项icons集合不为空时才能被成功创建
        if self.images:
            self.indicator = Indicator_Image(name = indicator_name, orimage = orimage) 
            self.indicator.change_select_set(self.images) 
        
        self.indicator.add_command(pygame.K_LEFT, 'self.switch_select(-1)')     #|内置indicator操作指令集
        self.indicator.add_command(pygame.K_RIGHT, 'self.switch_select(1)')     #|
        self.indicator.add_command(pygame.K_UP, 'self.switch_select(-1)')       #|
        self.indicator.add_command(pygame.K_DOWN, 'self.switch_select(1)')      #|
    
    def set_icon_location(self, ShowMode = None):
        #根据界面的大小、显示icons的数量以及输入的显示模式规则排列icons
        self.images.set_icon_location(ShowMode = ShowMode) 
    
    def update(self, UpSize = False, size = None, center = None, rect = None, UpItems = False, item_ids = default_item_id):
        #更新画面, 使界面内图像显示在合理位置
        sb.SubScreen.update(self, UpSize = UpSize, size = size, center = center, rect = rect, UpItems = UpItems, item_ids = item_ids) 
        
        temp_dict = self.items.get_show_index()
        if temp_dict != None:
            temp_list = list(temp_dict)                                         #运动Item碰撞检测, 暂存于此
            map_item = temp_list[0] 
            for item in temp_list[1:]:
                temp_dict[item].interact_accept_crash(Object = temp_dict[map_item]) 
                temp_dict[item].interact_accept_crash(Object = self.camera_rect) 
            
        if UpSize:
            self.set_icon_location() 
            if self.indicator:
                self.indicator.switch_select() 
    
    def show(self):
        sb.SubScreen.show(self) 
        try:
            self.indicator.draw(self.screen) 
        except AttributeError:  pass 