class PipelineFilter:
    def __init__(self):
        self.filters = []

    def addFilters(self, filter):
        """
        向管道过滤器模式中增加过滤器模型
        :param filter: 过滤器函数
        :return:
        """
        self.filters.append(filter)
        return self

    def executeMode(self, content):
        """
        执行对应的管道过滤器模式
        :param content:
        :return:
        """
        for filter in self.filters:
            content = filter(content)
        return content


def filterKeyWords(content: str):
    """
    该过滤器是为了过滤语句中的敏感词汇
    :param content:
    :return:
    """
    keyWords = ["***", "不让说"]
    for keyWord in keyWords:
        content = content.replace(keyWord, "")
    return content


def filterPrompt(content: str):
    """
    该过滤器使用提示词工程为提示词增加更全面的提示词
    :param content:
    :return:
    """
    content = f"""请认真阅读以下[]中的信息，分析其中的含义并认真作答
    同时请务必遵守以下规则来完成你阅读到的任务
    1. 请使用中文来回答我的问题
    2. 回答的务必详细可靠能在对应的原文找到结果
    
    Text: [{content}]"""

    return content
