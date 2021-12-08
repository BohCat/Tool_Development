#Drawing function & Data structure
#被Screen使用的基础类, 包括基本指令结构Indicator以及附加指令的InteractImage类
#除python第三方包外仅调用Tools, Item层以及Config_Resource
import pygame
from py.Tools import Pre as tp
from py.Tools.Items.General import GeneralItem
from py.Tools.Images.General import MoveImage, InteractImage
from py.Tools.Indicator import Indicator
from Config_Resource import default_image_id, default_item_id, default_bgp

class ID_Set():
    MaxID = 200 
    #编号储存相同类型的实例
    #不同编号间用key做区分, 相同编号的实例将被同时调用
    """
    Data:
        indexes - dict{dict{}}
        show_id - 
        Elempyte - class
    Function:
        __init__
        __str__
        add_elem
        add_elems
        change_show_id
        get_command
        get_show_index
        show
    """
    def __init__(self, Elemtype, show_id = None):
        self.indexes = {} 
        self.show_id = show_id 
        self.Elemtype = Elemtype            #记录允许的实例类型, 创建后不被更改
    
    def __str__(self):
        return (f"indexes = {self.indexes}\nshow_id = {self.show_id}\nElemtype = {self.Elemtype}\n")
    
    def __len__(self):
        try:
            return len(self.get_show_index()) 
        except TypeError:
            return 0 
    
    def add_elem(self, elem = None, elemSetID = None, elemID = None):
        #将输入的self.Elemtype类型实例记录至self.indexes中, 引用方式为self.indexes['elemSetID']['Elemtype']
        #elemSetID为elem所属的集合的ID, 用于辨别不同的elem集合
        #只有在单独调用此add_elem时才能通过elemID参数指定elem在集合中的ID
        try:                                                                    #确保存在以elemSetID为key的字典项
            sub_set = self.indexes[elemSetID] 
        except KeyError:
            sub_set = {} 
            self.indexes[elemSetID] = sub_set 
        
        if self.show_id not in self.indexes:                                    #确保self.show_id指向存在的字典项
            self.show_id = elemSetID 
        
        if not isinstance(elem, self.Elemtype):                                 #确保存入的elem 是指定的Elemtype
            return 
        
        if elemID == None:  elemID = 0 
        if elemID in sub_set:                                                   #保障ID的唯一性
            for i in range(1,self.MaxID+1):
                elemID = str(i) 
                if elemID not in sub_set:   break 
                
        sub_set[elemID] = elem                                                  #给予存入的elem 一个set内唯一的ID
        
        try:                                                                    #若elem内存在记录ID的变量, 则将ID存入此变量中
            elem.itemID = elemID 
        except AttributeError:  pass 
        try:                                                                    #|
            elem.screenID = elemID 
        except AttributeError:  pass 

    def add_elems(self, *arg, elemSetID = None):
        for elem in arg:
            self.add_elem(elem = elem, elemSetID = elemSetID) 
    
    def remove_elem(self, elemID, elemSetID = None):
        if elemSetID not in self.indexes:
            elemSetID = self.show_id 

        try:
            self.indexes[elemSetID].pop(elemID) 
            return True 
        except KeyError:    return False 
    
    def remove_set(self, elemSetID):
        if elemSetID == self.show_id:
            return False 
            
        try:
            self.indexes.pop(elemSetID) 
            return True 
        except KeyError:
            return False 
    
    def remove_all(self):
        try:
            for elemSetID in self.indexes.copy():
                self.indexes.pop(elemSetID) 
            return True 
        except: False 
    
    def change_show_id(self, new_id):
        self.show_id = new_id 
    
    def get_command(self, command_key):
        #从外界传入指令的接口
        #将指令在显示实例之间广播
        try:
            for elem in self.indexes[self.show_id]:
                if isinstance(self.indexes[self.show_id][elem], Indicator):
                    self.indexes[self.show_id][elem].get_command(command_key) 
        except KeyError:
            pass 
    
    def get_show_index(self):
        try:
            return self.indexes[self.show_id] 
        except KeyError:
            pass 
    
    def show(self, SCREEN, center = None, scale_rate = None, correct = None, add_show_id = ()):
        try:
            for elem in self.indexes[self.show_id]:
                self.indexes[self.show_id][elem].draw(SCREEN, center = center, scale_rate = scale_rate, correct = correct) 
        except TypeError:
            for elem in self.indexes[self.show_id]:
                self.indexes[self.show_id][elem].draw(SCREEN) 
        except KeyError:
            pass 
        except AttributeError:
            pass 
         
        for showID in add_show_id:
            if showID == self.show_id:
                continue 
                
            try:
                self.indexes[showID] 
            except KeyError: pass 
            
            try:
                for elem in self.indexes[showID]:
                    self.indexes[showID][elem].draw(SCREEN, center = center, scale_rate = scale_rate, correct = correct) 
            except TypeError:
                for elem in self.indexes[showID]:
                    self.indexes[showID][elem].draw(SCREEN) 
            except KeyError:
                pass 
            except AttributeError:
                pass 
        


