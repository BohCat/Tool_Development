#Tools for image
#除python第三方包外仅调用Tools层以及Config_Resource
import pygame
import numpy as np
import Config_Resource as cr
from py.Tools import Pre as tp
from py.Tools.Indicator import Indicator

class MoveImage():
    #包含一个pygame.Surface类型变量及其常用位置参数
    #并含有移动、原地旋转、复制等简单操作函数
    """
    Data:
        image - pygame.Surface
        rect - pygame.rect.Rect
        center - tuple (location)
        name
    Function:
        __init__
        __str__
        move_to
        rotate
        scale_to
        get_vetex
        copy
        draw
    """
    def __init__(self, name = "Item", orimage = None):
        if isinstance(orimage, pygame.Surface):
            self.image = orimage.copy() 
        else:
            self.image = cr.IMAGES[name].copy() 
        self.name = name                            #使用的图片名
        #self.ID 可能可以用于区分各个图片的标签
        self.rect = self.image.get_rect()     #使用的rect
        self.center = self.rect.center        #rect的几何中心（类型为tuple, 不会随rect变化而自动更新）
    
    def __str__(self):
        return f"name: {self.name}\nlocation = ({self.rect.x}, {self.rect.y})\ncenter = ({self.center})\n"
    
    def move_to(self, location = (0, 0), Vector = False, Center = False):
        """
        Vector: False - move to the given location
        Vector: True - move by the given vector
        """
        if not tp.is_location_tuple(location):
            return 
            
        if Vector:
            self.rect.move_ip(location) 
        elif Center:
            self.rect = self.image.get_rect(center = location) 
        else:
            self.rect.update(location, self.rect.size)     
        self.center = self.rect.center                  #更新几何中心
    
    def rotate(self, angle = 0, PiMode = False):
        """
        PiMode: False - angle is expressed without pi
        PiMode: True - angle is expressed by pi
        """
        if PiMode:
            angle = angle * 180 / np.pi 
        
        self.image = pygame.transform.rotate(self.image, angle) 
        self.rect = self.image.get_rect(center = self.center) 
    
    def scale_to(self, rate = None, size = None):
        #放缩围绕图片几何中心进行, rate为放缩比例, size为放缩后的尺寸, 当rate为数字时size无效
        if tp.is_number(rate):
            size = tp.dot_tuple(self.image.get_size(), rate) 
            
        if tp.is_location_tuple(size):
            self.image = pygame.transform.scale(self.image, size) 
            self.rect = self.image.get_rect(center = self.center) 
    
    def get_vertex(self):
        #返回左上角顶点的坐标
        return self.rect.topleft 
    
    def get_center(self):
        return self.rect.center 
    
    def copy(self):
        new_Mimage = MoveImage(orimage=self.image.copy()) 
        new_Mimage.move_to((self.rect.x, self.rect.y)) 
        return new_Mimage 
    
    def draw(self, SCREEN, center = None, scale_rate = None, correct = None):
        """图像缩放"""
        #center, correct是元素为数字的二元组, scale_rate是数字
        #只有当缩放中心center与缩放率scale_rate同时有意义, 才会进行缩放
        if tp.is_location_tuple(center) and tp.is_number(scale_rate):
            vect = tp.minus_location_tuple(center, self.center) 
            vect = tp.dot_tuple(vect, 1 - scale_rate) 
            self.move_to(vect, Vector=True)             #将中心移动到缩放后的中心
            self.scale_to(rate = scale_rate)            #原地缩放
            
        """图像位置矫正"""
        if tp.is_location_tuple(correct):               #根据矫正向量correct将图像位置坐标变换为显示的相对坐标
            self.rect.move_ip(correct) 
        
        SCREEN.blit(self.image, self.rect) 


class InteractImage(MoveImage, Indicator):
    #在MoveImage的基础上拓展交互接口, 新增辨识ID以及指令映射表
    """
    Data:
        (Tools_Image.MoveImage)
        (Indicator)
    Function:
        (Tools_Image.MoveImage)
        (Indicator)
        __init__
        __str__
    """
    def __init__(self, name = "Item", orimage = None, Command_ID = None):
        MoveImage.__init__(self, name = name, orimage = orimage) 
        Indicator.__init__(self, Command_ID = Command_ID) 
    
    def __str__(self):
        return MoveImage.__str__(self) + Indicator.__str__(self) 