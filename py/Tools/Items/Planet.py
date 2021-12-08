#Planet
import pygame
import Config_Resource as cr
from py.Tools import Pre as tp
from py.Tools.Items import General as tig
from py.Tools.Items.Pre import ItemValue

mass_range = (1, 10**8-1) 
mass_breaks = (10**3, 10**6, 10**7) 
tempr_range = (0, 500) 
tempr_breaks = (200, 300) 
vol_min = 20 
vol_max = 200 
#生成Mass与Tempr的基本数据, 属于初始设置, 暂存于此


def vector_disassemble(vd = None, r = None):
    #将向量vd沿r方向与垂直r方向做正交分解
    #返回包含两个分解向量的元组(vr, va), 其中vr平行r方向, va垂直r方向
    if not (tp.is_location_tuple(vd) and tp.is_location_tuple(r)):
        return 
    
    distance = tp.distance_location_tuple(r, (0, 0)) 
    if distance == 0:
        return 
    elif distance != 1:
        tp.dot_tuple(r, 1/distance) 
    
    a, b = r 
    x, y = vd 
    c, d = b*y+a*x, b*x-a*y 
    return ((c*a, c*b), (d*b, -d*a)) 

def vector_crash(v1 = None, v2 = None, m1 = None, m2 = None, rate = None):
    #根据输入的速度与质量计算碰撞后速度, v1, m1分别为物体1的速度与质量, v2, m2分别为物体2的速度与质量, rate为速度衰减(-)/保持(+)率
    #返回包含两个新速度的元组(v1', v2'), 其中v1'是物体1的新速度, v2'是物体2的新速度
    if not (tp.is_location_tuple(v1) and tp.is_location_tuple(v2)):
        return 
    
    if not (tp.is_number(m1) and tp.is_number(m2)):
        m1 = m2 = 1 
    rate = rate % 1.01 if tp.is_number(rate) else 1 
    new_v1 = tp.dot_tuple(tp.add_location_tuple(tp.dot_tuple(v1, m1-m2), tp.dot_tuple(v2, 2 * m2)), rate/(m1 + m2)) 
    new_v2 = tp.dot_tuple(tp.add_location_tuple(tp.dot_tuple(v2, m2-m1), tp.dot_tuple(v1, 2 * m1)), rate/(m1 + m2)) 
    return (new_v1, new_v2)

def number_gravety(mass = None, distance = None, g = cr.GravetyConstant):
    #计算重力加速度，distance与输出值为float变量
    if not(tp.is_number(mass) and tp.is_number(distance)):
        return 
        
    if distance == 0:
        return 0 
    return mass * g / (distance ** 2) 

def vector_gravety(mass = None, vector = None, g = cr.GravetyConstant):
    #功能同gravety，但用tuple变量代替float来表示距离distance与输出值addspeed
    if not (tp.is_number(mass) and tp.is_location_tuple(vector)):
        return 

    distance = tp.distance_location_tuple(vector, (0, 0)) 
    if distance == 0:
        return (0, 0) 
    else:
        rate = number_gravety(mass = mass, distance = distance)/distance 
        return tp.dot_tuple(vector, rate) 

def vector_reflect(vd = None, r = None, rate = None):
    #计算速度向量vd在方向r上的反弹, vr为单位向量时,反射后的向量模不变, rate为速度衰减(-)/保持(+)率
    if not(tp.is_location_tuple(vd) and tp.is_location_tuple(r)):
        return 
        
    rate = rate % 1.01 if tp.is_number(rate) else 1                                #碰撞率取(-1~0)的小数, 无数字输入则取-1
    
    vr, va = vector_disassemble(vd,r) 
    vr = tp.dot_tuple(vr, -rate) 
    return tp.add_location_tuple(vr, va)

def is_touch_round_item(item1 = None, item2 = None):
    #检测两个tig.SurroundedItem是否应该发生碰撞, 碰撞箱取圆形, 半径为Item矩形框架 长、宽均值的一半
    try:
        if item1.skip:  return                                                  #若item1含有skip参数并且值为True, 则跳过检测
    except AttributeError:  pass 
    try:
        if item2.skip:  return                                                  #若item2含有skip参数并且值为True, 则跳过检测
    except AttributeError:  pass 
    
    if not(isinstance(item1, tig.SurroundedItem) and isinstance(item1, tig.SurroundedItem)):
        return 

    distance = tp.distance_location_tuple(item1.moveimage.center, item2.moveimage.center) 
    radius = (item1.moveimage.rect.w + item1.moveimage.rect.h + item2.moveimage.rect.w + item2.moveimage.rect.h) // 4 
    return distance <= radius 