class SubScreen(Indicator):
    #游戏界面, 界面之间具有独立的显示, 用于管理与排版游戏图像, 并被用于输出到游戏窗口
    #一个界面内含有一个indicator, indicator具有基本的指令存储, 添加, 调用操作, 对SubScreen的指令操作即为对indicator的指令操作
    #赋予指令结构
    """
    Data:
        (Tools_Image.Indicator)
        screen - pygame.Surface
        draw_rect - pygame.rect.Rect
        camera_rect - pygame.rect.Rect
        screen_id - 
        
        indicator - Control_Indicator.Indicator
        items - ID_Set(type = Item_General.GeneralItem)
        images - ID_Set(type = Tools_Image.MoveImage)
        bgp - Tools_Image.MoveImage
        
        scalerate - number
        scalecenter - tuple(location)
    Function:
        (Tools_Image.Indicator)
        __init__
        __str__
        add_items
        add_images
        move_camera
        change_show_id
        change_bgp
        change_scale
        get_command
        update
        update_size
        update_items
        show
        draw
    """
    def __init__(self, size = None, center = None, rect = None, scale_rate = None, scale_center = None):
        Indicator.__init__(self)
        if isinstance(rect,pygame.rect.Rect):
            size = rect.size 
            center = rect.center 
        else:
            if not tp.is_location_tuple(size):
                size = pygame.display.get_surface().get_size() 
            if not tp.is_location_tuple(center):
                center = (size[0]//2, size[1]//2) 
            
        self.screen = pygame.Surface(size = size)                               #界面画布, 用来排版游戏图像
        self.draw_rect = self.screen.get_rect(center = center)                  #界面位置, 用来指示在窗口的显示区域, 取相对窗口坐标
        self.camera_rect = self.draw_rect.copy()                                #界面画布范围(镜头), 用来截取范围内的图像, 取绝对坐标
        self.screenID = None                                                    #界面id, 相同id的界面在窗口上具有相同的更新/不更新表现
        
        self.indicator = Indicator()                                            #该界面的可操作对象, 一个界面只能有一个操作对象
        self.items = ID_Set(Elemtype = GeneralItem)                             #该界面记录的GeneralItem类型
        self.images = ID_Set(Elemtype = InteractImage)                          #该界面记录的InteractImage类型
        self.bgp = MoveImage() 
        
        self.scalerate = scale_rate if tp.is_number(scale_rate) else 1     #界面放缩比例
        self.scalecenter = scale_center if tp.is_location_tuple(scale_center) else self.camera_rect.center     #界面放缩中心
    def __str__(self):
        return Indicator.__str__(self)

    def add_items(self, *arg, itemSetID = default_item_id):
        for item in arg:
            self.items.add_elem(elem = item, elemSetID = itemSetID) 
    
    def add_images(self, *arg, imageSetID = default_image_id):
        for image in arg:
            self.images.add_elem(elem = image, elemSetID = imageSetID) 
    
    def move_camera(self, location = None, Vector = False, Center = False):
        #将界面画布(镜头)范围移动到指定位置/指定位移
        if tp.is_location_tuple(location):
            if Vector:
                self.camera_rect.move_ip(location)
            else:
                if Center:
                    self.camera_rect = self.screen.get_rect(center = location) 
                else:
                    self.camera_rect.update(location, self.camera_rect.size) 

    def change_show_id(self, item_id = None, image_id = None, IgnoreNone = True):
        #IgnoreNone: 是否忽略None输入, 默认开启, 此时输入None即为不改变id
        if IgnoreNone and item_id == None:
            self.items.change_show_id(item_id) 
        if IgnoreNone and image_id == None:
            self.images.change_show_id(image_id) 
    
    def change_bgp(self, name = default_bgp, bgp_image = None):
        self.bgp = MoveImage(name = name, orimage = bgp_image) 
    
    def change_scale(self, scalecenter = None, scalerate = None):
        if tp.is_location_tuple(scalecenter):
            self.scalecenter = scalecenter 
        if tp.is_number(scalerate):
            self.scalerate = scalerate 
    
    def get_command(self, command_key):
        try:
            Indicator.get_command(self, command_key) 
        except KeyError:
            self.indicator.get_command(command_key) 
    
    def get_show_items(self):
        return self.items.get_show_index() 
    
    def get_show_images(self):
        return self.images.get_show_index() 
    
    def update(self, UpSize = False, size = None, center = None, rect = None, UpItems = False, item_ids = default_item_id):
        if UpSize:
            self.update_size(size = size, center = center, rect = rect) 
        if UpItems:
            try:
                iter(item_ids) 
            except TypeError:
                item_ids = [item_ids] 
            if type(item_ids) == str:
                item_ids = [item_ids] 
            
            for item_id in item_ids:
                self.update_items(item_id = item_id) 
    
    def update_size(self, size = None, center = None, rect = None):
        """根据外部输入更新界面尺寸以及相关参数"""
        if isinstance(rect,pygame.rect.Rect):
            size = rect.size 
            center = rect.center 
        else:
            if not tp.is_location_tuple(size):
                size = pygame.display.get_surface().get_size() 
            if not tp.is_location_tuple(center):
                center = (size[0]//2, size[1]//2) 
        
        if tp.is_location_tuple(size) and size != self.draw_rect.size:
            self.screen = pygame.Surface(size = size) 
            self.draw_rect = self.screen.get_rect(center = center) 
            self.camera_rect = self.screen.get_rect(center = self.camera_rect.center) 
    
    def update_items(self, item_id = default_item_id):
        #对于指定id的item执行item.update()命令
        try:
            for item in self.items.indexes[item_id]:
                if isinstance(self.items.indexes[item_id][item], GeneralItem):
                    self.items.indexes[item_id][item].update() 
        except KeyError:
            None 
    
    def show_bgp(self):
        """将self.bgp填充到整个界面"""
        #当bgp尺寸远小于当前界面尺寸时慎用, 爆卡! 需要进一步优化
        temp_rect = self.bgp.rect 
        temp_rect.update((temp_rect.x % (-temp_rect.w), temp_rect.y % (-temp_rect.h)),(temp_rect.size)) #将bgp的左上顶点校准到(-w, 0) * (-h, 0)范围
        
        wm = ((self.draw_rect.w - temp_rect.x) // self.bgp.rect.w) + 1        #计算沿宽度方向铺满界面需要的bgp数
        hm = ((self.draw_rect.h - temp_rect.y) // self.bgp.rect.h) + 1        #计算沿高度方向铺满界面需要的bgp数
        temp_rect = self.bgp.rect.copy()                                    #使用copy()赋值, 防止后续填充过程中对原始self.bgp.rect产生影响
        for i in range(wm):
            for j in range(hm):
                self.screen.blit(self.bgp.image, temp_rect)                 #<-:
                temp_rect.move_ip(0, temp_rect.h)                           #先沿高度方向填充
            temp_rect.move_ip(temp_rect.w, -hm * temp_rect.h)               #沿宽度方向移动一个bgp宽度, 重复上述填充
    
    def show(self, add_show_id = ()):
        #显示指定id下的item与image.
        correct = tp.dot_tuple(self.camera_rect.topleft,-1) 
        self.items.show(self.screen, center = self.scalecenter, scale_rate = self.scalerate, correct = correct, add_show_id = add_show_id) 
        self.images.show(self.screen) 
    
    def draw(self, SCREEN):
        #将界面图像显示在输入的Surface上
        self.show_bgp()     #填充背景
        self.show()         #显示内部图像
        if isinstance(SCREEN, pygame.Surface):
            SCREEN.blit(self.screen, self.draw_rect) 
            
            
class WinScreen(Indicator):
    #游戏窗口,用于管理与显示游戏界面
    #赋予指令结构
    """
    Data:
        (Tools_Image.Indicator)
        screen - pygame.Surface(window)
        sub_screens - ID_Set 
    Function:
        (Tools_Image.Indicator)
        __init__
        __str__
        add_screen
        change_show_id
        get_command
        show
    """
    def __init__(self, *arg, show_id = None):
        show_id = str(show_id) 
        Indicator.__init__(self, Command_ID = 'Windows')
        self.screen = pygame.display.get_surface()                                  #获取系统显示的Surface实例
        self.sub_screens = ID_Set(Elemtype = SubScreen, show_id = show_id)          #创建管理Surface的ID结构, 并指定需要显示的Surface编号
        for screen in arg:
            self.sub_screens.add_elem(elem = screen, elemSetID = show_id)                           #添加第一批Surface
        self.add_command(command_key = show_id, command = "self.change_show_id('" + show_id + "')") 
    
    def __str__(self):
        return Indicator.__str__(self) + "screen = pygame.display.get_surface()\nsub_screens:\n" + self.sub_screens.__str__()
    
    def add_screens(self, *arg, screen_id = None):
        screen_id = str(screen_id) 
        for screen in arg:
            self.sub_screens.add_elem(elem = screen, elemSetID = screen_id) 
            if isinstance(screen, SubScreen):
                screen.Command_ID = screen_id 
        #<---------------------------------------------------------------------
        #添加界面时增加 切换至显示该界面类 的指令
        self.add_command(command_key = screen_id, command = "self.change_show_id('" + screen_id + "')")
    
    def change_show_id(self, new_id):
        self.sub_screens.change_show_id(new_id) 
        
    def get_command(self, command_key):
        try:
            Indicator.get_command(self, command_key) 
        except KeyError:
            self.sub_screens.get_command(command_key) 
    
    def get_show_screens(self):
        return self.sub_screens.get_show_index() 
    
    def update(self, UpSize = False, size = None, center = None, rect = None, UpItems = False, item_ids = default_item_id):
        subscreens = self.sub_screens.get_show_index() 
        for screen in subscreens:
            subscreens[screen].update(UpSize = UpSize, size = size, center = center, rect = rect, UpItems = UpItems, item_ids = item_ids) 
        
    
    def show(self):
        self.sub_screens.show(self.screen) 