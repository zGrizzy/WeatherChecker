import os
import sys

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLineEdit, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, \
    QWidget

from data_management import get_weather
from visualization import plot_interactive_temperature_comparison, plot_temperature_comparison


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ensure the data directory exists
        data_directory = '../data'
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)

        # Handle the CSV file
        csv_path = os.path.join(data_directory, 'weather.csv')
        if not os.path.exists(csv_path):
            self.weather_data = pd.DataFrame(columns=['Date', 'Temperature', 'City'])
        else:
            self.weather_data = pd.read_csv(csv_path)

        # Load stylesheet
        stylesheet_path = os.path.join('../stylesheet', 'style.qss')
        try:
            with open(stylesheet_path, 'r') as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")

        # For buttons and layout
        self.setWindowTitle('Weather Information App')
        self.setWindowIcon(QIcon('../icons/sunny-cloud.png'))
        self.setGeometry(100, 100, 700, 400)
        layout = QVBoxLayout()

        self.input_city = QLineEdit()
        self.input_city.setPlaceholderText("Enter the city name, be as precise as possible.")
        layout.addWidget(self.input_city)

        self.button_get_weather = QPushButton('Search')
        self.button_get_weather.setIcon(QIcon("../icons/search-icon.png"))
        self.button_get_weather.setIconSize(QSize(24, 24))
        self.button_get_weather.clicked.connect(self.get_weather)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.input_city)
        search_layout.addWidget(self.button_get_weather)
        layout.addLayout(search_layout)

        self.button_plot_interactive = QPushButton("Show Interactive Chart")
        self.button_plot_interactive.clicked.connect(self.update_interactive_plot)
        layout.addWidget(self.button_plot_interactive)

        self.button_plot_seaborn = QPushButton("Show Seaborn Chart")
        self.button_plot_seaborn.clicked.connect(self.update_seaborn_plot)
        layout.addWidget(self.button_plot_seaborn)

        self.weather_output = QTextEdit()
        self.weather_output.setReadOnly(True)
        layout.addWidget(self.weather_output)

        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        self.figure = plt.figure(figsize=(20, 5), num="Weather Information App - Seaborn Chart")
        self.canvas = FigureCanvas(self.figure)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def get_weather(self):
        city_name = self.input_city.text()
        try:
            weather_data = get_weather(city_name)
            current_date = pd.Timestamp('now').strftime('%Y.%m.%d, %I:%M %p')
            weather_data_formatted = {
                'Date': [current_date],
                'Temperature': [weather_data['Temperature']],
                'City': [weather_data['City']]
            }
            new_data = pd.DataFrame(weather_data_formatted)
            new_data.dropna(axis=1, how='all', inplace=True)
            if self.weather_data.empty:
                self.weather_data = new_data
            else:
                self.weather_data = pd.concat([self.weather_data, new_data], ignore_index=True)
            self.update_weather_display(weather_data)
            self.weather_data.to_csv('../data/weather.csv', index=False)
        except Exception as e:
            self.weather_output.setText(str(e))

    def update_weather_display(self, weather_info):
        display_text = f"""
    Weather Information for {weather_info['City']}:
    ---------------------------------------------------
    Temperature: {weather_info['Temperature']} °C
    Pressure: {weather_info['Pressure']} hPa
    Humidity: {weather_info['Humidity']}%
    Wind: {weather_info['Wind']}m/s
    Description: {weather_info['Description']}
    ---------------------------------------------------
    """
        self.weather_output.setText(display_text)

    def update_interactive_plot(self):
        if not self.weather_data.empty:
            html_content = plot_interactive_temperature_comparison(self.weather_data)
            self.web_view.setHtml(html_content)

    def update_seaborn_plot(self):
        self.figure.clear()
        plot_temperature_comparison(self.weather_data)
        self.canvas.draw()


# Application and main window execution
app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec())
