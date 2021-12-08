# Preparation for item
# 本文件中定义的是Item类中的各种属性，如位置、速度、加速度、旋转角度、质量和温度等
import numpy as np
import Config_Resource as cr
from py.Tools import Pre as tp
from py.Tools.Images.General import MoveImage
#除python第三方包外仅调用Tools层以及Config_Resource

"""
本文件中的数据结构：
Classes:
    MovePoint - 以tuple形式储存二元数字对（可为平面坐标或向量）, 提供简单向量运算
    MoveSpeed - 移动必需参数之集合: 速度、加速度, 更新函数
    MoveAngle - 旋转必需参数之集合: 角、角速度、角加速度、旋转中心、旋转半径, 更新、换算函数
    ItemValue - 用于记录Planet中质量与温度值的数据结构
"""

#<---------------------------------------------------------------------------->
#II. 小型自定义类, 含有可自定义的运算函数
class MovePoint():  #以tuple形式储存二元数字对（可为平面坐标或向量）, 提供简单向量运算
    #一个点可以在平面直角坐标系与角坐标系中表示
    #在平面直角坐标系中，一个点用一个二元Tuple（self.location)来表示(x,y)
    #在角坐标系中，一个点用长度（self.length)与角度(self.angle)两个变量共同表示。由于角的表示分角度制与弧度制，所以还要把弧度制(self.pi_angle)转化为角度制(self.angle)。
    """
    Data:
        self.location - Tuple - 中心点的坐标
        self.length - int|float - 作为向量时的二范数
        self.angle - int|float - location作为向量与x轴正方向的夹角（逆时针为正方向）- 使用角度制
        self.pi_angle - int|float -location作为向量与x轴正方向的夹角（逆时针为正方向）- 使用弧度制
        
    Methods：
        用于初始化：
        __init__
        set_from_coordinate - 根据平面坐标生成数据
        set_from_angle - 根据角坐标生成数据

        用于更改数据：
        add - 更新中心点的位置信息，接受两种类型的参数，一种是MovePoint类的对象，另一种是二元的Tuple直角坐标
        limit - 向本函数传递一个参数limit，判断目前物体的self.length是否超过了输入的limit，若超过，则对self.location与self.length进行处理。
        
        用于返回属性值：
        get_coordinate - 返回点的直角坐标，类型为二元Tuple型(x,y)
        get_angle - 返回点的角坐标，类型为三元Tuple型(self.length, self.angle, self.pi_angle)
        distance - 返回本对象与另一个点的距离，返回值是 int |float。本函数需要传入一个MovePoint类型的对象或是一个直角坐标Tuple。
        
        
        用于打印属性值：
        show - 打印出本对象的坐标、角度、长度等属性
        print_contains - 作用同show()函数
    
    """
    def __init__(self, center = None, x = None, y = None, angle = None, length = None, PiMode = False):
        if tp.is_location_tuple(center):
            self.set_from_coordinate(center) 
        elif tp.is_location_tuple((x, y)):
            self.set_from_coordinate((x, y)) 
        elif tp.is_numberizable(angle) and tp.is_numberizable(length):
            self.set_from_angle(angle = angle, length = length, PiMode = PiMode) 
        else:
            self.set_from_coordinate() 
    
    def print_contains(self):
        print(f"location = ({self.location[0]}, {self.location[1]}), length = {self.length}\ndirection = {self.angle} or {self.pi_angle} (pi-scale)")
            
    def set_from_coordinate(self, center = None):     #根据平面坐标生成数据
        if tp.is_location_tuple(center):
            self.location = center 
            self.length = self.distance((0, 0))  #计算作为向量时的二范数
        else:
            self.location = (0, 0) 
            self.length = 0 
        
        if self.location[0] == 0:       #计算location作为向量与x轴正方向的夹角（逆时针为正方向）
            self.pi_angle = -np.pi if self.location[1] > 0 else np.pi
        else:
            self.pi_angle = -np.arctan(self.location[1]/self.location[0]) 
        
        self.angle = self.pi_angle * 180 / np.pi 
        
    def set_from_angle(self, angle = 0, length = 0, PiMode = False):    #根据角坐标生成数据
        if tp.is_numberizable(angle):
            self.angle = angle * 180 / np.pi if PiMode else angle 
            self.pi_angle = angle if PiMode else angle * np.pi / 180 
        else:
            self.angle = self.pi_angle = 0 
        
        self.length = length if tp.is_numberizable(length) else 0 
        
        self.location = (self.length * np.cos(self.pi_angle), -self.length * np.sin(self.pi_angle)) 
    
    def get_coordinate(self):
        return self.location         
    
    def get_angle(self):
        return (self.length, self.angle, self.pi_angle) 
    
    def show(self):
        print(f"x = {self.location[0]}, y = {self.location[1]}\n angle = {self.angle} or {self.pi_angle} (pi-scale), length = {self.length}") 
        
    def add(self, mv):
        #接受MovePoint或者坐标tuple为输入
        if isinstance(mv, MovePoint):
            self.set_from_coordinate(center = (self.location[0] + mv.location[0], self.location[1] + mv.location[1])) 
        if tp.is_location_tuple(mv):
            self.set_from_coordinate(center = (self.location[0] + mv[0], self.location[1] + mv[1])) 
    
    def limit(self, limit):
        if tp.is_numberizable(limit) and self.length > 0:
            if self.length >limit:
                self.location = tp.dot_tuple(self.location, limit/self.length) 
                self.length = limit 
    
    def distance(self, np):
        #接受MovePoint或者坐标tuple为输入
        if isinstance(np, MovePoint):
            return self.tp.distance_location_tuple(self.location, np.location) 
        return tp.distance_location_tuple(self.location, np) 

