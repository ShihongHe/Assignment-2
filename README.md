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
1. **Show raster images:** Select one or more text files by clicking on **'Show raster'** under **'File'** in the menu bar, click on the **'Open'** button to read the files and the raster images will be displayed side by side in the canvas area.
2. **Generation of site suitability maps based on weights:** Under the **'Show raster'** page click on **'Visualise the suitability'** or under **'File'** click on **'Visualise the suitability'** to select the file with the impact factor. After selecting the file you will see an image of the corresponding factor on the canvas as well as an image of the site suitability. By adjusting the sliders for the corresponding factors you can change the weights corresponding to each factor and reweight the site suitability image. There are also three buttons at the bottom, **'Save Image'**, **'Save File'** and **'Add'**. They correspond to the functions of saving the generated site suitability image (.jpg , .png and .svg formats are available), saving a text file (.txt and .csv formats are available) and adding a factor.
3. **Open the readme file：**The Readme file can be opened by clicking on **'Readme'** under **'Help'** to view the file for help on how to use it.
4. **Exit:** The GUI page can be exited by clicking on **'Exit'** under **'File'**.
5. **Shortcut keys:**
- Ctrl+s: Show raster
- Ctrl+v: Visualise the suitability
- Ctrl+e: Exit
- Ctrl+r: Readme
### Features


