#__init__.py in Control
#Control下的文件可调用本地所有包, 仅被main.py调用 
#注意Control文件应包含main.py需要的一切操作, 使得main只需要调用Control
__all__ = ['Keybord', 'HeadIndexScreen', 'PlayScreen'] 