class MoveSpeed():  #本类包含了点的移动所需要的参数与功能: 速度、加速度, 更新函数
    """
    Data:
        self.location - Items.Pre.MovePoint类的对象 - 若是平面直角坐标形式，在self.location.location存储一个二元Tuple；若为角坐标形式，在self.location.angle 和 self.location.length 中存储两个int或float类型的数字。
        self.speed - Items.Pre.MovePoint类的对象 - 若是平面直角坐标形式，在self.speed.loaction中存储一个二元Tuple；若为角坐标形式，在self.speed.angle 和 self.speed.length 中各存储一个int或float类型的数字。
        self.addspeed - Items.Pre.MovePoint类的对象 - 若是平面直角坐标形式，在self.addspeed.loaction中存储一个二元Tuple；若为角坐标形式，在self.addspeed.angle 和 self.addspeed.length 中各存储一个int或float类型的数字。
        self.maxspeed - int|float
        self.maxaddspeed - int|float

    Methods:
        用于初始化：
        __init__

        用于参数值：
        add_speed - 更改self.location、self.speed和self.addspeed的值。注意传入的参数是二元Tuple类型。
        update_speed - 用于更新self.speed与self.location，并对超过合理范围的self.speed进行处理。
        update_speed_limit - 用于更新self.maxspeed与self.maxaddspeed的值。注意传入的参数是int或float类型的数字。

        用于打印参数值：
        print_contains
    """
    def __init__(self, location = (0, 0), speed = (0, 0), addspeed = (0, 0), MaxSpeed = None, MaxAddSpeed = None, AngleMode = False, PiMode = False):
        """
        数据的存储可以有平面直角坐标或者角坐标两种形式。使用AngleMode这一参数来标注以何种形式存储数据。
        AngleMode: False - speed & addspeed represent the flat coordinate (x, y)
        AngleMode: True - speed & addspeed represect the angle coordinate (angle, length)
        使用角坐标形式存储数据时，角度可以用角度制或弧度制表示，为了防止出现差错，若角度使用弧度制表示，使用PiMode这一参数标注。
        PiMode: False - accept angle with normal-scale
        PiMode: True - accept angle with pi-scale
        """
        #注意，长度参数应除以FPS
        if AngleMode:
            self.location = MovePoint(angle = location[0], length = speed[1], PiMode = PiMode) if tp.is_location_tuple(location) else MovePoint() 
            self.speed = MovePoint(angle = speed[0], length = speed[1] / cr.FPS, PiMode = PiMode) if tp.is_location_tuple(speed) else MovePoint() 
            self.addspeed = MovePoint(angle = addspeed[0], length = addspeed[1] / cr.FPS, PiMode = PiMode) if tp.is_location_tuple(addspeed) else MovePoint() 
        else:
            self.location = MovePoint(center = location) if tp.is_location_tuple(location) else MovePoint() 
            self.speed = MovePoint(center = tp.dot_tuple(speed,1/cr.FPS)) if tp.is_location_tuple(speed) else MovePoint() 
            self.addspeed = MovePoint(center = tp.dot_tuple(addspeed,1/cr.FPS)) if tp.is_location_tuple(addspeed) else MovePoint() 
        
        self.maxspeed = MaxSpeed 
        self.maxaddspeed = MaxAddSpeed 
    
    def print_contains(self):
        print("location:")
        self.location.print_contains() 
        print("speed:")
        self.speed.print_contains() 
        print("addspeed:")
        self.addspeed.print_contains() 
    
    def update_speed_limit(self, MaxSpeed = None, MaxAddSpeed = None):
        self.maxspeed = MaxSpeed 
        self.maxaddspeed = MaxAddSpeed 
    
    def update_speed(self, location = None, speed = None, addspeed = None, MI = None, AngleMode = False, PiMode = False):
        if tp.is_location_tuple(addspeed):
            if AngleMode:
                self.addspeed.set_from_angle(angle = addspeed[0], length = addspeed[1]/cr.FPS, PiMode = PiMode)
            else:
                self.addspeed.set_from_coordinate(tp.dot_tuple(addspeed,1/cr.FPS)) 
        if type(self.maxaddspeed) in [int, float]:
            self.addspeed.limit(self.maxaddspeed) 
            
        if tp.is_location_tuple(speed):
            if AngleMode:
                self.speed.set_from_angle(angle = speed[0], length = speed[1]/cr.FPS, PiMode = PiMode) 
            else:
                self.speed.set_from_coordinate(tp.dot_tuple(speed,1/cr.FPS)) 
        else:
            self.speed.add(self.addspeed) 
        if type(self.maxspeed) in [int, float]:
            self.speed.limit(self.maxspeed) 
        
        if tp.is_location_tuple(location):
            if AngleMode:
                self.location.set_from_angle(angle = location[0], length = location[1], PiMode = PiMode) 
            else:
                self.location.set_from_coordinate(location) 
        else:
            self.location.add(self.speed) 
        
        if isinstance(MI, MoveImage):                       #rect.x, y只能为整数值，因此直接将速度叠加的话会产生显著的舍入误差，使得位移与速度不匹配, 因此只能另添加一对浮点数来储存位置值，并通过同步更新将浮点数与rect绑定
            MI.move_to(location = (round(self.location.location[0]), round(self.location.location[1])))
    
    def add_speed(self, location = None, speed = None, addspeed = None, MI = None):
        self.location.add(location) 
        self.speed.add(tp.dot_tuple(speed,1/cr.FPS)) 
        self.addspeed.add(tp.dot_tuple(addspeed,1/cr.FPS)) 
        
        if isinstance(MI, MoveImage):                       #rect.x, y只能为整数值，因此直接将速度叠加的话会产生显著的舍入误差，使得位移与速度不匹配, 因此只能另添加一对浮点数来储存位置值，并通过同步更新将浮点数与rect绑定
            MI.move_to(location = (round(self.location.location[0]), round(self.location.location[1])))

