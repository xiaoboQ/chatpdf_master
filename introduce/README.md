## 问题



## 功能概述

​		项目对chatPDF接口进行了封装，完成了对于apiKey下的**PDF增加**、**删除**、**单个PDF对话**以及**全体PDF对话**的功能。封装的主要函数在API文件中，下面逐一介绍函数功能：

​		

### 一、增加PDF

函数：

```python
addPDF(apiKey: str, PDFPath: str):
	"""
	向当前账号中添加PDF文件
	:param apiKey: 用于请求数据的key
	:param PDFPath: 本机存储PDF的路径
	:return: 是否成功添加PDF文件
	"""
```

作用：向当前apiKey中添加PDF文件，添加完成后会在根目录下生成ChatPDF.json的文件名与sourceId映射文件。

示例：

```python
# 增加PDF文件
addPDF("sec_IB4utx616TgY5AAW8cupSsXgOTIre4oa", "./pdf/ImageNet Classification with Deep Convolutional Neural Networks.pdf")
```



### 二、删除PDF

函数：

```python
def deletePDF(apiKey: str, sourceId: str):
    """
    根据文件的sorceId删除对应的PDF文件数据
    :param apiKey: 用于请求数据的key
    :param sourceId: 添加文件后产生的唯一Id可以在ChatPDF.json文件中查询
    :return: 是否成功删除当前PDF文件
    """
```

作用：删除当前apiKey中的PDF文件，删除完成后会修改根目录下ChatPDF.json的文件中的对应条目。

示例：

```python
# 删除PDF文件
deletePDF("sec_IB4utx616TgY5AAW8cupSsXgOTIre4oa", "src_eHNPuLb3TLpjQJhyj8B1m")
```



### 三、单个PDF对话

函数：

```python
def chatSinglePDF(apiKey: str, sourceId: str, content: str):
    """
    与单个PDF文件进行交互
    :param apiKey: 用于请求数据的key
    :param sourceId: 添加文件后产生的唯一Id可以在ChatPDF.json文件中查询
    :param content: 与LLM交互的提示词
    :return: 大语言模型返回结果
    """
```

作用：通过apikey与sourceId与选中的PDF对话

示例：

```python
# 与PDF文件交流
answer = chatSinglePDF("sec_IB4utx616TgY5AAW8cupSsXgOTIre4oa", "src_t28L5WSHj3vWs9iDwVLRT", "请概括一下本文大致内容")
print(answer)
```



### 四、全体PDF对话

函数：

```python
def chatAllPDF(apiKey: str, content: str, outputPath=None):
    """
    对本apiKey下的所有PDF进行全局对话
    若存在传入的输出路径则将结果存储再输出路径上
    :param apiKey: 用于请求数据的key
    :param content: 与LLM交互的提示词
    :param outputPath: 结果输出路径，注意该路径只需要定位到文件夹即可，不需要定义对应的输出文件
    :return: 是否成功输出
    """
```

作用：通过apiKey，与当前apiKey下的所有PDF文件及进行对话。若对output参数进行赋值则将对应结果输出到相应的文件夹之下，若未赋值则不会保存结果。

示例：

```python
# 与全体PDF对话
chatAllPDF(apiKey="sec_IB4utx616TgY5AAW8cupSsXgOTIre4oa", content="请介绍一下本文大致信息", outputPath="./answer")
```



### 五、添加文件夹中PDF

```python
def AddFolderPDF(apiKey: str, folderPath: str):
    """
    向当前帐号添加整个文件夹下的所有PDF文件
    :param apiKey: 用于请求数据的key
    :param folderPath: PDF所在文件夹位置
    :return: 是否成功添加PDF
    """
```

作用：通过apiKey，将folderPath下的所有pdf添加到对应的账号当中。如果该函数添加PDF过程中有pdf添加失败，则后续的pdf也不会添加

示例：

```python
AddFolderPDF(apiKey="sec_IB4utx616TgY5AAW8cupSsXgOTIre4oa", folderPath="./KGPDF")
```



### 六、多个问题对话全体PDF
