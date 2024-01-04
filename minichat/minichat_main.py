from PyQt5.QtWidgets import QApplication, QMainWindow
from minichat import Ui_MainWindow
from pypdf import Pypdf, PypdfRecoder
from pypdfControl import ChatSingleCommand, Controller
from pipeline_filter import PipelineFilter, filterKeyWords, filterPrompt
import sys


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 绑定命令
        self.post.clicked.connect(self.clickedPost)
        self.clear.clicked.connect(self.clickedClear)

        # 初始化对话模式
        self.pypdf = Pypdf(apiKey="sec_IB4utx616TgY5AAW8cupSsXgOTIre4oa")
        self.pdfRecoder = PypdfRecoder(pypdf=self.pypdf, outputPath="./output")
        self.piplineFilter = PipelineFilter().addFilters(filterKeyWords).addFilters(filterPrompt)
        self.chatSingle = ChatSingleCommand()\
            .setPypdf(pypdf=self.pypdf)\
            .setSourceId(sourceId="src_pWUaBip0D1mfU9UMbOyRi")
        # 还需要设置pdf以及内容再去绑定命令

        # 展示sourceId以及name
        pdfDatas = self.pdfRecoder.getJsonData()
        text = ""
        for pdfName in pdfDatas.keys():
            text += pdfName
            text += "\n"
            text += pdfDatas[pdfName]
            text += "\n\n"

        self.sourceName.setText(text)

    def clickedPost(self):
        # 设置询问pdf以及内容并绑定命令
        if not len(self.sourceId.text()) == 0:
            self.chatSingle.setSourceId(sourceId=self.sourceId.text())
        self.chatSingle.setContent(content=self.piplineFilter.executeMode(content=self.lineEdit.text()))
        controller = Controller(command=self.chatSingle)  # 将命令交给对应的controller进行执行
        answer = controller.executeCommand()

        # 增加text内容
        chatText = self.chat.text()
        chatText += "用户:\n"
        chatText += self.lineEdit.text()
        chatText += "\n"
        chatText += "机器人:\n"
        chatText += answer
        chatText += "\n\n"

        self.chat.setText(chatText)

        # 清空输入框
        self.lineEdit.setText("")

    def clickedClear(self):
        # 清空输入输入框
        self.chat.setText("")
        self.lineEdit.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())
