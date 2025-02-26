import re
import sys
import numpy as np
import pandas as pd
from PyQt5.QtCore import Qt
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime, time
import matplotlib.dates as mdates
import torch
from torch import nn
from d2l import torch as d2l
from d2l.torch import Accumulator
from PyQt5.QtGui import QPixmap, QPainter, QImage, QFont, QPalette, QColor, QIcon
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import (QApplication, QWidget, QGraphicsScene,
                             QGraphicsView, QTableWidgetItem, QTabBar,
                             QFileDialog, QGraphicsPixmapItem, QMessageBox,
                             QPushButton, QDialog, QVBoxLayout, QLabel, QHBoxLayout)
from PyQt5 import uic
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pyecharts.charts import HeatMap, Bar3D
from pyecharts import options as opts
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        # 加载qt-designer中设计的ui文件
        self.ui = uic.loadUi("./traffic1.0.ui")
        # 菜单下拉框
        self.actionlight = self.ui.actionlight
        self.actiondark = self.ui.actiondark
        self.actiongrey = self.ui.actiongrey
        self.actionbrown = self.ui.actionbrown
        self.actiondefault = self.ui.actiondefault
        self.actionintro = self.ui.actionintro
        self.actionversion = self.ui.actionversion
        self.actionexit = self.ui.actionexit
        # 左侧边栏
        self.video_btn = self.ui.video_btn
        self.chart2_btn = self.ui.chart2_btn
        self.dataset_btn = self.ui.dataset_btn
        self.d2l_btn = self.ui.d2l_btn
        self.chart1_btn = self.ui.chart1_btn
        self.single_btn = self.ui.single_btn
        self.all_btn = self.ui.all_btn
        # 全局展示
        self.all_enter_num = self.ui.all_enter_num
        self.all_road_num = self.ui.all_road_num
        # tab
        self.tabWidget = self.ui.tabWidget
        # tab1_video
        self.video = self.ui.video
        self.choose_video = self.ui.choose_video
        self.play_pause = self.ui.play_pause
        self.graph_road = self.ui.graph_road
        # tab2_dataset/xlsx
        self.enter_num = self.ui.enter_num
        self.road_num = self.ui.road_num
        self.row = self.ui.row
        self.col = self.ui.col
        self.all_car_num = self.ui.all_car_num
        self.xlsx = self.ui.xlsx
        self.selectxlsx_btn = self.ui.selectxlsx_btn
        # tab3_all
        self.hotmap = self.ui.hotmap
        self.bar3d = self.ui.bar3d
        self.combo3_1 = self.ui.combo3_1
        self.combo3_2 = self.ui.combo3_2
        # tab4_chart1
        self.small_hotmap = self.ui.small_hotmap
        self.small_bar3d = self.ui.small_bar3d
        # tab5_chart2
        self.chart3 = self.ui.chart3
        self.chart4 = self.ui.chart4
        self.chart5 = self.ui.chart5
        self.combo = self.ui.combo
        # tab6_single
        self.input = self.ui.input
        self.search_btn = self.ui.search_btn
        self.chart_speed = self.ui.chart_speed
        self.chart_location = self.ui.chart_location
        self.chart_curve = self.ui.chart_curve
        self.show_image = self.ui.show_image
        self.show_id = self.ui.show_id
        self.show_name = self.ui.show_name
        self.show_veh = self.ui.show_veh
        self.show_direction = self.ui.show_direction
        self.show_speed = self.ui.show_speed
        self.show_acc = self.ui.show_acc
        self.show_alltime = self.ui.show_alltime
        self.show_status = self.ui.show_status
        # tab7_deeplearn
        self.pytorch_btn = self.ui.pytorch_btn
        self.show_pytorch = self.ui.show_pytorch
        self.input_epoch = self.ui.input_epoch
        self.input_lr = self.ui.input_lr
        self.input_size = self.ui.input_size
        self.output_loss = self.ui.output_loss
        self.output_train_acc = self.ui.output_train_acc
        self.output_test_acc = self.ui.output_test_acc
        # 保存/导出按钮
        self.export1 = self.ui.export1
        self.export3_1 = self.ui.export3_1
        self.export3_2 = self.ui.export3_2
        self.export4_1 = self.ui.export4_1
        self.export4_2 = self.ui.export4_2
        self.export5_1 = self.ui.export5_1
        self.export5_2 = self.ui.export5_2
        self.export5_3 = self.ui.export5_3
        self.export6_1 = self.ui.export6_1
        self.export6_2 = self.ui.export6_2
        self.export6_3 = self.ui.export6_3
        self.export7 = self.ui.export7
        # 隐藏所有的Tab widget页面
        self.tabBar = self.tabWidget.findChild(QTabBar)
        self.tabBar.hide()
        # 默认打开首页
        self.tabWidget.setCurrentIndex(0)
        # 菜单下拉栏
        self.actionlight.triggered.connect(self.menu_white)
        self.actiondark.triggered.connect(self.menu_black)
        self.actiongrey.triggered.connect(self.menu_grey)
        self.actionbrown.triggered.connect(self.menu_brown)
        self.actiondefault.triggered.connect(self.menu_default)
        self.actionintro.triggered.connect(self.menu_intro)
        self.actionversion.triggered.connect(self.menu_version)
        self.actionexit.triggered.connect(self.myexit)
        # 左侧router按钮点击事件
        self.video_btn.clicked.connect(self.open1)
        self.dataset_btn.clicked.connect(self.open2)
        self.all_btn.clicked.connect(self.open3)
        self.chart1_btn.clicked.connect(self.open4)
        self.chart2_btn.clicked.connect(self.open5)
        self.single_btn.clicked.connect(self.open6)
        self.d2l_btn.clicked.connect(self.open7)
        # 其他按钮点击事件
        self.choose_video.clicked.connect(self.chooseVideo)
        self.play_pause.clicked.connect(self.playPause)
        self.selectxlsx_btn.clicked.connect(self.select_dataset)
        self.pytorch_btn.clicked.connect(self.showtorch)
        self.search_btn.clicked.connect(self.show_specific_data)
        self.combo.currentIndexChanged.connect(self.combo5_change)
        self.combo3_1.currentIndexChanged.connect(self.combo3_1_change)
        self.combo3_2.currentIndexChanged.connect(self.combo3_2_change)
        # 导出图片按钮的点击事件
        self.export1.clicked.connect(self.export_chart1)
        self.export3_1.clicked.connect(self.export_chart3_1)
        self.export3_2.clicked.connect(self.export_chart3_2)
        self.export4_1.clicked.connect(self.export_chart4_1)
        self.export4_2.clicked.connect(self.export_chart4_2)
        self.export5_1.clicked.connect(self.export_chart5_1)
        self.export5_2.clicked.connect(self.export_chart5_2)
        self.export5_3.clicked.connect(self.export_chart5_3)
        self.export6_1.clicked.connect(self.export_chart6_1)
        self.export6_2.clicked.connect(self.export_chart6_2)
        self.export6_3.clicked.connect(self.export_chart6_3)
        self.export7.clicked.connect(self.export_chart7)
        # tab_1 视频
        # 创建一个媒体播放器对象和一个视频窗口对象
        self.media_player = QMediaPlayer()
        # 将视频窗口设置为媒体播放器的显示窗口
        self.video = self.ui.video
        self.media_player.setVideoOutput(self.video)
        # 进度条
        self.media_player.durationChanged.connect(self.getDuration)
        self.media_player.positionChanged.connect(self.getPosition)
        self.ui.slider.sliderMoved.connect(self.updatePosition)
        print(self.ui.__dict__)
        # tab_2 数据集
        # 读取xlsx、csv文件
        print('正在读取数据，请稍等...')
        # 初始化为0，用作判断用户是否打开数据集
        self.df = 0
        # 预加载所需的所有数据表
        xlsx_1_1 = pd.ExcelFile('./data/1进口/1_1.xlsx')
        xlsx_1_2 = pd.ExcelFile('./data/1进口/1_2.xlsx')
        xlsx_1_3 = pd.ExcelFile('./data/1进口/1_3.xlsx')
        xlsx_1_4 = pd.ExcelFile('./data/1进口/1_4.xlsx')
        xlsx_1_5 = pd.ExcelFile('./data/1进口/1_5.xlsx')
        xlsx_2_1 = pd.ExcelFile('./data/2进口/2_1.xlsx')
        xlsx_2_4 = pd.ExcelFile('./data/2进口/2_4.xlsx')
        xlsx_3_1 = pd.ExcelFile('./data/3进口/3_1.xlsx')
        xlsx_3_5 = pd.ExcelFile('./data/3进口/3_5.xlsx')
        xlsx_4_1 = pd.ExcelFile('./data/4进口/4_1.xlsx')
        xlsx_4_2 = pd.ExcelFile('./data/4进口/4_2.xlsx')
        xlsx_4_3 = pd.ExcelFile('./data/4进口/4_3.xlsx')
        xlsx_4_4 = pd.ExcelFile('./data/4进口/4_4.xlsx')
        xlsx_1_6 = pd.ExcelFile('./data/行人电动车自行车/1_6.xlsx')
        xlsx_2_6 = pd.ExcelFile('./data/行人电动车自行车/2_6.xlsx')
        xlsx_3_6 = pd.ExcelFile('./data/行人电动车自行车/3_6.xlsx')
        xlsx_4_6 = pd.ExcelFile('./data/行人电动车自行车/4_6.xlsx')
        self.df1_1 = pd.read_excel(xlsx_1_1)
        self.df1_2 = pd.read_excel(xlsx_1_2)
        self.df1_3 = pd.read_excel(xlsx_1_3)
        self.df1_4 = pd.read_excel(xlsx_1_4)
        self.df1_5 = pd.read_excel(xlsx_1_5)
        self.df2_1 = pd.read_excel(xlsx_2_1)
        self.df2_4 = pd.read_excel(xlsx_2_4)
        self.df3_1 = pd.read_excel(xlsx_3_1)
        self.df3_5 = pd.read_excel(xlsx_3_5)
        self.df4_1 = pd.read_excel(xlsx_4_1)
        self.df4_2 = pd.read_excel(xlsx_4_2)
        self.df4_3 = pd.read_excel(xlsx_4_3)
        self.df4_4 = pd.read_excel(xlsx_4_4)
        self.df1_6 = pd.read_excel(xlsx_1_6)
        self.df2_6 = pd.read_excel(xlsx_2_6)
        self.df3_6 = pd.read_excel(xlsx_3_6)
        self.df4_6 = pd.read_excel(xlsx_4_6)
        # c1 = '../data/4进口/4_1.csv'
        # self.df4_1 = pd.read_csv(c1)
        # c2 = '../data/4进口/4_2.csv'
        # self.df4_2 = pd.read_csv(c2)
        # c3 = '../data/4进口/4_3.csv'
        # self.df4_3 = pd.read_csv(c3)
        # c4 = '../data/4进口/4_4.csv'
        # self.df4_4 = pd.read_csv(c4)
        print('读取成功！')
    def menu_white(self):
        print('light')
        stylesheet1 = f"QMainWindow{{background-color: rgb(250,250,250)}}"
        stylesheet2 = f"QWidget{{background-color: rgb(250,250,250)}}"
        self.ui.setStyleSheet(stylesheet1)
        self.ui.centralwidget.setStyleSheet(stylesheet2)
    def menu_black(self):
        print('dark')
        stylesheet1 = f"QMainWindow{{background-color: rgb(50,50,50)}}"
        stylesheet2 = f"QWidget{{background-color: rgb(50,50,50)}}"
        self.ui.setStyleSheet(stylesheet1)
        self.ui.centralwidget.setStyleSheet(stylesheet2)
    def menu_grey(self):
        print('grey')
        stylesheet1 = f"QMainWindow{{background-color: rgb(150,150,150)}}"
        stylesheet2 = f"QWidget{{background-color: rgb(150,150,150)}}"
        self.ui.setStyleSheet(stylesheet1)
        self.ui.centralwidget.setStyleSheet(stylesheet2)
    def menu_brown(self):
        print('brown')
        stylesheet1 = f"QMainWindow{{background-color: rgb(129,82,25)}}"
        stylesheet2 = f"QWidget{{background-color: rgb(129,82,25)}}"
        self.ui.setStyleSheet(stylesheet1)
        self.ui.centralwidget.setStyleSheet(stylesheet2)
    def menu_default(self):
        print('default')
        stylesheet1 = f"QMainWindow{{background-color: rgb(240,240,240)}}"
        stylesheet2 = f"QWidget{{background-color: rgb(240,240,240)}}"
        self.ui.setStyleSheet(stylesheet1)
        self.ui.centralwidget.setStyleSheet(stylesheet2)
    def menu_intro(self):
        print('intro')
        try:
            dialog = QDialog()
            dialog.setWindowTitle('introduction')
            dialog.setFixedSize(1000, 800)  # 设置对话框大小
            # 总体水平布局
            layout = QHBoxLayout(dialog)
            # 左侧的 QLabel，用于显示图片
            image_label = QLabel()
            pixmap = QPixmap('./traffic.png')  # 替换为您的图片路径
            pixmap = pixmap.scaled(300, 220)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(image_label)
            # 设置标题字体
            font = QFont()
            font.setPointSize(16)  # 设置字体大小
            font.setBold(True)  # 加粗
            # 右侧的 QVBoxLayout，用于显示文字
            text_layout = QVBoxLayout()
            label1 = QLabel("基于无信号交叉口")
            label1.setAlignment(Qt.AlignCenter)  # 居中对齐
            label1.setFont(font)
            label2 = QLabel("数据可视化动态分析")
            label2.setAlignment(Qt.AlignCenter)  # 居中对齐
            label2.setFont(font)
            label3 = QLabel("本软件致力于为交叉口数据进行可视化，")
            label3.setAlignment(Qt.AlignCenter)  # 居中对齐
            label4 = QLabel("为研究者直观展示数据分布情况，")
            label4.setAlignment(Qt.AlignCenter)  # 居中对齐
            label5 = QLabel("利于后续研究开展及效果演示。")
            label5.setAlignment(Qt.AlignCenter)  # 居中对齐
            text_layout.addSpacing(100)  # 设置间距为100
            text_layout.addWidget(label1)
            text_layout.addWidget(label2)
            text_layout.addSpacing(50)  # 设置间距为50
            text_layout.addWidget(label3)
            text_layout.addWidget(label4)
            text_layout.addWidget(label5)
            text_layout.addSpacing(100)  # 设置间距为100
            # 关闭按钮
            btn = QPushButton('关闭', dialog)
            btn.setFixedSize(150, 60)
            # 连接关闭信号
            btn.clicked.connect(dialog.close)
            text_layout.addWidget(btn, alignment=Qt.AlignCenter)
            layout.addLayout(text_layout)
            # 加载对话框图标
            dialog.setWindowIcon(QIcon("./data/car.jpg"))
            # 显示对话框，而不是一闪而过
            dialog.exec()
        except Exception as e:
            print(e)
    def menu_version(self):
        print('version')
        try:
            dialog = QDialog()
            dialog.setWindowTitle('version')
            dialog.setFixedSize(1000, 800)  # 设置对话框大小
            # 总体水平布局
            layout = QHBoxLayout(dialog)
            # 左侧的 QLabel，用于显示图片
            image_label = QLabel()
            pixmap = QPixmap('./traffic.png')  # 替换为您的图片路径
            pixmap = pixmap.scaled(300, 220)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(image_label)
            # 设置标题字体
            font = QFont()
            font.setPointSize(12)  # 设置字体大小
            font.setBold(True)  # 加粗
            # 设置主要文字字体
            font1 = QFont()
            font1.setPointSize(14)  # 设置字体大小
            font1.setBold(True)  # 加粗
            # 创建 QPalette 对象并设置文本颜色
            palette = QPalette()
            # 设置为蓝色
            palette.setColor(QPalette.WindowText, QColor(0, 200, 255))
            # 右侧的 QVBoxLayout，用于显示文字
            text_layout = QVBoxLayout()
            label1 = QLabel("基于无信号交叉口")
            label1.setAlignment(Qt.AlignCenter)  # 居中对齐
            label1.setFont(font)
            label2 = QLabel("数据可视化动态分析")
            label2.setAlignment(Qt.AlignCenter)  # 居中对齐
            label2.setFont(font)
            label3 = QLabel("版本:  1.0")
            label3.setAlignment(Qt.AlignCenter)  # 居中对齐
            label3.setFont(font)
            label3.setPalette(palette)
            label4 = QLabel("时间:  2024年01月28日")
            label4.setAlignment(Qt.AlignCenter)  # 居中对齐
            label4.setFont(font)
            label4.setPalette(palette)
            text_layout.addSpacing(100)  # 设置间距为10
            text_layout.addWidget(label1)
            text_layout.addWidget(label2)
            text_layout.addSpacing(50)  # 设置间距为10
            text_layout.addWidget(label3)
            text_layout.addWidget(label4)
            text_layout.addSpacing(100)  # 设置间距为10
            btn = QPushButton('关闭', dialog)
            btn.setFixedSize(150, 60)
            btn.clicked.connect(dialog.close)
            text_layout.addWidget(btn, alignment=Qt.AlignCenter)
            layout.addLayout(text_layout)
            # 加载对话框图标
            dialog.setWindowIcon(QIcon("./data/car.jpg"))
            # 显示对话框，而不是一闪而过
            dialog.exec()
        except Exception as e:
            print(e)
    def open1(self):
        try:
            subdf1_1 = self.df1_1[self.df1_1['target_id'] == 303]
            subdf1_2 = self.df1_2[self.df1_2['target_id'] == 127]
            subdf1_3 = self.df1_3[self.df1_3['target_id'] == 654]
            subdf1_4 = self.df1_4[self.df1_4['target_id'] == 816]
            subdf1_5 = self.df1_5[self.df1_5['target_id'] == 732]
            subdf2_1 = self.df2_1[self.df2_1['target_id'] == 18]
            subdf2_4 = self.df2_4[self.df2_4['target_id'] == 263]
            subdf3_1 = self.df3_1[self.df3_1['target_id'] == 343]
            subdf3_5 = self.df3_5[self.df3_5['target_id'] == 248]
            subdf4_1 = self.df4_1[self.df4_1['target_id'] == 494]
            subdf4_2 = self.df4_2[self.df4_2['target_id'] == 382]
            subdf4_3 = self.df4_3[self.df4_3['target_id'] == 14]
            subdf4_4 = self.df4_4[self.df4_4['target_id'] == 147]
            self.tabWidget.setCurrentIndex(0)
            self.figure1 = Figure(figsize=(8, 8))
            self.ax = self.figure1.add_subplot(111)
            self.canvas = FigureCanvas(self.figure1)
            self.ax.scatter(subdf1_1['x'], subdf1_1['y'], label='1_1', color="blue")
            self.ax.scatter(subdf1_2['x'], subdf1_2['y'], label='1_2', color="blue")
            self.ax.scatter(subdf1_3['x'], subdf1_3['y'], label='1_3', color="blue")
            self.ax.scatter(subdf1_4['x'], subdf1_4['y'], label='1_4', color="blue")
            self.ax.scatter(subdf1_5['x'], subdf1_5['y'], label='1_5', color="blue")
            self.ax.scatter(subdf2_1['x'], subdf2_1['y'], label='2_1', color="orange")
            self.ax.scatter(subdf2_4['x'], subdf2_4['y'], label='2_4', color="orange")
            self.ax.scatter(subdf3_1['x'], subdf3_1['y'], label='3_1', color="yellow")
            self.ax.scatter(subdf3_5['x'], subdf3_5['y'], label='3_5', color="yellow")
            self.ax.scatter(subdf4_1['x'], subdf4_1['y'], label='4_1', color="green")
            self.ax.scatter(subdf4_2['x'], subdf4_2['y'], label='4_2', color="green")
            self.ax.scatter(subdf4_3['x'], subdf4_3['y'], label='4_3', color="green")
            self.ax.scatter(subdf4_4['x'], subdf4_4['y'], label='4_4', color="green")
            self.ax.legend()
            self.canvas.draw()
            scene = QGraphicsScene(self)
            scene.addWidget(self.canvas)
            self.graph_road.setScene(scene)
        except Exception as e:
            print(e)
    def open2(self):
        self.tabWidget.setCurrentIndex(1)
    def open3(self):
        self.tabWidget.setCurrentIndex(2)
        try:
            # 垂直拼接多个 DataFrame（按行）
            combined_df = pd.concat(
                [self.df1_1, self.df1_2, self.df1_3, self.df1_4, self.df1_5, self.df2_1, self.df2_4,
                 self.df3_1, self.df3_5, self.df4_1, self.df4_2, self.df4_3, self.df4_4], axis=0)
            print("success1")
            data = pd.DataFrame(columns=['x', 'y'])
            data['x'] = combined_df['x']
            data['y'] = combined_df['y']
            list_x = [-40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60,
                      70, 80, 90, 100, 110, 120, 130, 140, 150, 160]
            list_y = [-200, -190, -180, -170, -160, -150, -140, -130,
                      -120, -110, -100, -90, -80, -70, -60,
                      -50, -40, -30, -20, -10, 0, 10, 20,
                      30, 40, 50, 60, 70, 80, 90, 100]
            res = np.zeros((20, 30))
            for index, row in combined_df.iterrows():
                # print(row['x'], row['y'])
                for i in range(20):
                    if list_x[i] <= row['x'] and row['x'] <= list_x[i + 1]:
                        for j in range(30):
                            if list_y[j] <= row['y'] and row['y'] <= list_y[j + 1]:
                                res[i][j] += 1
            x = ["-90", "-80", "-70", "-60", "-50", "-40", "-30", "-20", "-10", "0",
                 "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]
            y = ["-190", "-180", "-170", "-160", "-150", "-140", "-130", "-120",
                 "-110", "-100", "-90", "-80", "-70", "-60", "-50", "-40", "-30",
                 "-20", "-10", "0", "10", "20", "30", "40", "50", "60", "70",
                 "80", "90", "100"]
            data = [(i, j, res[i][j]) for i in range(20) for j in range(30)]
            # data = [[d[1], d[0], d[2]] for d in data]
            heatmap = (
                HeatMap(init_opts=opts.InitOpts(width="900px", height="750px"))
                .add_xaxis(x)
                .add_yaxis("", y, data)
                .set_global_opts(
                    title_opts=opts.TitleOpts("热力图"),
                    visualmap_opts=opts.VisualMapOpts(
                        max_=1000,
                        range_color=[
                            "#ffffff", "#ffffbf", "#fee090", "#fdae61",
                            "#f46d43", "#d73027", "#a50026"
                        ],
                    )
                )
            )
            bar3d = (
                Bar3D(init_opts=opts.InitOpts(width="800px", height="750px")).add(
                    series_name="",
                    data=data,
                    xaxis3d_opts=opts.Axis3DOpts(type_="category", data=x),
                    yaxis3d_opts=opts.Axis3DOpts(type_="category", data=y),
                    zaxis3d_opts=opts.Axis3DOpts(type_="value"),
                ).set_global_opts(
                    title_opts=opts.TitleOpts("3D柱状图"),
                    visualmap_opts=opts.VisualMapOpts(
                        max_=1000,
                        range_color=[
                            "#313695", "#4575b4", "#74add1", "#abd9e9",
                            "#e0f3f8", "#ffffbf", "#fee090", "#fdae61",
                            "#f46d43", "#d73027", "#a50026"
                        ],
                    )
                )
            )
            # 获取图表的HTML内容
            self.hotmap_html = heatmap.render_embed()
            self.bar3d_html = bar3d.render_embed()
            # 将图表的HTML内容加载到QWebEngineView中
            self.hotmap.setHtml(self.hotmap_html)
            self.bar3d.setHtml(self.bar3d_html)
        except Exception as e:
            print(e)
    def open4(self):
        self.tabWidget.setCurrentIndex(3)
        if type(self.df) == int:
            print("未加载数据表xlsx/csv")
            # 弹出提示框
            dialog = QMessageBox()
            dialog.setWindowTitle('warning')
            dialog.setIcon(QMessageBox.Warning)
            dialog.setText("请先选择数据集！")
            dialog.exec_()
            return
        try:
            # 单个 DataFrame
            combined_df = self.df
            print("success1")
            data = pd.DataFrame(columns=['x', 'y'])
            data['x'] = combined_df['x']
            data['y'] = combined_df['y']
            list_x = [-40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60,
                      70, 80, 90, 100, 110, 120, 130, 140, 150, 160]
            list_y = [-200, -190, -180, -170, -160, -150, -140, -130,
                      -120, -110, -100, -90, -80, -70, -60,
                      -50, -40, -30, -20, -10, 0, 10, 20, 30,
                      40, 50, 60, 70, 80, 90, 100]
            res = np.zeros((20, 30))
            for index, row in combined_df.iterrows():
                # print(row['x'], row['y'])
                for i in range(20):
                    if list_x[i] <= row['x'] and row['x'] <= list_x[i + 1]:
                        for j in range(30):
                            if list_y[j] <= row['y'] and row['y'] <= list_y[j + 1]:
                                res[i][j] += 1
            x = ["-90", "-80", "-70", "-60", "-50", "-40", "-30", "-20", "-10", "0",
                 "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]
            y = ["-190", "-180", "-170", "-160", "-150", "-140", "-130", "-120",
                 "-110", "-100", "-90", "-80", "-70", "-60", "-50", "-40", "-30",
                 "-20", "-10", "0", "10", "20", "30", "40", "50", "60", "70",
                 "80", "90", "100"]
            data = [(i, j, res[i][j]) for i in range(20) for j in range(30)]
            # data = [[d[1], d[0], d[2]] for d in data]
            heatmap = (
                HeatMap(init_opts=opts.InitOpts(width="900px", height="600px"))
                .add_xaxis(x)
                .add_yaxis("", y, data)
                .set_global_opts(
                    title_opts=opts.TitleOpts("车辆热力图"),
                    visualmap_opts=opts.VisualMapOpts(
                        max_=500,
                        range_color=[
                            "#ffffff", "#ffffbf", "#fee090", "#fdae61",
                            "#f46d43", "#d73027", "#a50026"
                        ],
                    )
                )
            )
            bar3d = (
                Bar3D(init_opts=opts.InitOpts(width="800px", height="600px")).add(
                    series_name="",
                    data=data,
                    xaxis3d_opts=opts.Axis3DOpts(type_="category", data=x),
                    yaxis3d_opts=opts.Axis3DOpts(type_="category", data=y),
                    zaxis3d_opts=opts.Axis3DOpts(type_="value"),
                ).set_global_opts(
                    title_opts=opts.TitleOpts("车辆3D柱状图"),
                    visualmap_opts=opts.VisualMapOpts(
                        max_=500,
                        range_color=[
                            "#313695", "#4575b4", "#74add1", "#abd9e9",
                            "#e0f3f8", "#ffffbf", "#fee090", "#fdae61",
                            "#f46d43", "#d73027", "#a50026"
                        ],
                    )
                )
            )
            # 获取图表的HTML内容
            self.small_hotmap_html = heatmap.render_embed()
            self.small_bar3d_html = bar3d.render_embed()
            # 将图表的HTML内容加载到QWebEngineView中
            self.small_hotmap.setHtml(self.small_hotmap_html)
            self.small_bar3d.setHtml(self.small_bar3d_html)
        except Exception as e:
            print(e)
    def open5(self):
        self.tabWidget.setCurrentIndex(4)
        if type(self.df) == int:
            print("未加载数据表xlsx/csv")
            # 弹出提示框
            dialog = QMessageBox()
            dialog.setWindowTitle('warning')
            dialog.setIcon(QMessageBox.Warning)
            dialog.setText("请先选择数据集！")
            dialog.exec_()
            return
        print(self.is_six)
        print(type(self.is_six))
        if self.is_six == '6':
            try:
                # 绘制chart3
                self.figure5_1 = Figure(figsize=(6, 4))
                self.myax3 = self.figure5_1.add_subplot(111)
                self.canvas = FigureCanvas(self.figure5_1)
                # 根据元素tag分类
                subset_r1 = self.df[self.df['target_tag'].str.contains('human')]
                subset_r2 = self.df[self.df['target_tag'].str.contains('bike')]
                subset_r3 = self.df[self.df['target_tag'].str.contains('ele_veh')]
                # 统计每个子集的数量
                count_r1 = subset_r1.shape[0]
                count_r2 = subset_r2.shape[0]
                count_r3 = subset_r3.shape[0]
                # 创建饼状图
                labels = ['human', 'bike', 'ele_veh']
                sizes = [count_r1, count_r2, count_r3]
                self.myax3.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
                               colors=['lightcoral', 'skyblue', 'lightgreen'])
                # 添加标题
                self.myax3.set_title('Distribution of Target Names (human, bike, ele_veh)')
                # 添加标签和标题
                self.canvas.draw()
                scene = QGraphicsScene(self)
                scene.addWidget(self.canvas)
                # 将 QGraphicsScene 设置到 QGraphicsView 中
                self.chart3.setScene(scene)
                # 绘制chart4
                self.figure5_2 = Figure(figsize=(6, 4))
                self.myax4 = self.figure5_2.add_subplot(111)
                self.canvas = FigureCanvas(self.figure5_2)
                # 计算每个类别（bike、human、ele_veh）的平均速度
                avg_speeds = self.df.groupby('target_tag')['speed'].mean()
                # 画出平均速度
                categories = avg_speeds.index
                average_speeds = avg_speeds.values
                self.myax4.bar(categories, average_speeds, color=['skyblue', 'lightgreen', 'lightcoral'])
                # 添加标签和标题
                self.myax4.set_xlabel('categories')
                self.myax4.set_ylabel('average_speed')
                self.myax4.set_title('average_speed of different categories')
                # 在每个柱子上方显示平均速度
                for i, speed in enumerate(average_speeds):
                    self.myax4.text(i, speed + 0.1, f'{speed:.2f}', ha='center', va='bottom')
                # 绘制柱状图
                self.canvas.draw()
                scene = QGraphicsScene(self)
                scene.addWidget(self.canvas)
                self.chart4.setScene(scene)
            except Exception as e:
                print(e)
        else:
            try:
                # 绘制chart3
                self.figure5_1 = Figure(figsize=(6, 4))
                self.myax3 = self.figure5_1.add_subplot(111)
                self.canvas = FigureCanvas(self.figure5_1)
                # 根据元素是否包含 "R1" 来过滤数据
                subset_r1 = self.df[self.df['target_name'].str.contains('R1')]
                subset_r2 = self.df[self.df['target_name'].str.contains('R2')]
                # 统计每个子集的数量
                count_r1 = subset_r1.shape[0]
                count_r2 = subset_r2.shape[0]
                # 创建饼状图
                labels = ['R1', 'R2']
                sizes = [count_r1, count_r2]
                # 绘制饼状图
                self.myax3.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
                               colors=['lightcoral', 'skyblue'])
                # 添加标题
                self.myax3.set_title('Distribution of Target Names (R1 and R2)')
                self.canvas.draw()
                scene = QGraphicsScene(self)
                scene.addWidget(self.canvas)
                # 将 QGraphicsScene 设置到 QGraphicsView 中
                self.chart3.setScene(scene)
                # 绘制chart4
                self.figure5_2 = Figure(figsize=(6, 4))
                self.myax4 = self.figure5_2.add_subplot(111)
                self.canvas = FigureCanvas(self.figure5_2)
                # 根据元素是否包含 "veh" 来过滤数据
                try:
                    subset_r1 = self.df[self.df['target_tag'] == 'veh']
                    subset_r2 = self.df[self.df['target_tag'] == 'bus']
                except Exception as e:
                    print(e)
                # 统计每个子集的数量
                count_r1 = subset_r1.shape[0]
                count_r2 = subset_r2.shape[0]
                # 绘制柱状图
                self.myax4.bar(['veh', 'bus'], [count_r1, count_r2], color=['lightcoral', 'orange'])
                # 在每个柱子上方添加数量标签
                for i, count in enumerate([count_r1, count_r2]):
                    self.myax4.text(i, count + 0.1, str(count), ha='center', va='bottom')
                # 添加标签和标题
                self.myax4.set_xlabel('Target Tag')
                self.myax4.set_ylabel('Count')
                self.myax4.set_title('Distribution of Target Tag(Veh / Bus)')
                self.canvas.draw()
                scene = QGraphicsScene(self)
                scene.addWidget(self.canvas)
                self.chart4.setScene(scene)
            except Exception as e:
                print(e)
        # 绘制chart5
        self.figure5_3 = Figure(figsize=(24, 6))
        self.myax5 = self.figure5_3.add_subplot(111)
        self.canvas = FigureCanvas(self.figure5_3)
        # 根据时间间隔进行分箱
        self.df['global_time'] = pd.to_datetime(self.df['global_time'])
        # self.df['global_time'] = pd.to_datetime(self.df['global_time'], format='%Y-%m-%d %H:%M:%S.%f')
        self.df['global_time'] = pd.to_datetime('2023-09-16 ' +
                                                self.df['global_time'].dt.strftime('%H:%M:%S'))
        # 获取当前日期
        # current_date = datetime.today().date()
        current_date = datetime.today().replace(year=2023, month=9, day=16).date()
        # 创建时间部分
        start_time = time(7, 54, 0)
        end_time = time(8, 24, 0)
        # 组合日期和时间
        start_time = datetime.combine(current_date, start_time)
        end_time = datetime.combine(current_date, end_time)
        filtered_data = self.df[(self.df['global_time'] >= start_time)
                                & (self.df['global_time'] <= end_time)]
        bins = pd.date_range(start=start_time, end=end_time, freq='2T')
        binned_data = pd.cut(filtered_data['global_time'], bins=bins)
        # 使用自定义坐标轴进行柱状图绘制
        counts = binned_data.value_counts().sort_index()
        self.myax5.bar(counts.index.astype(str), counts, color='lightgreen')
        # binned_data.value_counts().sort_index().plot(kind='bar', color='blue')
        # 添加标签和标题
        self.myax5.set_xlabel('time')
        # 设置 x 轴刻度标签的旋转角度
        self.myax5.set_xticklabels(counts.index.astype(str), rotation=7, ha='right')
        self.myax5.set_ylabel('number of cars')
        self.myax5.set_title('cars of different times')
        self.canvas.draw()
        scene = QGraphicsScene(self)
        scene.addWidget(self.canvas)
        self.chart5.setScene(scene)
    def open6(self):
        self.tabWidget.setCurrentIndex(5)
    def open7(self):
        self.tabWidget.setCurrentIndex(6)
    # tab1_btn事件
    # 选择视频
    def chooseVideo(self):
        try:
            self.media_player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))
            self.media_player.play()
        except Exception as e:
            print(e)
    # 播放/暂停
    def playPause(self):
        if self.media_player.state() == 1:
            self.media_player.pause()
        else:
            self.media_player.play()
    # 视频总时长获取
    def getDuration(self, d):
        '''d是获取到的视频总时长（ms）'''
        self.ui.slider.setRange(0, d)
        self.ui.slider.setEnabled(True)
        self.displayTime(d)
    # 视频实时位置获取
    def getPosition(self, p):
        self.ui.slider.setValue(p)
        self.displayTime(self.ui.slider.maximum() - p)
    # 显示剩余时间
    def displayTime(self, ms):
        minutes = int(ms / 60000)
        seconds = int((ms - minutes * 60000) / 1000)
        self.ui.time.setText('{}:{}'.format(minutes, seconds))
    # 用进度条更新视频位置
    def updatePosition(self, v):
        self.media_player.setPosition(v)
        self.displayTime(self.ui.slider.maximum() - v)
    # tab2_btn事件
    def select_dataset(self):
        # 打开文件对话框，选择要读取的文件
        file_path, _ = QFileDialog.getOpenFileName(None, '选择要读取的文件', '.',
                                                   'Excel Files (*.xlsx *.xls);;CSV Files (*.csv)')
        if file_path:
            if file_path.endswith('.xlsx'):
                print("正在读取 Excel 文件，请稍候...")
                xlsx_file = pd.ExcelFile(file_path)
                self.df = pd.read_excel(xlsx_file)
                print("读取成功！")
            elif file_path.endswith('.csv'):
                # 读取 csv 文件
                print("正在读取 CSV 文件，请稍候...")
                self.df = pd.read_csv(file_path)
                print("读取成功！")
            try:
                # 设置表格的行数和列数
                self.xlsx.setRowCount(self.df.shape[0])
                self.xlsx.setColumnCount(self.df.shape[1])
                # 设置列标签
                self.xlsx.setHorizontalHeaderLabels(self.df.columns.tolist())
                # 填充表格
                for i in range(self.df.shape[0]):
                    for j in range(self.df.shape[1]):
                        item = QTableWidgetItem(str(self.df.iloc[i, j]))
                        self.xlsx.setItem(i, j, item)
            except Exception as e:
                print("请输入有效的数字！", e)
        else:
            print('用户取消了数据集选择操作')
            return
        # 使用正则表达式提取_前后各一个字符，总共两个字符，作为进口方向和第几车道
        match = re.search(r'(.{1})_(.{1})', file_path)
        if match:
            before_char = match.group(1)
            after_char = match.group(2)
            print("前一个字符:", before_char)
            print("后一个字符:", after_char)
            self.is_six = after_char
            self.enter_num.setText(before_char)
            self.road_num.setText(after_char)
            self.all_enter_num.setText(before_char)
            self.all_road_num.setText(after_char)
        print(type(self.df.shape[0]))
        print(self.df.shape[1])
        print(self.df['target_id'].nunique())
        self.row.setText(str(self.df.shape[0]))
        self.col.setText(str(self.df.shape[1]))
        self.all_car_num.setText(str(self.df['target_id'].nunique()))
    # tab3
    def combo3_1_change(self, index):
        print(index)
        if index == 0:
            # 绘制汽车热力图
            try:
                # 垂直拼接多个 DataFrame（按行）
                combined_df = pd.concat(
                    [self.df1_1, self.df1_2, self.df1_3, self.df1_4, self.df1_5, self.df2_1, self.df2_4,
                     self.df3_1, self.df3_5, self.df4_1, self.df4_2, self.df4_3, self.df4_4], axis=0)
                print("success1")
                data = pd.DataFrame(columns=['x', 'y'])
                data['x'] = combined_df['x']
                data['y'] = combined_df['y']
                list_x = [-40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60,
                          70, 80, 90, 100, 110, 120, 130, 140, 150, 160]
                list_y = [-200, -190, -180, -170, -160, -150, -140,
                          -130, -120, -110, -100, -90, -80, -70, -60,
                          -50, -40, -30, -20, -10, 0, 10, 20, 30,
                          40, 50, 60, 70, 80, 90, 100]
                res = np.zeros((20, 30))
                for index, row in combined_df.iterrows():
                    # print(row['x'], row['y'])
                    for i in range(20):
                        if list_x[i] <= row['x'] and row['x'] <= list_x[i + 1]:
                            for j in range(30):
                                if list_y[j] <= row['y'] and row['y'] <= list_y[j + 1]:
                                    res[i][j] += 1
                x = ["-90", "-80", "-70", "-60", "-50", "-40", "-30", "-20", "-10", "0",
                     "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]
                y = ["-190", "-180", "-170", "-160", "-150", "-140", "-130", "-120",
                     "-110", "-100", "-90", "-80", "-70", "-60",
                     "-50", "-40", "-30", "-20", "-10", "0", "10", "20",
                     "30", "40", "50", "60", "70", "80", "90", "100"]
                data = [(i, j, res[i][j]) for i in range(20) for j in range(30)]
                # data = [[d[1], d[0], d[2]] for d in data]
                heatmap = (
                    HeatMap(init_opts=opts.InitOpts(width="900px", height="750px"))
                    .add_xaxis(x)
                    .add_yaxis("", y, data)
                    .set_global_opts(
                        title_opts=opts.TitleOpts("车辆热力图"),
                        visualmap_opts=opts.VisualMapOpts(
                            max_=1000,
                            range_color=[
                                "#ffffff", "#ffffbf", "#fee090", "#fdae61",
                                "#f46d43", "#d73027", "#a50026"
                            ],
                        )
                    )
                )
                # 获取图表的HTML内容
                self.hotmap_html = heatmap.render_embed()
                # 将图表的HTML内容加载到QWebEngineView中
                self.hotmap.setHtml(self.hotmap_html)
            except Exception as e:
                print(e)
        else:
            # 绘制行人小车热力图
            try:
                # 垂直拼接多个 DataFrame（按行）
                combined_df = pd.concat(
                    [self.df1_6, self.df2_6, self.df3_6, self.df4_6], axis=0)
                print("success1")
                data = pd.DataFrame(columns=['x', 'y'])
                data['x'] = combined_df['x']
                data['y'] = combined_df['y']
                list_x = [-40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60,
                          70, 80, 90, 100, 110, 120, 130, 140, 150, 160]
                list_y = [-200, -190, -180, -170, -160, -150, -140, -130,
                          -120, -110, -100, -90, -80, -70, -60,
                          -50, -40, -30, -20, -10, 0, 10, 20,
                          30, 40, 50, 60, 70, 80, 90, 100]
                res = np.zeros((20, 30))
                for index, row in combined_df.iterrows():
                    # print(row['x'], row['y'])
                    for i in range(20):
                        if list_x[i] <= row['x'] and row['x'] <= list_x[i + 1]:
                            for j in range(30):
                                if list_y[j] <= row['y'] and row['y'] <= list_y[j + 1]:
                                    res[i][j] += 1
                x = ["-90", "-80", "-70", "-60", "-50", "-40", "-30", "-20", "-10", "0",
                     "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]
                y = ["-190", "-180", "-170", "-160", "-150", "-140", "-130", "-120",
                     "-110", "-100", "-90", "-80", "-70", "-60",
                     "-50", "-40", "-30", "-20", "-10", "0", "10", "20",
                     "30", "40", "50", "60", "70", "80", "90", "100"]
                data = [(i, j, res[i][j]) for i in range(20) for j in range(30)]
                # data = [[d[1], d[0], d[2]] for d in data]
                heatmap = (
                    HeatMap(init_opts=opts.InitOpts(width="900px", height="750px"))
                    .add_xaxis(x)
                    .add_yaxis("", y, data)
                    .set_global_opts(
                        title_opts=opts.TitleOpts("行人/小车热力图"),
                        visualmap_opts=opts.VisualMapOpts(
                            max_=1000,
                            range_color=[
                                "#ffffff", "#ffffbf", "#fee090", "#fdae61",
                                "#f46d43", "#d73027", "#a50026"
                            ],
                        )
                    )
                )
                # 获取图表的HTML内容
                self.hotmap_html = heatmap.render_embed()
                # 将图表的HTML内容加载到QWebEngineView中
                self.hotmap.setHtml(self.hotmap_html)
            except Exception as e:
                print(e)
    def combo3_2_change(self, index):
        print(index)
        if index == 0:
            # 绘制汽车3D图
            try:
                # 垂直拼接多个 DataFrame（按行）
                combined_df = pd.concat(
                    [self.df1_1, self.df1_2, self.df1_3, self.df1_4, self.df1_5, self.df2_1, self.df2_4,
                     self.df3_1, self.df3_5, self.df4_1, self.df4_2, self.df4_3, self.df4_4], axis=0)
                print("success1")
                data = pd.DataFrame(columns=['x', 'y'])
                data['x'] = combined_df['x']
                data['y'] = combined_df['y']
                list_x = [-40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60,
                          70, 80, 90, 100, 110, 120, 130, 140, 150, 160]
                list_y = [-200, -190, -180, -170, -160, -150, -140, -130,
                          -120, -110, -100, -90, -80, -70, -60,
                          -50, -40, -30, -20, -10, 0, 10, 20, 30,
                          40, 50, 60, 70, 80, 90, 100]
                res = np.zeros((20, 30))
                for index, row in combined_df.iterrows():
                    # print(row['x'], row['y'])
                    for i in range(20):
                        if list_x[i] <= row['x'] and row['x'] <= list_x[i + 1]:
                            for j in range(30):
                                if list_y[j] <= row['y'] and row['y'] <= list_y[j + 1]:
                                    res[i][j] += 1
                x = ["-90", "-80", "-70", "-60", "-50", "-40", "-30", "-20", "-10", "0",
                     "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]
                y = ["-190", "-180", "-170", "-160", "-150", "-140", "-130",
                     "-120", "-110", "-100", "-90", "-80", "-70", "-60",
                     "-50", "-40", "-30", "-20", "-10", "0", "10", "20",
                     "30", "40", "50", "60", "70", "80", "90", "100"]

                data = [(i, j, res[i][j]) for i in range(20) for j in range(30)]
                # data = [[d[1], d[0], d[2]] for d in data]
                bar3d = (
                    Bar3D(init_opts=opts.InitOpts(width="800px", height="750px")).add(
                        series_name="",
                        data=data,
                        xaxis3d_opts=opts.Axis3DOpts(type_="category", data=x),
                        yaxis3d_opts=opts.Axis3DOpts(type_="category", data=y),
                        zaxis3d_opts=opts.Axis3DOpts(type_="value"),
                    ).set_global_opts(
                        title_opts=opts.TitleOpts("车辆3D柱状图"),
                        visualmap_opts=opts.VisualMapOpts(
                            max_=1000,
                            range_color=[
                                "#313695", "#4575b4", "#74add1", "#abd9e9",
                                "#e0f3f8", "#ffffbf", "#fee090", "#fdae61",
                                "#f46d43", "#d73027", "#a50026"
                            ],
                        )
                    )
                )
                # 获取图表的HTML内容
                self.bar3d_html = bar3d.render_embed()
                # 将图表的HTML内容加载到QWebEngineView中
                self.bar3d.setHtml(self.bar3d_html)
            except Exception as e:
                print(e)
        else:
            # 绘制行人小车3D图
            try:
                # 垂直拼接多个 DataFrame（按行）
                combined_df = pd.concat(
                    [self.df1_6, self.df2_6, self.df3_6, self.df4_6], axis=0)
                print("success1")
                data = pd.DataFrame(columns=['x', 'y'])
                data['x'] = combined_df['x']
                data['y'] = combined_df['y']
                list_x = [-40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70,
                          80, 90, 100, 110, 120, 130, 140, 150, 160]
                list_y = [-200, -190, -180, -170, -160, -150, -140, -130,
                          -120, -110, -100, -90, -80, -70, -60,
                          -50, -40, -30, -20, -10, 0, 10, 20, 30,
                          40, 50, 60, 70, 80, 90, 100]
                res = np.zeros((20, 30))
                for index, row in combined_df.iterrows():
                    # print(row['x'], row['y'])
                    for i in range(20):
                        if list_x[i] <= row['x'] and row['x'] <= list_x[i + 1]:
                            for j in range(30):
                                if list_y[j] <= row['y'] and row['y'] <= list_y[j + 1]:
                                    res[i][j] += 1
                x = ["-90", "-80", "-70", "-60", "-50", "-40", "-30", "-20", "-10", "0",
                     "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]
                y = ["-190", "-180", "-170", "-160", "-150", "-140", "-130",
                     "-120", "-110", "-100", "-90", "-80", "-70", "-60",
                     "-50", "-40", "-30", "-20", "-10", "0", "10", "20",
                     "30", "40", "50", "60", "70", "80", "90", "100"]
                data = [(i, j, res[i][j]) for i in range(20) for j in range(30)]
                # data = [[d[1], d[0], d[2]] for d in data]
                bar3d = (
                    Bar3D(init_opts=opts.InitOpts(width="800px", height="750px")).add(
                        series_name="",
                        data=data,
                        xaxis3d_opts=opts.Axis3DOpts(type_="category", data=x),
                        yaxis3d_opts=opts.Axis3DOpts(type_="category", data=y),
                        zaxis3d_opts=opts.Axis3DOpts(type_="value"),
                    ).set_global_opts(
                        title_opts=opts.TitleOpts("行人/小车3D柱状图"),
                        visualmap_opts=opts.VisualMapOpts(
                            max_=1000,
                            range_color=[
                                "#313695", "#4575b4", "#74add1", "#abd9e9",
                                "#e0f3f8", "#ffffbf", "#fee090", "#fdae61",
                                "#f46d43", "#d73027", "#a50026"
                            ],
                        )
                    )
                )
                # 获取图表的HTML内容
                self.bar3d_html = bar3d.render_embed()
                # 将图表的HTML内容加载到QWebEngineView中
                self.bar3d.setHtml(self.bar3d_html)
            except Exception as e:
                print(e)
    # tab4会根据用户是否有选择数据集，而选择是否展示
    # tab5_下拉框
    def combo5_change(self, index):
        print("你选择了：" + self.combo.currentText())
        print(index)
        # 判断是否加载了xlsx/csv数据集
        if type(self.df) == int:
            print("未加载数据表xlsx/csv")
            # 弹出提示框
            dialog = QMessageBox()
            dialog.setWindowTitle('warning')
            dialog.setIcon(QMessageBox.Warning)
            dialog.setText("请先选择数据集！")
            dialog.exec_()
            return
        if index == 0:
            # 绘制chart5
            self.figure5_3 = Figure(figsize=(24, 6))
            self.myax5 = self.figure5_3.add_subplot(111)
            self.canvas = FigureCanvas(self.figure5_3)
            # 根据时间间隔进行分箱
            self.df['global_time'] = pd.to_datetime(self.df['global_time'])
            # self.df['global_time'] = pd.to_datetime(self.df['global_time'], format='%Y-%m-%d %H:%M:%S.%f')
            self.df['global_time'] = pd.to_datetime('2023-09-16 '
                                                    + self.df['global_time'].dt.strftime('%H:%M:%S'))
            # 获取当前日期
            # current_date = datetime.today().date()
            current_date = datetime.today().replace(year=2023, month=9, day=16).date()
            # 创建时间部分
            start_time = time(7, 54, 0)
            end_time = time(8, 24, 0)
            # 组合日期和时间
            start_time = datetime.combine(current_date, start_time)
            end_time = datetime.combine(current_date, end_time)
            filtered_data = self.df[(self.df['global_time'] >= start_time)
                                    & (self.df['global_time'] <= end_time)]
            bins = pd.date_range(start=start_time, end=end_time, freq='2T')
            binned_data = pd.cut(filtered_data['global_time'], bins=bins)
            # 使用自定义坐标轴进行柱状图绘制
            counts = binned_data.value_counts().sort_index()
            self.myax5.bar(counts.index.astype(str), counts, color='lightgreen')
            # binned_data.value_counts().sort_index().plot(kind='bar', color='blue')
            # 添加标签和标题
            self.myax5.set_xlabel('time')
            # 设置 x 轴刻度标签的旋转角度
            self.myax5.set_xticklabels(counts.index.astype(str), rotation=7, ha='right')
            self.myax5.set_ylabel('number of cars')
            self.myax5.set_title('cars of different times')
            self.canvas.draw()
            scene = QGraphicsScene(self)
            scene.addWidget(self.canvas)
            self.chart5.setScene(scene)
        elif index == 1:
            print(index)
            # 绘制chart5
            self.figure5_3 = Figure(figsize=(24, 6))
            self.myax5 = self.figure5_3.add_subplot(111)
            self.canvas = FigureCanvas(self.figure5_3)
            # 根据时间间隔进行分箱
            self.df['global_time'] = pd.to_datetime(self.df['global_time'])
            # self.df['global_time'] = pd.to_datetime(self.df['global_time'], format='%Y-%m-%d %H:%M:%S.%f')
            self.df['global_time'] = pd.to_datetime('2023-09-16 '
                                                    + self.df['global_time'].dt.strftime('%H:%M:%S'))
            # 获取当前日期
            # current_date = datetime.today().date()
            current_date = datetime.today().replace(year=2023, month=9, day=16).date()
            # 创建时间部分
            start_time = time(7, 54, 0)
            end_time = time(8, 24, 0)
            # 组合日期和时间
            start_time = datetime.combine(current_date, start_time)
            end_time = datetime.combine(current_date, end_time)
            filtered_data = self.df[(self.df['global_time'] >= start_time)
                                    & (self.df['global_time'] <= end_time)]
            bins = pd.date_range(start=start_time, end=end_time, freq='2T')
            binned_data = pd.cut(filtered_data['global_time'], bins=bins)
            # 绘制折线图
            counts = binned_data.value_counts().sort_index()
            self.myax5.plot(counts.index.astype(str), counts, color='pink', marker='o')
            # binned_data.value_counts().sort_index().plot(kind='bar', color='blue')
            # 添加标签和标题
            self.myax5.set_xlabel('time')
            # 设置 x 轴刻度标签的旋转角度
            self.myax5.set_xticklabels(counts.index.astype(str), rotation=7, ha='right')
            self.myax5.set_ylabel('number of cars')
            self.myax5.set_title('cars of different times')
            self.canvas.draw()
            scene = QGraphicsScene(self)
            scene.addWidget(self.canvas)
            self.chart5.setScene(scene)
        else:
            print(index)
            # 绘制chart5
            self.figure5_3 = Figure(figsize=(24, 6))
            self.myax5 = self.figure5_3.add_subplot(111)
            self.canvas = FigureCanvas(self.figure5_3)
            # 根据时间间隔进行分箱
            self.df['global_time'] = pd.to_datetime(self.df['global_time'])
            # self.df['global_time'] = pd.to_datetime(self.df['global_time'], format='%Y-%m-%d %H:%M:%S.%f')
            self.df['global_time'] = pd.to_datetime('2023-09-16 '
                                                    + self.df['global_time'].dt.strftime('%H:%M:%S'))
            # 获取当前日期
            # current_date = datetime.today().date()
            current_date = datetime.today().replace(year=2023, month=9, day=16).date()
            # 创建时间部分
            start_time = time(7, 54, 0)
            end_time = time(8, 24, 0)
            # 组合日期和时间
            start_time = datetime.combine(current_date, start_time)
            end_time = datetime.combine(current_date, end_time)
            filtered_data = self.df[(self.df['global_time'] >= start_time)
                                    & (self.df['global_time'] <= end_time)]
            bins = pd.date_range(start=start_time, end=end_time, freq='2T')
            binned_data = pd.cut(filtered_data['global_time'], bins=bins)
            # 使用自定义坐标轴进行柱状图绘制
            counts = binned_data.value_counts().sort_index()
            self.myax5.bar(counts.index.astype(str), counts, color='lightgreen')
            # 绘制折线图（多加一个y轴出来）
            self.myax6 = self.myax5.twinx()
            self.myax6.plot(counts.index.astype(str), counts, color='pink', marker='o')
            self.figure5_3.legend(['Line Chart'], loc='upper left')
            # 添加标签和标题
            self.myax5.set_xlabel('time')
            # 设置 x 轴刻度标签的旋转角度
            self.myax5.set_xticklabels(counts.index.astype(str), rotation=7, ha='right')
            self.myax5.set_ylabel('number of cars')
            self.myax5.set_title('cars of different times')
            self.canvas.draw()
            scene = QGraphicsScene(self)
            scene.addWidget(self.canvas)
            self.chart5.setScene(scene)
    # tab6_btn事件
    def show_specific_data(self):
        # myinput = int(self.input.text())
        try:
            myinput = int(self.input.text())
        except ValueError:
            # 如果用户输入的不是整数，显示一个错误提示框
            QMessageBox.warning(self, 'error', '请输入有效的整数', QMessageBox.Ok)
            return
        print(self.df)
        print(myinput)
        if type(self.df) == int:
            print("未加载数据表xlsx/csv")
            dialog = QMessageBox()
            dialog.setWindowTitle('warning')
            dialog.setIcon(QMessageBox.Warning)
            dialog.setText('未加载数据表xlsx/csv')
            dialog.exec_()
            return
        try:
            print(self.df['target_id'] == myinput)
            data = self.df[self.df['target_id'] == myinput]
            data = data.reset_index(drop=True)
        except Exception as e:
            print(e)
        if data.empty:
            # 弹窗提示用户没有找到记录
            print("未找到匹配的记录，请尝试其他输入。")
            dialog = QMessageBox()
            dialog.setWindowTitle('warning')
            dialog.setIcon(QMessageBox.Warning)
            dialog.setText('未找到匹配的记录，请尝试其他输入。')
            dialog.exec_()
            return
        print(data['target_name'][1])
        print(data['target_tag'][1])
        try:
            self.show_id.setText(self.input.text())
            self.show_name.setText(data['target_name'][1])
            self.show_veh.setText(data['target_tag'][1])
            self.show_direction.setText("right")
            self.show_speed.setText(str(round(data['speed'].mean(), 2)))
            self.show_acc.setText(str(round(data['acceleration'].mean(), 2)))
            self.show_alltime.setText(str(round(data['local_elapsed_time'].max(), 2)))
            self.show_status.setText(data['status'][1])
        except Exception as e:
            print(e)
        scene = QGraphicsScene()
        if data['target_tag'][1] == 'veh':
            img = QPixmap("./data/car.jpg")
            img = img.scaled(450, 400)
            scene.addPixmap(img)
            self.show_image.setScene(scene)
            # 调整图像大小以适应场景
            # self.show_image.setRenderHint(QPainter.Antialiasing, True)
            # self.show_image.setRenderHint(QPainter.SmoothPixmapTransform, True)
            # self.show_image.setRenderHint(QPainter.HighQualityAntialiasing, True)
        elif data['target_tag'][1] == 'bus':
            try:
                img = QPixmap("./data/bus.jpg")
                img = img.scaled(450, 400)
                scene.addPixmap(img)
                self.show_image.setScene(scene)
            except Exception as e:
                print(e)
        elif data['target_tag'][1] == 'human':
            try:
                img = QPixmap("./data/human.jpg")
                img = img.scaled(450, 400)
                scene.addPixmap(img)
                self.show_image.setScene(scene)
            except Exception as e:
                print(e)
        elif data['target_tag'][1] == 'bike':
            try:
                img = QPixmap("./data/bike.jpg")
                img = img.scaled(450, 400)
                scene.addPixmap(img)
                self.show_image.setScene(scene)
            except Exception as e:
                print(e)
        else:
            try:
                img = QPixmap("./data/ele_veh.jpg")
                img = img.scaled(400, 400)
                scene.addPixmap(img)
                self.show_image.setScene(scene)
            except Exception as e:
                print(e)
        # 一辆车 - 速度/加速度图
        # 创建Matplotlib图形区域
        try:
            self.figure6_3 = Figure(figsize=(5, 4))
            self.myax1 = self.figure6_3.add_subplot(111)
            self.canvas = FigureCanvas(self.figure6_3)
            # 绘制速度和加速度随时间的变化曲线
            self.myax1.set_title('speed and acceleration')
            self.myax1.plot(data['local_elapsed_time'], data['speed'], label='Speed')
            # plt.plot(data1['local_elapsed_time'], data1['speed'], label='Speed2')
            self.myax1.plot(data['local_elapsed_time'], data['acceleration'], label='Acceleration')
            self.myax1.set_xlabel('Time (s)')
            self.myax1.set_ylabel('Speed / Acceleration (m/s / m/s^2)')
            self.myax1.legend()
            self.canvas.draw()
            # self.myscene1 = QGraphicsScene()
            # self.myview1 = QGraphicsView(self.scene)
            scene = QGraphicsScene(self)
            scene.addWidget(self.canvas)
            # 将 QGraphicsScene 设置到 QGraphicsView 中
            self.chart_speed.setScene(scene)
            # 一辆车 - 位置图
            self.figure6_2 = Figure(figsize=(5, 4))
            self.myax2 = self.figure6_2.add_subplot(111)
            self.canvas = FigureCanvas(self.figure6_2)
            x = data['x']
            y = data['y']
            print(x)
            self.myax2.set_title('location x and y')
            self.myax2.scatter(x, y, c='green')
            self.canvas.draw()
            scene = QGraphicsScene(self)
            scene.addWidget(self.canvas)
            self.chart_location.setScene(scene)
            # 一辆车 - 曲率图
            self.figure6_1 = Figure(figsize=(7, 4))
            self.myax3 = self.figure6_1.add_subplot(111)
            self.canvas = FigureCanvas(self.figure6_1)
            self.myax3.set_title('Curve')
            self.myax3.plot(data['local_elapsed_time'], data['angle'], label='Curve', c='lightcoral')
            self.myax3.set_xlabel('Time (s)')
            self.myax3.set_ylabel('Curve')
            self.myax3.legend()
            self.canvas.draw()
            scene = QGraphicsScene(self)
            scene.addWidget(self.canvas)
            self.chart_curve.setScene(scene)
        except Exception as e:
            print(e)
    # tab7_btn事件
    def showtorch(self):
        try:
            # 获取用户输入
            if self.input_epoch.text() == '' or \
                    self.input_lr.text() == '' or \
                    self.input_size.text() == '':
                # 弹出提示框
                dialog = QMessageBox()
                dialog.setWindowTitle('error')
                dialog.setIcon(QMessageBox.Critical)
                dialog.setText("输入不能为空！")
                dialog.exec_()
                return
            self.epoch = int(self.input_epoch.text())
            self.lr = float(self.input_lr.text())
            self.size = int(self.input_size.text())
            # 创建Matplotlib图形区域
            self.figure7 = Figure(figsize=(8, 7))
            self.ax = self.figure7.add_subplot(111)
            self.canvas = FigureCanvas(self.figure7)
            batch_size = self.size  # 动态指定批量大小
            train_iter, test_iter = d2l.load_data_fashion_mnist(batch_size)
            # PyTorch不会隐式地调整输入的形状
            # 因此要在线性层前定义了展平层（flatten），来调整网络输入的形状
            # 自定义网络 = 展平层 + 线性层
            net = nn.Sequential(nn.Flatten(), nn.Linear(784, 10))
            def init_weights(m):
                if type(m) == nn.Linear:
                    nn.init.normal_(m.weight, std=0.01)
            net.apply(init_weights)
            # 内置交叉熵损失函数
            loss_fn = nn.CrossEntropyLoss(reduction='none')
            trainer = torch.optim.SGD(net.parameters(), lr=self.lr)  # 动态指定学习率
            num_epochs = self.epoch  # 动态指定迭代训练总次数
            train_loss, train_acc, test_acc = self.my_train(net, train_iter, test_iter,
                                                            loss_fn, num_epochs, trainer)
            # 绘制3条折线
            self.plot_metrics(train_loss, train_acc, test_acc)
            self.canvas.draw()
            scene = QGraphicsScene(self)
            scene.addWidget(self.canvas)
            self.show_pytorch.setScene(scene)
        except Exception as e:
            print(e)
    def accuracy(self, y_hat, y):
        """计算预测正确的数量"""
        if len(y_hat.shape) > 1 and y_hat.shape[1] > 1:
            y_hat = y_hat.argmax(axis=1)  # 每个样本都取概率最大的作为预测的类别
        # 看预测的类别和真实值是否相等（先将y_hat的形式转为和y一样，再做判断）
        cmp = y_hat.type(y.dtype) == y
        return float(cmp.type(y.dtype).sum())  # 表示预测正确的样本总数
    def evaluate_accuracy(self, net, data_iter):
        """计算在指定数据集上模型的精度"""
        if isinstance(net, torch.nn.Module):
            net.eval()  # 将模型设置为评估模式，不会自动计算梯度
        # 累加器对象，能累加  正确预测数、预测总数  这两种
        metric = Accumulator(2)
        with torch.no_grad():
            for X, y in data_iter:
                metric.add(self.accuracy(net(X), y), y.numel())
                # net(X): 利用模型的前向传播，得到预测结果（类似于上文出现的y_hat）
                # accuracy(net(X), y) 就是利用上面定义的函数：计算这个小批量预测正确的数量
                # y.numel() 计算整个y的真实值数量     最后metric.add，将这个小批量的数据累加到累加器metric中
        print("test accuracy:   " + str(metric[0] / metric[1]))
        self.output_test_acc.setText(str(round(metric[0] / metric[1], 4)))
        return metric[0] / metric[1]  # 总准确率 = 总预测正确数量 / 总数量
    def train_epoch_ch3(self, net, train_iter, loss, updater):  # @save
        """训练模型一个迭代周期"""
        # 若是nn模型则启动train训练模式，表示要计算梯度
        if isinstance(net, torch.nn.Module):
            net.train()
        # 累加3种数据：训练损失总和、训练准确度总和、样本数
        metric = Accumulator(3)
        for X, y in train_iter:
            # 计算梯度并更新参数
            y_hat = net(X)
            l = loss(y_hat, y)
            if isinstance(updater, torch.optim.Optimizer):
                # 使用PyTorch内置的优化器和损失函数
                updater.zero_grad()
                # 求loss均值得到标量，再反向传播，计算梯度，求出梯度下降的最优方向
                l.mean().backward()
                # 内置SGD进行梯度下降，更新模型操作
                updater.step()
            else:
                # 使用定制的优化器和损失函数
                l.sum().backward()
                updater(X.shape[0])
            metric.add(float(l.sum()), self.accuracy(y_hat, y), y.numel())
        # 返回训练损失和训练精度
        print("最终训练损失:   " + str(metric[0] / metric[2]))
        print("最终train训练精度:   " + str(metric[1] / metric[2]))
        self.output_loss.setText(str(round(metric[0] / metric[2], 4)))
        self.output_train_acc.setText(str(round(metric[1] / metric[2], 4)))
        return metric[0] / metric[2], metric[1] / metric[2]
    # 自定义模型训练函数
    def my_train(self, net, train_iter, test_iter, loss_fn, num_epochs, updater):
        train_losses, train_acc = [], []
        # 进行多轮迭代循环训练，每次训练后都记录loss损失、精确度等数值
        for epoch in range(num_epochs):
            loss, acc = self.train_epoch_ch3(net, train_iter, loss_fn, updater)
            train_losses.append(loss)
            train_acc.append(acc)
        test_acc = self.evaluate_accuracy(net, test_iter)
        return train_losses, train_acc, test_acc
    # 绘制三条折线的函数
    def plot_metrics(self, train_losses, train_acc, test_acc):
        x_vals = np.arange(1, len(train_losses) + 1)
        self.ax.plot(x_vals, train_losses, label='Train Loss')
        self.ax.plot(x_vals, train_acc, label='Train Accuracy')
        self.ax.plot(x_vals, [test_acc] * len(train_losses), label='Test Accuracy')
        self.ax.legend()
        # 添加这行以实现动态展现
        plt.pause(0.1)
    # 保存图表/导出为图片
    # 导出为图片
    def export_chart1(self):
        # 拿到想要导出的路径
        # 其中支持(*.png *.jpg *.bmp)这三种图片格式导出
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Chart Image', '', 'Images (*.png *.jpg *.bmp)')
        # 用户点击了确定
        if file_path:
            # 保存为图片
            self.figure1.savefig(file_path)
        # 用户点击了取消
        else:
            print('用户取消了保存图片操作')
            return
    def export_chart3_1(self):
        # 保存热力图
        pixmap = QPixmap()
        # 获取图表的截图
        pixmap = self.hotmap.grab()
        # 拿到想要导出的路径
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Hotmap Image", "",
                                                   "Images (*.png *.jpg *.bmp)")  # 弹出保存文件对话框
        if file_path != "":
            pixmap.save(file_path)  # 保存图表
        else:
            print('用户取消了保存图片操作')
            return
    def export_chart3_2(self):
        # 保存3D柱状图
        pixmap = QPixmap()
        # 获取图表的截图
        pixmap = self.bar3d.grab()
        # 拿到想要导出的路径
        file_path, _ = QFileDialog.getSaveFileName(self, "Save 3D Bar Image", "",
                                                   "Images (*.png *.jpg *.bmp)")  # 弹出保存文件对话框
        if file_path != "":
            pixmap.save(file_path)  # 保存图表
        else:
            print('用户取消了保存图片操作')
            return
    def export_chart4_1(self):
        # 保存3D柱状图
        pixmap = QPixmap()
        # 获取图表的截图
        pixmap = self.small_hotmap.grab()
        # 拿到想要导出的路径
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Small Hotmap Image', '',
                                                   'Images (*.png *.jpg *.bmp)')
        if file_path != "":
            pixmap.save(file_path)  # 保存图表
        else:
            print('用户取消了保存图片操作')
            return
    def export_chart4_2(self):
        # 保存3D柱状图
        pixmap = QPixmap()
        # 获取图表的截图
        pixmap = self.small_bar3d.grab()
        # 拿到想要导出的路径
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Small 3D Bar Chart Image', '',
                                                   'Images (*.png *.jpg *.bmp)')
        if file_path != "":
            pixmap.save(file_path)  # 保存图表
        else:
            print('用户取消了保存图片操作')
            return
    def export_chart5_1(self):
        # 拿到想要导出的路径
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Chart Image', '', 'Images (*.png *.jpg *.bmp)')
        if file_path:
            # 保存为图片
            self.figure5_1.savefig(file_path)
        else:
            print('用户取消了保存图片操作')
            return
    def export_chart5_2(self):
        # 拿到想要导出的路径
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Chart Image', '', 'Images (*.png *.jpg *.bmp)')
        if file_path:
            # 保存为图片
            self.figure5_2.savefig(file_path)
        else:
            print('用户取消了保存图片操作')
            return
    def export_chart5_3(self):
        # 拿到想要导出的路径
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Chart Image', '', 'Images (*.png *.jpg *.bmp)')
        if file_path:
            # 保存为图片
            self.figure5_3.savefig(file_path)
        else:
            print('用户取消了保存图片操作')
            return
    def export_chart6_1(self):
        # 拿到想要导出的路径
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Chart Image', '', 'Images (*.png *.jpg *.bmp)')
        if file_path:
            # 保存为图片
            self.figure6_1.savefig(file_path)
        else:
            print('用户取消了保存图片操作')
            return
    def export_chart6_2(self):
        # 拿到想要导出的路径
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Chart Image', '', 'Images (*.png *.jpg *.bmp)')
        if file_path:
            # 保存为图片
            self.figure6_2.savefig(file_path)
        else:
            print('用户取消了保存图片操作')
            return
    def export_chart6_3(self):
        # 拿到想要导出的路径
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Chart Image', '', 'Images (*.png *.jpg *.bmp)')
        if file_path:
            # 保存为图片
            self.figure6_3.savefig(file_path)
        else:
            print('用户取消了保存图片操作')
            return
    def export_chart7(self):
        # 拿到想要导出的路径
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Chart Image', '', 'Images (*.png *.jpg *.bmp)')
        # if file_path:
        #     # Use the snapshot feature to export the chart as an image
        #     self.small_bar3d.page().runJavaScript('''
        #                 var canvas = document.createElement("canvas");
        #                 canvas.width = 800;  // set the width of canvas to match the chart
        #                 canvas.height = 600;  // set the height of canvas to match the chart
        #                 var ctx = canvas.getContext("2d");
        #                 echarts.getInstanceByDom(document.getElementById("main"))._chart.convertToPixel({xAxisIndex: 0}, [0, 0]);
        #                 echarts.getInstanceByDom(document.getElementById("main"))._chart.group.renderToCanvas(ctx);
        #                 canvas.toBlob(function(blob) {
        #                     var reader = new FileReader();
        #                     reader.onloadend = function() {
        #                         var base64data = reader.result;
        #                         pywebview.api.exportSmallBar3d(base64data);
        #                     }
        #                     reader.readAsDataURL(blob);
        #                 });
        #             ''')
        if file_path:
            # 保存为图片
            self.figure7.savefig(file_path)
        else:
            print('用户取消了保存图片操作')
            return
    # 数据预处理
    def pre_data(self):
        df1_1 = 0
        plt.figure(figsize=(8, 6))
        df1_1['status'].value_counts().plot(kind='bar', color='skyblue')
        plt.xlabel('Vehicle Status')
        plt.ylabel('Count')
        plt.title('Distribution of Vehicle Status')
        plt.show()
        plt.figure(figsize=(10, 6))
        plt.scatter(df1_1['local_elapsed_time'], df1_1['x'], label='X Position', alpha=0.7)
        plt.scatter(df1_1['local_elapsed_time'], df1_1['y'], label='Y Position', alpha=0.7)
        plt.xlabel('Local Elapsed Time')
        plt.ylabel('Position')
        plt.legend()
        plt.title('Vehicle Position Over Time')
        plt.show()
        df = df1_1
        df['local_elapsed_time'] = pd.to_numeric(df['local_elapsed_time'], errors='coerce')
        df = df.dropna(subset=['local_elapsed_time'])
        df = df.reset_index(drop=True)
        df = df.drop(df.columns[0], axis=1)
        df = df1_1.iloc[:120]
        # 转为数值型，去除中间没用的标签行
        df1_4 = df
        df1_4['local_elapsed_time'] = pd.to_numeric(df1_4['local_elapsed_time'], errors='coerce')  # 转为数值型，转不了就变为NaN
        df1_4 = df1_4.dropna(subset=['local_elapsed_time'])  # 去除NaN
        df1_4 = df1_4.reset_index(drop=True)
        # 行人/电动/自行车数据预处理
        xlsx_5_1 = pd.ExcelFile('./data/行人电动车自行车/5_1.xlsx')
        xlsx_5_2 = pd.ExcelFile('./data/行人电动车自行车/5_2.xlsx')
        xlsx_5_3 = pd.ExcelFile('./data/行人电动车自行车/5_3.xlsx')
        xlsx_5_4 = pd.ExcelFile('./data/行人电动车自行车/5_4.xlsx')
        df5_1 = pd.read_excel(xlsx_5_1)
        df5_2 = pd.read_excel(xlsx_5_2)
        df5_3 = pd.read_excel(xlsx_5_3)
        df5_4 = pd.read_excel(xlsx_5_4)
        df5_1 = df5_1.drop("tag", axis=1)
        df5_2 = df5_2.drop("tag", axis=1)
        df5_3 = df5_3.drop("tag", axis=1)
        df5_4 = df5_4.drop("tag", axis=1)
        df5_1 = df5_1.loc[~df5_1['target_name'].apply(lambda x: isinstance(x, float))]
        df5_2 = df5_2.loc[~df5_2['target_name'].apply(lambda x: isinstance(x, float))]
        df5_3 = df5_3.loc[~df5_3['target_name'].apply(lambda x: isinstance(x, float))]
        df5_4 = df5_4.loc[~df5_4['target_name'].apply(lambda x: isinstance(x, float))]
        df5_1['target_tag'] = df5_1['target_name'].apply(lambda name: 'human' if ('P' in name or 'p' in name) else (
            'ele_veh' if ('M' in name or 'm' in name) else 'bike'))
        df5_2['target_tag'] = df5_2['target_name'].apply(lambda name: 'human' if ('P' in name or 'p' in name) else (
            'ele_veh' if ('M' in name or 'm' in name) else 'bike'))
        df5_3['target_tag'] = df5_3['target_name'].apply(lambda name: 'human' if ('P' in name or 'p' in name) else (
            'ele_veh' if ('M' in name or 'm' in name) else 'bike'))
        df5_4['target_tag'] = df5_4['target_name'].apply(lambda name: 'human' if ('P' in name or 'p' in name) else (
            'ele_veh' if ('M' in name or 'm' in name) else 'bike'))
        df5_1.to_excel('./data/行人、电动车及自行车数据/5_1.xlsx', index=False)
        df5_2.to_excel('./data/行人、电动车及自行车数据/5_2.xlsx', index=False)
        df5_3.to_excel('./data/行人、电动车及自行车数据/5_3.xlsx', index=False)
        df5_4.to_excel('./data/行人、电动车及自行车数据/5_4.xlsx', index=False)
    # 退出函数
    def myexit(self):
        exit()
if __name__ == "__main__":
    # 创建应用程序对象
    app = QApplication(sys.argv)
    # 创建自定义的窗口MyWindow对象，初始化相关属性和方法
    win = MyWindow()
    # 显示图形界面
    win.ui.show()
    # 启动应用程序的事件循环，可不断见监听点击事件等
    app.exec()