def is_touch_bound(item = None, winrect = None):
    #检测tig.SurroundedItem是否与给定Rect的边界发生碰撞, 若winrect不是Rect变量则将其重设为窗口Rect
    if not isinstance(item, tig.SurroundedItem):
        return 
        
    if not isinstance(winrect, pygame.rect.Rect):
        winrect = pygame.display.get_surface().get_rect() 
    irect = item.moveimage.rect 
    return not winrect.contains(irect) 

def get_bound_direction(item = None, winrect = None):
    #得到发生碰撞时边界给予的径向向量, 若不发生碰撞则返回0向量
    if not isinstance(item, tig.SurroundedItem):
        return 
        
    if not isinstance(winrect, pygame.rect.Rect):
        winrect = pygame.display.get_surface().get_rect() 
    irect = item.moveimage.rect 
    try:
        if irect.x <= winrect.x:
            speed_x = (1, 0) 
        elif irect.x + irect.w >= winrect.w:
            speed_x = (-1, 0) 
        
        if irect.y <= winrect.y:
            speed_y = (0, 1) 
        elif irect.y + irect.h >= winrect.h:
            speed_y = (0, -1) 
        
        speed = tp.add_location_tuple(speed_x, speed_y) 
        return tp.dot_tuple(speed, 2**0.5) 
    except NameError:
        try:
            return speed_x 
        except NameError:
            try:
                return speed_y 
            except NameError:
                return (0, 0)

