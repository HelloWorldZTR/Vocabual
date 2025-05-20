from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QSizePolicy, QSpacerItem
import PyQt5.Qt as Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from qframelesswindow.webengine import FramelessWebEngineView
from qfluentwidgets import ElevatedCardWidget, ProgressRing, BodyLabel, ImageLabel, TitleLabel


import tempfile
import os
import datetime

class StaticsFrame(QFrame):
    def __init__(self, parent, unique_name):
        super().__init__(parent)
        self.setObjectName(unique_name)

        # 设置布局
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setLayout(QHBoxLayout())

        # Two Columns Layout
        self.leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()

        self.layout().addLayout(self.leftLayout)
        self.layout().addLayout(self.rightLayout)

        self.prog = ProgressRingCardWidget(self)
        self.calendar = CalendatChartCardWidget(self)
        self.leftLayout.addWidget(self.prog)
        self.leftLayout.addWidget(self.calendar)
        self.leftLayout.setStretch(0, 1)

        self.kline = KlineChartCardWidget(self)
        self.rightLayout.addWidget(self.kline)
        self.rightLayout.setStretch(0, 1)

        # 测试数据
        import random
        startDate = datetime.date(2023, 3, 1)
        endDate = datetime.date(2023, 3, 30)
        data = [((startDate + datetime.timedelta(days=i)).strftime("%Y-%m-%d"), random.randint(0, 100)) for i in range((endDate - startDate).days + 1)]
        self.setCalendarInfo(data, startDate, endDate)

        self.setInfo("小学英语", 114514, 111199)

        date = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        learned = [(date[i], random.randint(0, 100)) for i in range(7)]
        reviewed = [(date[i], random.randint(0, 100)) for i in range(7)]
        self.setKLineInfo(learned, reviewed)
    
    def setInfo(self, bookname:str, wordcount:int, learned:int):
        """
        设置信息栏
        wordcount 为总单词数量
        """
        self.prog.setInfo(bookname, wordcount, learned)

    def setCalendarInfo(self, data, beginDate, endDate):
        """
        设置日历图表信息
        data: 词汇量数据
        beginDate: 开始日期
        endDate: 结束日期
        """
        self.calendar.createChart(data, beginDate, endDate)

    def setKLineInfo(self, learned, reviewed):
        """
        设置K线图表信息
        learned: 学习数据
        reviewed: 复习数据
        """
        self.kline.createChart(learned, reviewed)


class ProgressRingCardWidget(ElevatedCardWidget):
    def __init__(self, parent=None, percentage = 0):
        super().__init__(parent)

        self.setLayout(QVBoxLayout())
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.layout().addLayout(self.row1)
        self.layout().addLayout(self.row2)

        self.header = TitleLabel(self)
        self.header.setText("统计信息")
        self.row1.addWidget(self.header)
        self.row1.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.hspacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.prog = ProgressRing(self)
        self.prog.setRange(0, 100)
        self.row2.addItem(self.hspacer)
        self.row2.addWidget(self.prog)
        self.row2.addItem(self.hspacer)

        class _InfoWidget(QWidget):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setLayout(QVBoxLayout())
                self.labelBookName = BodyLabel(self)
                self.labelWordCount = BodyLabel(self)
                self.layout().addWidget(self.labelBookName)
                self.layout().addWidget(self.labelWordCount)
                self.layout().setAlignment(Qt.Qt.AlignCenter)

        
        self.info = _InfoWidget(self)
        self.layout().addWidget(self.info)
        self.layout().addItem(self.hspacer)
        #Fill dummy Info
        # self.setInfo("小学英语", 114514, 111199)

    
    def setInfo(self, bookName, wordCount, wordLearned):
        percentage = int(wordLearned / wordCount * 100)
        self.info.labelBookName.setText(bookName)
        self.info.labelWordCount.setText(f'单词数量: {wordLearned}/{wordCount}')
        self.prog.setValue(percentage)
    
    


