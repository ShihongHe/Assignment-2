# Site suitability
## Introduction
The aim of this project is to develop software for a company producing rock aggregates to help them explore three key factors for building a plant in the UK. The software will use raster data to analyse the suitability of each factor for the location of the plant. By assigning weights to each factor and adding up the weighted factors, the software will produce a comprehensive suitability map. A graphical user interface (GUI) is provided to allow the user to easily select the factor weights and view the visualisation of the suitability score in real time. Finally, the software saves a raster of the results as a file for further analysis and decision making.
## Installation
1. Install Python 3.8 or later. You can download and install it from the official Python website:[https://www.python.org/downloads/](https://www.python.org/downloads/).
2. To access the project directory and install the required dependencies:
```
cd src
pip install -r requirements.txt
```
## Project structure
```
Site-suitability/
│
├── data/
│   ├── input/
│   │   ├── geology.txt
│   │   ├── population.txt
│   │   └── transport.txt
│   └── output/
│
├── src/
│   ├── main.py
│   ├── requirements.txt
│   └── my_modules/
│       ├── GUI.py
│       ├── io.py
│       ├── raster.py
│       └── test_raster.py
│
└── README.md
```
## Use
### Run the application:
```
python main.py
```
### GUI interface use
1. Show raster images: Select one or more text files by clicking on **'Show raster'** under **'File'** in the menu bar, click on the **'Open'** button to read the files and the raster images will be displayed side by side in the canvas area.
2. 根据权重生成场地适宜性地图：在**'Show raster'** 页面下点击**'Visualise the suitability'**或点击**'File'**下的**'Visualise the suitability'**选择影响因子的文件。选择文件后可以看到画布上出现对应的因子图像以及一个场地适宜性的图像。通过调整对应因子的滑块来改变每个因子对应的权重，重新加权计算场地适应性图像。同时下方还有三个按钮，分别为**'Save Image'**，**'Save File'**，**'Add'**。它们对应的功能是，保存生成的场地适宜性的图像(有.jpg , .png 和 .svg的格式可以选择)，保存文本文件(有.txt和.csv格式可以选择)和添加因子
### Features

