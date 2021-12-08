#Indicator
import pygame

class Indicator():
    #定义指令: 可被eval()处理的字符串
    #基本内置交互类, 含有基础的指令集操作
    #Command_ID 为自身记录的一个指令, 可被借由消息队列输出到上层
    #Commands中建议仅添加自限性指令(即只执行self层面的运算)
    """
    Data:
        ID - 
        commands - dict{key: str}
    Function:
        __init__
        __str__
        __len__
        add_command
        get_command
    """
    def __init__(self, Command_ID = None):
        self.Command_ID = Command_ID    #指令集ID
        self.Commands = {}      #指令映射表, 
    def __str__(self):
        return f"CommandID = {self.Command_ID}\nCommands_Key:\n{list(self.Commands)}\n"
    def __len__(self):
        return len(self.Commands) 
    
    def add_command(self, command_key, command):
        #给command指令表添加新表项, 无输入正确性检测, 因此使用时应确保输入的command为可执行数据的字符串, 即command = 'function(...)'而function(...)能被正常执行
        if type(command) == str:
            self.Commands[command_key] = command 
    
    def get_command(self, command_key):
        #根据输入的command_key执行对应的command (即function(...))
        #只有在指令链的尾部被继承时才需要针对性地编写错误处理
        try:
            if '.' not in command_key:  None + 1 
            command_key = command_key.split('.') 
            [self.get_command(command) for command in command_key] 
        except TypeError:
            eval(self.Commands[command_key])
    
    def return_cID(self):
        #将自身Command_ID借助pygame.USEREVENT传出
        #name, creater, value 规定为返回消息的必备字段, 有新需求时可以以此为模板修改返回消息的格式
        temp_event = pygame.event.Event(pygame.USEREVENT, name = 'default_command', creater = 'Indicator', value = self.Command_ID) 
        pygame.event.post(temp_event) 
    
    def return_newcID(self, newcID):
        #将输入的newcID借助pygame.USEREVENT传出, 可用于将内部值传递至外侧
        #name, creater, value 规定为返回消息的必备字段, 有新需求时可以以此为模板修改返回消息的格式
        temp_event = pygame.event.Event(pygame.USEREVENT, name = 'default_command', creater = 'Indicator', value = newcID) 
        pygame.event.post(temp_event) 
    
    def draw(self, SCREEN):
        pass 