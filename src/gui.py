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
            self.weather_data = pd.DataFrame(columns=['Data', 'Temperatūra', 'Miestas'])
        else:
            self.weather_data = pd.read_csv(csv_path)

        # Load stylesheet
        stylesheet_path = os.path.join('../stylesheet', 'style.qss')
        try:
            with open(stylesheet_path, 'r') as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")

        # For buttons and  layout
        self.setWindowTitle('Orų Informacijos Programa')
        self.setWindowIcon(QIcon('../icons/sunny-cloud.png'))
        self.setGeometry(100, 100, 700, 400)
        layout = QVBoxLayout()

        self.input_city = QLineEdit()
        self.input_city.setPlaceholderText("Įveskite miesto pavadinimą, būkite kuo tiksliau.")
        layout.addWidget(self.input_city)

        self.button_get_weather = QPushButton('Paieška')
        self.button_get_weather.setIcon(QIcon("../icons/search-icon.png"))
        self.button_get_weather.setIconSize(QSize(24, 24))
        self.button_get_weather.clicked.connect(self.get_weather)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.input_city)
        search_layout.addWidget(self.button_get_weather)
        layout.addLayout(search_layout)

        self.button_plot_interactive = QPushButton("Rodyti interaktyvų grafiką")
        self.button_plot_interactive.clicked.connect(self.update_interactive_plot)
        layout.addWidget(self.button_plot_interactive)

        self.button_plot_seaborn = QPushButton("Rodyti Seaborn grafiką")
        self.button_plot_seaborn.clicked.connect(self.update_seaborn_plot)
        layout.addWidget(self.button_plot_seaborn)

        self.weather_output = QTextEdit()
        self.weather_output.setReadOnly(True)
        layout.addWidget(self.weather_output)

        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        self.figure = plt.figure(figsize=(20, 5), num="Orų Informacijos Programa - Seaborn Grafikas")
        self.canvas = FigureCanvas(self.figure)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # for weather and seaborn, interactive statistical data visualization

    def get_weather(self):
        city_name = self.input_city.text()
        try:

            weather_data = get_weather(city_name)
            current_date = pd.Timestamp('now').strftime('%Y.%m.%d, %I:%M %p')
            weather_data_formatted = {
                'Data': [current_date],
                'Temperatūra': [weather_data['Temperatūra']],
                'Miestas': [weather_data['Miestas']]
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
    Weather Information for {weather_info['Miestas']}:
    ---------------------------------------------------
    Temperatūra: {weather_info['Temperatūra']} °C
    Slėgis: {weather_info['Slėgis']} hPa
    Drėgnumas: {weather_info['Drėgnumas']}%
    Vėjas: {weather_info['Vėjas']}m/s
    Aprašymas: {weather_info['Aprašymas']}
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


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec())
