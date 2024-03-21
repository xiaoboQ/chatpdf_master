import requests
import os
import json
import uuid
import time

"""工具函数"""


def processTime(time: str):
    """
    该函数用于获取当前时间的函数具体用法如下
    # 获取当前时间
    nowTime = str(time.strftime("%Y-%m-%d %A %X", time.localtime()))
    # 将时间改成合理格式
    nowTime = processTime(nowTime)
    :param time: 经过time.strftime输出的时间结构
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


def getFileName(PDFPath: str):
    file = PDFPath.split('/')[-1]
    # 后缀名不是pdf
    if file.split('.')[-1] == "pdf":
        return file.split('.')[-2]
    else:
        raise Exception("文件需要为pdf文件")


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


def addPDF(apiKey: str, PDFPath: str):
    """
    向当前账号中添加PDF文件
    :param fileName: PDF文件的名称
    :param apiKey: 用于请求数据的key
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
        'x-api-key': apiKey
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
        file.close()
        return False, ""

    if response.status_code == 200:
        return True, str(response.json()['sourceId'])
    else:
        print('Status:', response.status_code)
        return False, ""


"""与chatpdf后端存储的pdf进行对话"""


def chatSinglePDF(apiKey: str, sourceId: str, content: str):
    """
    与单个PDF文件进行交互
    :param apiKey: 用于请求数据的key
    :param sourceId: 添加文件后产生的唯一Id可以在ChatPDF.json文件中查询
    :param content: 与LLM交互的提示词
    :return: 是否成功对话，大语言模型返回结果
    """
    headers = {
        'x-api-key': apiKey,
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
        return False, ""

    if response.status_code == 200:  # 成功访问
        return True, str(response.json()['content'])
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
        return False, ""


def singleQuestionChatAllPDF(api_Key: str, content: str, pdfs):
    """
    对本apiKey下的所有PDF进行全局对话
    若存在传入的输出路径则将结果存储再输出路径上
    :param pdfs: pdf数据类型存在source_id以及pdf_name的属性
    :param api_Key: 用于请求数据的key
    :param content: 与LLM交互的提示词
    :return: 是否成功输出， 对话数据
    """
    # 如果存在pdf信息则遍历pdf信息，并返回结果
    data = []
    # 循环向chatpdf后端请求数据
    for pdf in pdfs:
        source_id = pdf.source_id
        # 向chatpdf后端请求数据
        isSuccess, answer = chatSinglePDF(apiKey=api_Key, sourceId=source_id, content=content)

        if isSuccess:
            data.append({"answer": answer, "pdf_name": pdf.pdf_name})
        else:
            # 当前pdf处理请求时发生异常
            return False, None

    # 处理完所有pdf信息且没有发生异常
    return True, data


def multipleQuestionChatAllPDF(api_Key: str, contents: list, pdfs):
    """
    该函数用于多个问题与当前账号下的所有pdf进行对话并将信息输出到对应路径下
    注：该函数输出的的文件名为问题询问时的时间
    :param pdfs: pdf数据类型存在source_id以及pdf_name的属性
    :param api_Key: 用于请求数据的key
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
            isSuccess, answer = chatSinglePDF(apiKey=api_Key, sourceId=pdf.source_id, content=content)

            if isSuccess:
                data[pointer]["outcome"].append({"content": content, "answer": answer})
            else:
                # 当前pdf处理请求时发生异常
                return False, None
        pointer += 1

    # 处理完所有pdf信息且没有发生异常
    return True, data


"""删除chatpdf后端pdf的函数"""


def deletePDF(apiKey: str, sourceIds: list):
    """
    根据文件的sorceIds删除对应的PDF文件数据
    :param apiKey: 用于请求数据的key
    :param sourceIds: 添加文件后产生的唯一Id可以在ChatPDF.json文件中查询
    :return: 是否成功删除当前PDF文件
    """
    headers = {
        'x-api-key': apiKey,
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
        print('Error:', error)
        return False


def deleteAllPDF(apiKey: str, pdfs: list):
    """
    删除chatpdf后端中当前apiKey中的所有pdf数据
    :param apiKey: 用于请求数据的key
    :param pdfs: 当前apiKey下的所有pdf数据
    :return: 是否成功删除
    """

    sourceIds = []

    for pdf in pdfs:
        sourceIds.append(pdf.source_id)

    isSuccess = deletePDF(apiKey=apiKey, sourceIds=sourceIds)

    return isSuccess


