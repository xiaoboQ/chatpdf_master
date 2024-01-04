"""
单例模式-装饰器模式
该文件用于基本的与chatpdf后端交互的逻辑的编写
主要的类有以下两个（均使用了单例模式）
Pypdf
    最基本的工具类，其父类为PypdfAbstract
    实现了最基本的增删改查的功能，但是没有将对云端的数据存储在本地的能力
PypdfRecoder
    工具类的装饰器，其父类为PypdfAbstract
    它在最基本的工具类之上增添了json本地api数据存储的功能如：source_id, pdf_name
    同时增加了将对话后的结果存储在本地的能力
"""

import requests
import logging
import datetime
import json
import abc
import os


class PDF:
    def __init__(self, pdf_name, source_id):
        """
        辅助工具类
        :param pdf_name: pdf的名称
        :param source_id: pdf对应的source_id信息
        """
        self.pdf_name = pdf_name
        self.source_id = source_id

    def setPdfName(self, pdf_name: str):
        self.pdf_name = pdf_name

    def getPdfName(self):
        return self.pdf_name

    def setSourceId(self, source_id):
        self.source_id = source_id

    def getSourceId(self):
        return self.source_id


class PypdfAbstract(metaclass=abc.ABCMeta):
    """
    工具类的抽象父类
    """

    @abc.abstractmethod
    def getApiKey(self):
        pass

    @abc.abstractmethod
    def setApiKey(self, apiKey):
        pass

    @abc.abstractmethod
    def addPDF(self, PDFPath: str):  # 增加一个pdf文件
        pass

    @abc.abstractmethod
    def chatSinglePDF(self, sourceId: str, content: str):  # 与单个pdf文件进行对话
        pass

    @abc.abstractmethod
    def deletePDF(self, sourceIds: list):  # 删除单个pdf
        pass

    @abc.abstractmethod
    def singleQuestionChatAllPDF(self, content: str, pdfs: list):
        pass

    @abc.abstractmethod
    def multipleQuestionChatAllPDF(self, contents: list, pdfs: list):
        pass