class MoveAngle():  #本类包含了物体旋转所需要的参数与功能: 角、角速度、角加速度、旋转中心、旋转半径, 更新、换算函数
    """
    Data:
    self.center - 二元Tuple - 旋转中心的坐标
    self.radius - int|float - 物体的半径
    self.angle - int|float 
    self.pi_angle - int|float
    self.speed - int|float - 注意是每帧的速度
    self.addspeed - int|float - 注意是每帧的加速度

    Methods:
        用于初始化：
        __init__
        reset

        用于更改参数值：
        update_radius - 用于更新旋转半径
        update_center - 用于更新旋转中心与旋转半径
        update_angle - 用于更新角速度等参数
        rotate_vector - 用于计算造成按参数旋转后image几何中心移动结果的等效向量. 原始几何中心规定在旋转中心正上方(-y方向)

        用于打印参数值：
        print_contains
    """
    
    def __init__(self, angle = 0, speed = 0, addspeed = 0, center = None, radius = None):
        self.reset(angle = angle, speed = speed, addspeed = addspeed, center = center, radius = radius) 
    
    def reset(self, angle = 0, speed = 0, addspeed = 0, center = None, radius = None):
        #重设参数
        self.angle = angle 
        self.pi_angle = self.angle * np.pi / 180 
        self.speed = speed / cr.FPS 
        self.addspeed = addspeed / cr.FPS 
        if tp.is_location_tuple(center):
            self.center = center 
            self.radius = abs(radius) if tp.is_numberizable(radius) else 1 
    
    def print_contains(self, ShowCenter = False):
        print(f"algle = {self.angle}, speed = {self.speed}, addspeed = {self.addspeed}") 
        if ShowCenter:
            print(f"center = ({self.center[0]}, {self.center[1]}), radius = {self.radius}") 
    
    def update_radius(self, radius = None):
        #更新旋转半径
        if tp.is_numberizable(radius):
            self.radius = abs(radius) 
    
    def update_center(self, center = None, radius = None):
        #更新旋转中心与旋转半径
        self.update_radius(radius) 
        if tp.is_location_tuple(center):
            self.center = center 
    
    def update_angle(self, angle = None, speed = None, addspeed = None):
        #更新角速度等参数
        if tp.is_number(addspeed):
            self.addspeed = addspeed / cr.FPS 
            
        if tp.is_number(speed):
            self.speed = speed / cr.FPS 
        else:
            self.speed += self.addspeed 
        
        if tp.is_number(angle):
            self.angle = angle 
        else:
            self.angle += self.speed 
            while self.angle>180:
                self.angle-=360 
            while self.angle<-180:
                self.angle+=360 
            self.pi_angle = self.angle * np.pi / 180 
    
    def rotate_vector(self):
        """
        Calculate the equivalent vector that the geometrical center of the image should move in a rotation.
        The original geom-center is directly above the rotation center (-y direction).
        """
        #计算造成按参数旋转后image几何中心移动结果的等效向量. 原始几何中心规定在旋转中心正上方(-y方向)
        try:
            return (round(-self.radius * np.sin(self.pi_angle)), round(self.radius * (1 - np.cos(self.pi_angle))))
        except AttributeError:
            return (0, 0)

