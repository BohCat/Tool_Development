#Preporation (Simple tools)
import numpy as np
#仅调用python第三方包

#<---------------------------------------------------------------------------->
#I. 小型功能函数，不依赖下方的类
def is_number(nu):
    return type(nu) in [int, float, np.float64] 

def is_numberizable(tu = None):
    """
    Test if all the inputted parameter contains are number value.
    """
    if tu == None:                  #排除None输入
        return False
    
    try:
        if type(tu) in [int, float, np.float64]:
            return True             #确认数值型输入
        
        for item in tu:
            if not is_number(item):
                return False        #排除非数值型输入
        return True                 #确认全部数值型输入
    except IndexError or ValueError or TypeError:
        return False                #排除无法被处理的输入

def is_location_tuple(tu = None):
    if type(tu) == tuple and len(tu) == 2 and is_numberizable(tu):
        return True 
    return False 

def add_location_tuple(tu = None, at = None):
    if is_location_tuple(tu) and is_location_tuple(at):
        return (tu[0]+at[0], tu[1]+at[1]) 

def minus_location_tuple(tu = None, mt = None):
    if is_location_tuple(tu) and is_location_tuple(mt):
        return (tu[0]-mt[0], tu[1]-mt[1]) 

def distance_location_tuple(tu = None, at = None):
    if is_location_tuple(tu) and is_location_tuple(at):
        return np.sqrt((tu[0]-at[0])**2+(tu[1]-at[1])**2)
    return 0 

def dot_tuple(tu = None, c = 1):
    if is_location_tuple(tu) and is_numberizable(c):
        if c == 1:
            return tu 
        return (c * tu[0], c * tu[1])