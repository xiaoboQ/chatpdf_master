"""
命令模式-生成器模式
该文件用于命令模式的实现方便对于应用增加更多的功能，实现了ocp原则
"""
from abc import ABC

from pypdf import PypdfAbstract
import abc


class Command(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def executeCommand(self):
        pass

    @abc.abstractmethod
    def undoCommand(self):
        pass


class Controller:
    def __init__(self, command: Command):
        self.command = command

    def setCommand(self, command):
        self.command = command

    def executeCommand(self):
        return self.command.executeCommand()

    def undoCommand(self):
        return self.command.undoCommand()


class ChatSingleCommand(Command):
    def __init__(self):
        # 这里可以直接使用多态来对此进行初始化
        self.pypdf = None
        self.sourceId = ""
        self.content = ""

    # 用于构建生成器模式
    def setPypdf(self, pypdf):
        # 这里可以直接使用多态来对此进行初始化
        self.pypdf = pypdf
        return self

    def setSourceId(self, sourceId: str):
        self.sourceId = sourceId
        return self

    def setContent(self, content: str):
        self.content = content
        return self

    def executeCommand(self):
        whetherSuccess, answer = self.pypdf.chatSinglePDF(sourceId=self.sourceId, content=self.content)
        if whetherSuccess:
            return answer
        else:
            return "对话失败请重试！"

    # chatSingle无法进行撤销操作，所以这里直接返回None
    def undoCommand(self):
        return None