#<-----------------------------------------------------------------------------
class PlanetItem(tig.SurroundedItem):
    """
    Data:
        (Tools.Items.General.SurroundedItem)
        self.skip
        self.Mass
        self.Tempr
    Methods:
        (Tools.Items.General.SurroundedItem)
        interact_gravety
        interact_accept_gravety
        interact_crash_direction
        interact_accept_crash
        interact_both_crash
    """
    
    itemType = 'PlanetItem' 
    
    def __init__(self, name = cr.default_Planet, location = None, rotatespeed = 0, mass = None, tempr = None, detemprate = None):
        tig.SurroundedItem.__init__(self, name = name, location = location, rotatespeed = rotatespeed) 
        self.skip = False                                                       #标记该item是否参与item碰撞检测
        self.update_speed_limit(MaxSpeed = 200) 
        
        #<---将属性封装成类
        self.Mass = ItemValue(mass, 0, mass_range, mass_breaks)                 #质量, Planet类基本属性之一(feature), 用于归类Planet, 以及进行交互运算
        self.Tempr = ItemValue(tempr, detemprate, tempr_range, tempr_breaks)    #温度, Planet类基本属性之一(feature), 用于归类Planet, 以及进行交互运算
        #self.mass = mass                                                        #旧版质量
    
    def categorize(self):
        return self.Mass.categorize(), self.Tempr.categorize() 
    
    def get_energy(self):
        return self.Mass.value * self.Tempr.value 
    
    def reset(self, mass = None, tempr = None, detempr = None):
        #重设参数
        if tp.is_number(mass):
            self.Mass.update(value = mass) 
            self.update_size() 
        if tp.is_number(tempr):
            self.Tempr.update(value = tempr, devalue = detempr) 
        else:
            self.Tempr.update(value = self.Tempr.value, devalue = detempr) 
    
    def Ruins(self, KeepRotate = False):
        #尝试将实例变成损毁状态(贴图), 并停止参与item碰撞检测
        try:
            self.update_image(name = self.moveimage.name+'.Ruins') 
            if not KeepRotate:  self.update_rotate(angle=0,speed=0) 
            self.skip = True 
        except KeyError:    pass 
    
    def Hidden(self):
        #隐藏实例并停止参与item碰撞检测
        self.update_image(name = cr.default_empty) 
        self.skip = True 
    
    def update_size(self):
        #根据Mass大小设定item贴图大小
        location = self.moveimage.center 
        Itemlength = self.Mass.get_log_value(vol_min, vol_max) 
        self.moveimage.image = cr.IMAGES[self.moveimage.name].copy() 
        self.scale_to(size = (Itemlength, Itemlength)) 
        self.move_to(location = location, Center = True) 
    
    def update(self):
        tig.SurroundedItem.update(self) 
        self.Mass.update() 
        self.Tempr.update() 
    
    #<------------------------------------------------------------------------
    #|引力交互
    def interact_gravety(self, Item):
        #引力交互(仅计算)，返回作用在Item上的引力加速度, 不对Item运动状态作任何改变
        if isinstance(Item, tig.SurroundedItem):
            if tp.is_number(self.Mass.value):
                addspeedvector = tp.minus_location_tuple(self.moveimage.center, Item.moveimage.center, ) 
                return vector_gravety(mass = self.Mass.value, vector = addspeedvector) 
            
    def interact_accept_gravety(self, Item = None):
        """
        引力交互(被动), 暂时写在PlanetItem类里
        """
        if isinstance(Item, PlanetItem):
            self.add_speed(speed = Item.interact_gravety(self)) 
            #瞬时加速度只需要作用在speed上
    
    #<------------------------------------------------------------------------
    #|单方碰撞交互
    def interact_crash_direction(self, Item = None):
        #返回沿碰撞径向方向指向外侧的单位向量
        if not isinstance(Item, tig.SurroundedItem):
            return 
        
        vr = tp.minus_location_tuple(Item.moveimage.center, self.moveimage.center) 
        return tp.dot_tuple(vr, 1/tp.distance_location_tuple(vr, (0, 0))) 
    
    def interact_accept_crash(self, Object = None, rate = None):
        """碰撞反弹交互, 暂时写在Planet类里"""
        #当Object为tig.SurroundedItem时, 进行与该Item的碰撞交互  当Object为Rect时, 进行与该Rect边界的碰撞交互  若非上述两种情况, 则进行与窗口边界的碰撞交互
        if isinstance(Object, tig.SurroundedItem):
            r = Object.interact_crash_direction(self) if is_touch_round_item(self, Object) else (0, 0)  #计算碰撞点径向方向向量,并单位化.
        else:
            r = get_bound_direction(self, Object) if is_touch_bound(self, Object) else (0, 0)
        
        if r[0] == 0 and r[1] == 0:                                     #排除径向向量不存在的情况(即为0)
            return 
        
        speed = tp.dot_tuple(self.move.speed.location, cr.FPS)          #提取原始速度, 从move里提取速度信息时记得乘回FPS
        speed = vector_reflect(speed, r, rate)                          #计算原始速度在径向上的分解速度大小与径向向量长度之比(已包括碰撞后反向)
            
        self.update_speed(speed = speed)                                #赋予处理后的合成速度
        
        try:
            while is_touch_round_item(self, Object):                    #将碰撞状态消除
                self.add_speed(location = r)                            #此处若改为减去vr, 则会产生穿透Item的效果
        except AttributeError:
            while is_touch_bound(self, Object):
                self.add_speed(location = r) 
    
    def interact_give_crash(self, Object = None, rate = None):
        """碰撞反弹交互, 暂时写在Planet类里"""
        #interact_accept_crash的相反版本, 给予Object碰撞交互
        try:
            Object.interact_accept_crash(Object=self, rate = rate) 
        except AttributeError:  pass 
    
    #<------------------------------------------------------------------------
    #|双方碰撞交互
    def interact_both_crash(self, Object = None, rate = None):
        """碰撞反弹交互, 暂时写在Planet类里"""
        if not isinstance(Object, PlanetItem):
            return 
        if not (is_touch_round_item(self, Object) and tp.is_number(self.Mass.value) and tp.is_number(Object.Mass.value)):
            return 
        
        r = Object.interact_crash_direction(self) 
        vr_S, va_S = vector_disassemble(tp.dot_tuple(self.move.speed.location, cr.FPS), r) 
        vr_O, va_O = vector_disassemble(tp.dot_tuple(Object.move.speed.location, cr.FPS), r) 
        
        v_S, v_O = vector_crash(vr_S, vr_O, m1 = self.Mass.value, m2 = Object.Mass.value, rate = rate) 
        self.update_speed(speed = v_S) 
        Object.update_speed(speed = v_O) 
        
        while is_touch_round_item(self, Object):                                #将碰撞状态消除
            self.add_speed(location = r)                                        #此处若改为减去vr, 则会产生穿透Item的效果