class ItemValue():  #用于记录Planet中质量与温度值的数据结构

    def __init__(self, value = None, devalue = None, bound = None, cate_break = None):
        #value为存储数值
        #devalue为update时value的变化值
        #bound为value边界, 取None时意味无上/下界, 否则其中的值应按升序排列
        #cate_break为对value作分类时的临界值, 其中的值应按升序排列
        self.value = value if tp.is_number(value) else 0 
        self.devalue = devalue/cr.FPS if tp.is_number(devalue) else 0 
        self.bound = bound if tp.is_location_tuple(bound) else (None, None) 
        self.cate_break = cate_break if tp.is_numberizable(cate_break) else None 
    
    def __repr__(self):
        return f"Value = {self.value}, Devalue = {self.devalue}\nBound = {self.bound}\nBreaks = {self.cate_break}"
    
    def add(self, value = None, devalue = None):
        if tp.is_number(value):
            self.value += value 
        if tp.is_number(devalue):
            self.devalue += devalue/cr.FPS 
        
        self.bound_value() 
    
    def bound_value(self):
        if tp.is_location_tuple(self.bound):
            if self.value < self.bound[0]:
                self.value = self.bound[0] 
            if self.value > self.bound[1]:
                self.value = self.bound[1] 
    
    def categorize(self):
        try:
            iter(self.cate_break) 
        except TypeError:   return 
        for i in range(len(self.cate_break)):
            if self.value <= self.cate_break[i]:    return i 
        return len(self.cate_break) 
    
    
    def draw(self,SCREEN, location = None, col = None):
        #在界面上可视化显示数据
        #self.value的大小决定了显示的样貌
        """
        ......
        """
        pass 
    
    def get_log_value(self, y_min, y_max):
        #建立函数模型y= a * log10(x+1) + c, 取x = self.value, 返回对应的y值
        #注意, 输入的y_min, y_max分别为函数在x = 0 与x = self.bound[1]处的取值
        if not tp.is_numberizable((y_min, y_max, self.value)) or self.value < 0:
            return 
        if not tp.is_number(self.bound[1]):
            return (y_min + y_max)/2 
        
        a = (y_max - y_min)/np.log10(self.bound[1] + 1) 
        return a * np.log10(self.value + 1) + y_min 
    
    def get_qmodel_value(self, c):
        #建立函数模型y= - a * x^2 + c, 取x = self.value, 返回对应的y值
        #注意, 输入参数c 即为函数参数c, 并规定函数在self.bound上界处取0(若上界存在)
        if not tp.is_location_tuple((c, self.value)):
            return 
        if not tp.is_number(self.bound[1]):
            return c 
        
        a = c / self.bound[1] ** 2 
        return - a * self.value ** 2 + c 
    
    def get_lmodel_value(self, c):
        #建立函数模型y= - a * log10(x+1) + c, 取x = self.value, 返回对应的y值
        #注意, 输入参数c 即为函数参数c, 并规定函数在self.bound上界处取0(若上界存在)
        if not tp.is_location_tuple((c, self.value)) or self.value < 0:
            return 
        if not tp.is_number(self.bound[1]) or self.bound[1] <= 1:
            return c 
        
        a = c/np.log10(self.bound[1] + 1) 
        return - a * np.log10(self.value + 1) + c 
    
    def get_qlmodel_value(self,c):
        #建立函数模型y= - a * (log10(x+1))^2 + c, 取x = self.value, 返回对应的y值
        #注意, 输入参数c 即为函数参数c, 并规定函数在self.bound上界处取0(若上界存在)
        if not tp.is_location_tuple((c, self.value)) or self.value < 0:
            return 
        if not tp.is_number(self.bound[1]) or self.bound[1] <= 1:
            return c 
        
        a = c/np.log10(self.bound[1] + 1) ** 2 
        return - a * np.log10(self.value + 1) ** 2 + c 
        
    """
    def get......
    """
    
    def update(self, value = None, devalue = None):
        if tp.is_number(devalue):
            self.devalue = devalue/cr.FPS 
        
        if tp.is_number(value):
            self.value = value 
        else:
            self.value += self.devalue 
        
        self.bound_value() 
        
        