class Pypdf(PypdfAbstract):
    """
    工具类，用于与pdf交互
    """
    __instance = None  # 用于存储单例实例的变量

    def __init__(self, apiKey: str):
        self.apiKey = apiKey

    def __new__(cls, *args, **kwargs):
        """
        在创建示例的时候查看静态变量中是否存在值，若存在则返回对应实例
        若没有则创建对应的实例
        :param args:
        :param kwargs:
        """
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def getApiKey(self):
        return self.apiKey

    def setApiKey(self, apiKey):
        self.apiKey = apiKey

    @staticmethod
    def processTime(time: str):
        """
        该函数用于获取当前时间的函数具体用法如下
        # 将时间改成合理格式
        nowTime = processTime(nowTime)
        :param time: 输出的时间结构
        :return: 当前时间的字符串形式
        """
        temp = ""
        for index in range(len(time)):
            element = time[index]
            if not element == '-':
                if not element == ':':
                    temp += element
                else:
                    temp += ' '
            else:
                temp += ' '
        return temp

    @staticmethod
    def getFileName(PDFPath: str):
        file = PDFPath.split('/')[-1]
        # 后缀名不是pdf
        if file.split('.')[-1] == "pdf":
            return file.split('.')[-2]
        else:
            raise Exception("文件需要为pdf文件")

    @staticmethod
    def fitJudgment(allPdfs, sourceIds: list):
        """
        该函数用于判断sourceIds中的sourceId是否与pdfs中的sourceId适配
        :param allPdfs:
        :param sourceIds: pdf的sourceId列表
        :return: sourceIds中的sourceId是否与pdfs中的sourceId适配, sourceIds对应的pdf列表
        """
        pdfs = []
        for sourceId in sourceIds:
            # 设置访问标志
            flag = False
            for pdf in allPdfs:
                if pdf.source_id == sourceId and not flag:
                    pdfs.append(pdf)
                    flag = True
                    break
            # 当前sourceId再全体pdf数据中没有记录
            if not flag:
                return False, None
        return True, pdfs

    """向chatpdf后端添加pdf文件"""

    def addPDF(self, PDFPath: str):
        """
        向当前账号中添加PDF文件
        :param PDFPath: 本机存储PDF的路径
        :return: bool 是否成功添加PDF文件, source_id
        """

        # 请求参数
        file = open(PDFPath, 'rb')
        files = [
            ('file', ('file', file,
                      'application/octet-stream'))
        ]
        headers = {
            'x-api-key': self.apiKey
        }

        try:
            # 请求数据
            res = requests.session()
            response = requests.post(
                'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)
            # 成功发送则关闭文件
            file.close()
            res.keep_alive = False
        except requests.exceptions.ConnectionError:
            # 发生连接异常也需要关闭文件
            logging.warning("网络连接异常")
            file.close()
            return False, ""

        if response.status_code == 200:
            return True, str(response.json()['sourceId'])
        else:
            logging.warning(f"Status:{response.status_code}")
            return False, ""

    """与chatpdf后端存储的pdf进行对话"""

    def chatSinglePDF(self, sourceId: str, content: str):
        """
        与单个PDF文件进行交互
        :param sourceId: 添加文件后产生的唯一Id可以在ChatPDF.json文件中查询
        :param content: 与LLM交互的提示词
        :return: 是否成功对话，大语言模型返回结果
        """
        headers = {
            'x-api-key': self.apiKey,
            "Content-Type": "application/json",
        }

        data = {
            'sourceId': sourceId,
            'messages': [
                {
                    'role': "user",
                    'content': content,
                }
            ]
        }

        try:
            res = requests.session()

            response = requests.post(
                'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)
            res.keep_alive = False
        except requests.exceptions.RequestException:
            logging.warning("网络连接异常")
            return False, ""

        if response.status_code == 200:  # 成功访问
            return True, str(response.json()['content'])
        else:
            logging.warning(f"Status:{response.status_code}")
            logging.warning(f"Error:{response.text}")
            return False, ""

    def singleQuestionChatAllPDF(self, content: str, pdfs: list):
        """
        对本apiKey下的所有PDF进行全局对话
        若存在传入的输出路径则将结果存储再输出路径上
        :param pdfs: pdf数据类型存在source_id以及pdf_name的属性
        :param content: 与LLM交互的提示词
        :return: 是否成功输出， 对话数据
        """
        # 如果存在pdf信息则遍历pdf信息，并返回结果
        data = []
        # 循环向chatpdf后端请求数据
        for pdf in pdfs:
            source_id = pdf.source_id
            # 向chatpdf后端请求数据
            isSuccess, answer = self.chatSinglePDF(sourceId=source_id, content=content)

            if isSuccess:
                data.append({"answer": answer, "pdf_name": pdf.pdf_name})
            else:
                # 当前pdf处理请求时发生异常
                return False, None

        # 处理完所有pdf信息且没有发生异常
        return True, data

    def multipleQuestionChatAllPDF(self, contents: list, pdfs: list):
        """
        该函数用于多个问题与当前账号下的所有pdf进行对话并将信息输出到对应路径下
        注：该函数输出的的文件名为问题询问时的时间
        :param pdfs: pdf数据类型存在source_id以及pdf_name的属性
        :param contents: 与LLM交互的提示词列表
        :return: 是否成功进行对话， 对话数据
        """

        data = []
        # 记录当前pdf再data中的位置
        pointer = 0
        # 我们按照每篇pdf进行迭代
        for pdf in pdfs:
            data.append({"pdf_name": pdf.pdf_name, "outcome": []})
            for content in contents:
                # 向chatpdf后端请求数据
                isSuccess, answer = self.chatSinglePDF(sourceId=pdf.source_id, content=content)

                if isSuccess:
                    data[pointer]["outcome"].append({"content": content, "answer": answer})
                else:
                    # 当前pdf处理请求时发生异常
                    return False, None
            pointer += 1

        # 处理完所有pdf信息且没有发生异常
        return True, data

    """删除chatpdf后端pdf的函数"""

    def deletePDF(self, sourceIds: list):
        """
        根据文件的sourceIds删除对应的PDF文件数据
        :param sourceIds: 添加文件后产生的唯一Id可以在ChatPDF.json文件中查询
        :return: 是否成功删除当前PDF文件
        """
        headers = {
            'x-api-key': self.apiKey,
            'Content-Type': 'application/json',
        }

        data = {
            'sources': sourceIds,
        }

        res = requests.session()
        try:
            response = requests.post(
                'https://api.chatpdf.com/v1/sources/delete', json=data, headers=headers)
            response.raise_for_status()
            res.keep_alive = False
            return True
        except requests.exceptions.RequestException as error:
            logging.warning("网络连接异常")
            logging.warning(f"Error:{error}")
            return False


class PypdfRecoder(PypdfAbstract):
    """
    该类用于装饰器模式，通过装饰原有的PypdfAbstract完成在与pdf交互的同时能够在json中存储对应的数据
    """
    __instance = None  # 用于存储单例实例的变量

    def __init__(self, pypdf, outputPath=None):
        self.pypdf = pypdf
        # 如果用户输入recode的输出路径则在对应的位置输出，如果没有则默认在当前路径下
        if outputPath:
            self.outputPath = outputPath
        else:
            self.outputPath = ""

    def __new__(cls, *args, **kwargs):
        """
        在创建示例的时候查看静态变量中是否存在值，若存在则返回对应实例
        若没有则创建对应的实例
        :param args:
        :param kwargs:
        """
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def createRecoder(self):
        outputFile = os.path.join(self.outputPath, "Pypdf.json")
        if not os.path.exists(outputFile):
            # 声明存储用户数据的json文件
            data = {
                "x-api-key": self.pypdf.getApiKey(),
                "fileData": {}
            }
            with open(outputFile, 'w', encoding='utf-8') as f:
                json.dump(data, f)

    @staticmethod
    def getNowTime() -> str:
        now = datetime.datetime.now()
        formatted_time = now.strftime("%Y_%m_%d_%H_%M_%S")
        return formatted_time

    @staticmethod
    def saveData(data, outputFilePath):
        with open(outputFilePath, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def getFileName(PDFPath: str):
        file = PDFPath.split('/')[-1]
        # 后缀名不是pdf
        if file.split('.')[-1] == "pdf":
            return file.split('.')[-2]
        else:
            raise Exception("文件需要为pdf文件")

    def addPypdfData(self, fileName, sourceId):
        with open(os.path.join(self.outputPath, "Pypdf.json"), 'r') as f:
            data = json.load(f)
        if sourceId in data.values():  # 如果已经存在当前的sourceId信息则返回错误
            return False
        else:
            data[fileName] = sourceId

        with open(os.path.join(self.outputPath, "Pypdf.json"), 'w') as f:
            json.dump(data, f, indent=4)
        return True

    def deletePypdfData(self, sourceId):
        with open(os.path.join(self.outputPath, "Pypdf.json"), 'r') as f:
            data = json.load(f)
        if sourceId in data["fileData"].values():  # 如果查询高对应的sourceIds信息则进行删除
            data = {key: value for key, value in data["fileData"].items() if value != sourceId}
        else:
            return False

        with open(os.path.join(self.outputPath, "Pypdf.json"), 'w') as f:
            json.dump(data, f, indent=4)
        return True

    def getJsonData(self):
        with open(os.path.join(self.outputPath, "Pypdf.json"), 'r') as f:
            data = json.load(f)

        return data

    def getApiKey(self):
        return self.pypdf.getApiKey()

    def setApiKey(self, apiKey):
        self.pypdf.setApiKey(apiKey=apiKey)

    def addPDF(self, PDFPath: str):
        self.createRecoder()

        # 获得文件名并使用基础工具类传递pdf文件到后端
        fileName = self.getFileName(PDFPath=PDFPath)
        whetherSuccess, sourceId = self.pypdf.addPDF(PDFPath=PDFPath)

        if whetherSuccess:
            # 记录json数据
            whetherSuccess = self.addPypdfData(fileName=fileName, sourceId=sourceId)
            return True
        else:
            return False

    def chatSinglePDF(self, sourceId: str, content: str):
        # 基础工具类的功能
        whetherSuccess, answer = self.pypdf.chatSinglePDF(sourceId=sourceId, content=content)

        # 添加json保存结果的功能
        data = {
            "content": content,
            "answer": answer
        }
        self.saveData(data=data, outputFilePath=os.path.join(self.outputPath, self.getNowTime() + ".json"))
        return whetherSuccess, answer

    def singleQuestionChatAllPDF(self, content: str, pdfs: list):
        # 基础工具类的功能
        whetherSuccess, data = self.pypdf.singleQuestionChatAllPDF(content=content, pdfs=pdfs)

        # 添加json保存数据的功能
        self.saveData(data=data, outputFilePath=os.path.join(self.outputPath, self.getNowTime() + ".json"))
        return whetherSuccess, data

    def multipleQuestionChatAllPDF(self, contents: list, pdfs: list):
        # 基础工具类的功能
        whetherSuccess, data = self.pypdf.multipleQuestionChatAllPDF(contents=contents, pdfs=pdfs)

        # 添加json保存数据的功能
        self.saveData(data=data, outputFilePath=os.path.join(self.outputPath, self.getNowTime() + ".json"))
        return whetherSuccess, data

    def deletePDF(self, sourceIds: list):
        # 基础工具类的功能
        whetherSuccess = self.pypdf.deletePDF(sourceIds=sourceIds)

        if whetherSuccess:
            for sourceId in sourceIds:
                self.deletePypdfData(sourceId=sourceId)
        return whetherSuccess

