# chatpdf-master

## 一、简介

​	本项目是对chatpdf接口的更进一步的封装，能够完成基本的对于pdf的添加、删除、询问。你可以使用本项目提供的基本功能类在项目中完成快速与大语言模型的交互。



## 二、使用方式

### **1.最基本工具类的增、删、询问。**

​	基本工具类不提供数据记录功能，所以需要手动记录自己apikey下各个pdf文件所对应的soureId并且在调用询问的方法时手动的传入。同理在删除pdf文件的时候也需要手动指定相应pdf的sourceId信息。

​	基本工具类采用了单例模式进行设计所以使用环境应当避免在高并发环境下频繁切换声明实例以及修改类中apiKey字段。

```python
from pypdf import Pypdf

pypdf = Pypdf(apiKey="xxxx")
content = "***详细描述一下元素扩散的优先级？"

# 添加pdf文件
whetherSuccess, sourceId = pypdf.addPDF(PDFPath="xx/xx/xx.pdf")

# 单个问题询问指定pdf
whetherSuccess, answer = pypdf.chatSinglePDF(sourceId="src_pWUaBip0D1mfU9UMbOyRi", content=content)

# 删除单个pdf文件
# 该函数能够一次删除多篇pdf文件所以请传入一个pdf的sourceId列表
whetherSuccess = pypdf.deletePDF(sourceIds=[sourceId])
```

​	以上代码段介绍的是基本工具类的最基本使用，接下来介绍基本工具类提供的两种特殊的与大语言模型交互的函数。

**单个问题询问全体pdf**

```python
from pypdf import Pypdf, PDF

pypdf = Pypdf(apiKey="xxxx")
contents = ["请介绍一下本文的摘要", "本文有没有提到过一些实验方法"]

# 添加需要询问的pdf文件
pdfs = []
pdfs.append(PDF(pdf_name="A Surrogate Modeling and Adaptive Sampling", source_id="src_yVaa6bErIdzSNir6M6MyE"))
pdfs.append(PDF(pdf_name="Hierarchical Attention Networks for Document Classification", source_id="src_s2X6L2TdU0R9XsPkotrJB"))
# 单个问题询问所选的全部pdf文件
whetherSuccess, data = pypdf.singleQuestionChatAllPDF(content=contents[0], pdfs=pdfs)
print(data)

"""
输出结果：
[{'answer': '本文介绍了一个成熟、灵活和自适应的机器学习工具包，用于回归建模和主动学习，以解决计算科学/工程中的代理建模问题。该工具包汇集了数据拟合、模型选择、样本选择（主动学习）、超参数优化和分布式计算算法，旨在使领域专家能够高效地生成准确的模型。该工具包可用于任何需要便宜、准确的近似模型来替代某些昂贵参考模型的领域。', 'pdf_name': 'A Surrogate Modeling and Adaptive Sampling'}, {'answer': '本文提出了一种新颖的文档分类方法，使用了分层结构和两个级别的注意机制，使模型能够关注重要内容并构建准确的文档表示。该方法在六个大规模文本分类任务上的实验证明，优于以前的方法。', 'pdf_name': 'Hierarchical Attention Networks for Document Classification'}]
"""
```

**多个问题询问全体pdf**