class CalendatChartCardWidget(ElevatedCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumHeight(300)

        self.setLayout(QHBoxLayout())
        self.webview = FramelessWebEngineView(self)
        self.webview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.image = ImageLabel(self)
        # self.image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.image.setScaledContents(True)
        # self.layout().addWidget(self.image)
        self.layout().addWidget(self.webview)

        self.tempFile = None
        self.tempImgFile = None
    

    
    def createChart(self, data, beginDate, endDate) -> str:
        """
        生成日历图表的HTML代码
        data: 词汇量数据
        beginDate: 开始日期
        endDate: 结束日期
        """
        pass
        from pyecharts.charts import Calendar
        from pyecharts import options as opts

        assert len(data) == (endDate - beginDate).days + 1, "数据长度与日期范围不匹配"

        # 临时文件
        if self.tempFile is not None:
            self.tempFile.close()
            os.remove(self.tempFile.name)
        
        self.tempFile = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
        tempFileName = self.tempFile.name

        # 绘制日历图表
        calendar = (
            Calendar(init_opts=opts.InitOpts(width="100%"))
            .add(
                "", data, calendar_opts=opts.CalendarOpts(range_=[
                    beginDate.strftime("%Y-%m-%d"),
                    endDate.strftime("%Y-%m-%d"),
                ])
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="单词量统计"),
                visualmap_opts=opts.VisualMapOpts(
                    max_=100,   
                    min_=0,
                    orient="horizontal",
                    is_piecewise=False,
                )
            )
        )
        calendar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        calendar.render(tempFileName)
        self.webview.setUrl(Qt.QUrl.fromLocalFile(tempFileName))

        # 注入样式表,隐藏滚动条
        self.webview.page().runJavaScript("""
            var style = document.createElement('style');
            style.type = 'text/css';
            style.innerHTML = 'html, body {margin: 0;padding: 0;overflow: hidden; }';
            document.head.appendChild(style);
        """)
        # self.webview.setZoomFactor(0.5)
        
        return tempFileName

    def __del__(self):
        if self.tempFile is not None:
            self.tempFile.close()
            os.remove(self.tempFile.name)
        

class KlineChartCardWidget(ElevatedCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(300, 300)

        self.setLayout(QHBoxLayout())
        self.webview = FramelessWebEngineView(self)
        self.webview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout().addWidget(self.webview)

        self.tempFile = None
    
    def createChart(self, learned, reviewed):
        """
        生成K线图表的HTML代码
        learned: 学习数据
        reviewed: 复习数据
        """
        from pyecharts.charts import Bar
        from pyecharts import options as opts
        from pyecharts.charts import Grid

        # 临时文件
        if self.tempFile is not None:
            self.tempFile.close()
            os.remove(self.tempFile.name)
        
        self.tempFile = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
        tempFileName = self.tempFile.name


        x_axis = []
        y_axis = []

        for x, y in learned:
            x_axis.append(x)
            y_axis.append(y)

        bar = (
            Bar(init_opts=opts.InitOpts(width="100px"))
            .add_xaxis(x_axis)
            .add_yaxis(y_axis=y_axis, series_name="新学单词")
            .set_global_opts(
                title_opts=opts.TitleOpts(title="学习情况"),
                xaxis_opts=opts.AxisOpts(type_="category"),
                yaxis_opts=opts.AxisOpts(type_="value"),
            )
        )
        
        x_axis2 = []
        y_axis2 = []
        for x,y in reviewed:
            x_axis2.append(x)
            y_axis2.append(y)
        
        bar2 = (
            Bar(init_opts=opts.InitOpts(width="100px"))
            .add_xaxis(x_axis2)
            .add_yaxis(y_axis=y_axis2, series_name="复习单词")
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(type_="category"),
                yaxis_opts=opts.AxisOpts(type_="value"),
            )
        )

        grid = (
            Grid()
            .add(bar, grid_opts=opts.GridOpts(pos_top="55%", width="300px"))
            .add(bar2, grid_opts=opts.GridOpts(pos_bottom="55%", width="300px"))
        )

        grid.render(tempFileName)
        self.webview.setUrl(Qt.QUrl.fromLocalFile(tempFileName))

        # 注入样式表,隐藏滚动条
        self.webview.page().runJavaScript("""
            var style = document.createElement('style');
            style.type = 'text/css';
            style.innerHTML = 'html, body {margin: 0;padding: 0;overflow: hidden;}';
            document.head.appendChild(style);
        """)
        # self.webview.setZoomFactor(0.5)
    
    def __del__(self):
        if self.tempFile is not None:
            self.tempFile.close()
            os.remove(self.tempFile.name)