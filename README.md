## 程序设计实习大作业

- [源代码](/src/main.py)
- [项目报告](/81-作业报告.pdf)
- [演示视频](/81-演示.mp4)

## 项目介绍

本程序采用 Python 编写，主要基于 **PyQt 框架** 实现图形用户界面，同时结合多种现代开发工具和第三方服务，确保良好的用户体验和系统扩展性。

### 1. 界面设计与框架集成

* **界面实现**：大部分界面使用 PyQt 手写构建，部分简单界面则使用 **Qt Designer** 设计并生成 `.ui` 文件，随后通过 `pyuic` 工具编译为 `.py` 文件，供程序调用。
* **统一界面管理**：所有页面均通过 `FrameWrapper` 类统一挂载到主窗口，实现模块间的解耦与界面切换的统一管理。
* **现代化外观**：主窗口继承自 [qfluentwidgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)，提供符合 Windows Fluent Design 的现代化 UI，提升用户视觉体验。
* **复杂界面嵌套**：如“统计信息”页面，使用 **`QWebEngineView`** 嵌入基于 **pyecharts** 渲染的交互式图表，实现高质量的数据可视化展示。

### 2. 单词书数据管理

* **数据来源**：单词书数据来自开源项目 [LinXueyuanStdio/DictionaryData](https://github.com/LinXueyuanStdio/DictionaryData)。
* **数据处理流程**：

  * 首先进行数据清洗，将原始关系型数据库中的内容转化为程序内部可识别的 `Book`、`Word` 等对象模型；
  * 利用 **DeepSeek API** 补全原始数据中缺失的翻译内容，提升词汇数据的完整性；
  * 最终将数据转存为 **Apache Arrow 格式** 的二进制文件，有效提升数据加载速度和运行性能。
* **工具模块**：相关数据处理逻辑封装于 `bookdata/toolkit` 模块中，便于后续扩展和维护。

### 3. 音频播放与词典服务

* **发音音频**：使用 **有道词典 API** 获取单词发音音频，并通过 `ffmpeg` 播放；

  * 播放逻辑封装于 `utils/audio` 模块；
  * 采用 **子线程** 播放音频，避免阻塞主线程，确保界面响应流畅。
* **在线词典服务**：

  * 使用自定义爬虫，从有道词典网页实时抓取词义、图片、常用搭配等信息；
  * 相关功能由 `extern/webDict` 模块集中管理。

### 4. 用户配置与进度管理

* **配置管理**：

  * 所有用户配置与学习进度管理逻辑集中于 `settings` 包中；
  * 使用 UUID（通用唯一标识符）为单词和单词书赋予唯一身份，以确保跨会话记录准确。
* **历史记录与进度保存**：

  * 采用本地 JSON 文件（`settings.json`）保存用户设置和学习进度；
  * 支持记录每个单词的学习状态，便于将来引入如“艾宾浩斯遗忘曲线”等智能复习策略；
  * 历史记录模块已预留接口，以支持更多高级学习策略的扩展。

### 5. 界面代码结构

* 所有 UI 界面均被封装为独立类，具备良好的模块化和可维护性。
* 每个界面类均包含以下三个核心方法：

  * `setupUi`: 初始化界面组件；
  * `setupConnections`: 建立控件之间的信号与槽连接；
  * `update`: 在界面切换或数据变化时实时更新界面显示内容。
* 此结构设计可确保界面响应用户操作变化，提升程序整体的交互性和稳定性。


## Credits

- [qfluentwidgets](https://qfluentwidgets.com/)
- [DictionaryData](https://github.com/LinXueyuanStdio/DictionaryData)
- [FFmpeg](https://ffmpeg.org/)