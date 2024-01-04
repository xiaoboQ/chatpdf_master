from pypdf import Pypdf, PypdfRecoder

# 填入apiKey信息
pypdf = Pypdf(apiKey="xxx")
pdfRecoder = PypdfRecoder(pypdf=pypdf, outputPath="./output")
content = "请介绍一下本文的内容，告诉我其中涉及到什么实验方法"

prompt = f"""
假设你是一位科研工作者，请你仔细阅读以下[]中的我所给出的任务，然后按照下面的分点给出的需求完成我所给出的任务。
1. 请使用使用中文回答我
2. 字数尽量不少于200字
3. 内容详细具体，且能够在原文中找到依据。同时在你给我的答案结尾处将对应的段落标注在()中，你所给出的段落标注应当为对应的页面数如：page 1、page 12等，而一定不能是T1，T2这种格式
task: [{content}]
"""

# 填入当前pdf对应的sourceId信息
whetherSuccess, answer = pdfRecoder.chatSinglePDF(sourceId="xxx", content=prompt)

print(answer)