```python
from pypdf import Pypdf, PDF


pypdf = Pypdf(apiKey="xxxx")
contents = ["请介绍一下本文的摘要", "本文有没有提到过一些实验方法"]

# 添加pdf文件
pdfs = []
pdfs.append(PDF(pdf_name="A Surrogate Modeling and Adaptive Sampling", source_id="***"))
pdfs.append(PDF(pdf_name="Hierarchical Attention Networks for Document Classification", source_id="***"))
# 多个问题询问所选的全部pdf文件
whetherSuccess, data = pypdf.multipleQuestionChatAllPDF(contents=contents, pdfs=pdfs)
print(data)

"""
输出结果：
[{'pdf_name': 'A Surrogate Modeling and Adaptive Sampling', 'outcome': [{'content': '请介绍一下本文的摘要', 'answer': '本文介绍了一个成熟、灵活和自适应的机器学习工具包，用于回归建模和主动学习，以解决计算科学/工程中的代理建模问题。该工具包汇集了数据拟合、模型选择、样本选择（主动学习）、超参数优化和分布式计算算法，旨在使领域专家能够高效地生成准确的模型。该工具包可用于任何需要便宜、准确的近似模型来替代某些昂贵参考模型的领域。'}, {'content': '本文有没有提到过一些实验方法', 'answer': '是的，这篇文章提到了一些实验方法，包括有理函数、Kriging模型、人工神经网络（ANN）、样条和支持向量机（SVM）。这些方法用于构建全局逼近模型，以便预测系统性能并开发系统输入和输出之间的关系。'}]}, {'pdf_name': 'Hierarchical Attention Networks for Document Classification', 'outcome': [{'content': '请介绍一下本文的摘要', 'answer': '本文提出了一种新颖的文档分类方法，使用分层结构和两个级别的注意机制，能够关注重要内容并构建准确的文档表示。在六个大规模文本分类任务上进行的实验表明，该模型优于以前的方法。摘要没有具体提到实验结果，但提供了本文的主要贡献和方法。'}, {'content': '本文有没有提到过一些实验方法', 'answer': '是的，这篇论文提到了一些实验方法，比如使用了传统方法如线性方法、SVM和使用神经网络的段落嵌入、LSTM、基于单词的CNN、基于字符的CNN和Conv-GRNN、LSTM-GRNN等作为基线方法进行比较。'}]}]
"""
```



### 2.带有记录功能的工具类

​	带有记录功能的工具类实在基本工具类的基础上使用装饰器设计模式完成的。**其所有的函数功能都与基本的工具类使用方式一样。**唯一不同的地方体现在类的初始化的时候。

```python
from pypdf import Pypdf, PypdfRecoder

pypdf = Pypdf(apiKey="***")
# 这里需要初始化outputPath路径
# 你添加的pdf文件数据如pdf_name以及souce_id都会存储在该路径下
# 同时你询问的每一个对话数据也都会产生在该文件夹下
pdfRecoder = PypdfRecoder(pypdf=pypdf, outputPath="./output")
content = "请介绍一下本文的大致内容"
whetherSuccess, answer = pdfRecoder.chatSinglePDF(sourceId="***", content=content)
```

- 这里需要初始化outputPath路径
- 你添加的pdf文件数据如pdf_name以及souce_id都会存储在该路径下
- 你询问的每一个对话数据也都会产生在该文件夹下

​	**若你在别的项目中使用了该类且产生了存储数据，也可以直接把你之前的存储目录移动到当前目录下继续使用。**



## 三、命令模式以及管道过滤器模式

​	为了便于软件开发，本项目在pypdfControl.py以及pipline_filter.py文件中实现了命令模式以及管道过滤器模式。其用于将后端工具类与前端工具类充分解耦。

```python
from pypdf import Pypdf, PypdfRecoder, PDF
from pypdf.pypdfControl import ChatSingleCommand, Controller
from pypdf.pipeline_filter import PipelineFilter, filterKeyWords, filterPrompt

pypdf = Pypdf(apiKey="***")
content = "请介绍一下本文的大致内容"

piplineFilter = PipelineFilter().addFilters(filterKeyWords).addFilters(filterPrompt)
# 测试管道过滤器
content = piplineFilter.executeMode(content=content)
# 这里将内容进行了扩充，增加了提示词
print(f"question:{content}")

chatSingle = ChatSingleCommand()
.setPypdf(pypdf=pypdf)
.setSourceId(sourceId="***")
.setContent(content=content)
controller = Controller(command=chatSingle)  # 将命令交给对应的controller进行执行
# 命令模式-生成器模式测试
answer = controller.executeCommand
print(answer)
```

​	本项目的minichat文件夹下实现了一个很简单的前端案例用于测试该开发模式。