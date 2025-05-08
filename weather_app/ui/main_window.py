from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QPushButton,
    QHBoxLayout, QSizePolicy, QLineEdit, QColorDialog, QFileDialog
)
from PyQt6.QtCore import QTimer
from weather_app.gl.model_widget import ModelWidget
from weather_app.services.weather_service import WeatherService


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test task for Avrora, from Timur")

        self.weather_service = WeatherService("Poltava")

        self.init_ui()

        self.bind_signals()

        self.update_weather()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_weather)
        self.timer.start(300_000)

    def init_ui(self):
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        self.gl_widget = ModelWidget()
        self.gl_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.weather_panel = QWidget()
        self.weather_panel.setFixedWidth(220)
        panel_layout = QVBoxLayout(self.weather_panel)
        panel_layout.setContentsMargins(10, 10, 10, 10)

        self.temp_label = QLabel()
        self.city_name = QLabel()
        self.icon_label = QLabel()

        self.city_input = QLineEdit("Poltava")
        self.city_input.setPlaceholderText("Введіть місто")

        self.color_btn = QPushButton("Змінити колір")
        self.change_city_btn = QPushButton("Змінити місто")
        self.reset_btn = QPushButton("Скинути положення")
        self.update_weather_btn = QPushButton("Оновити погоду")
        self.load_model_btn = QPushButton("Завантажити модель")

        panel_layout.addWidget(self.temp_label)
        panel_layout.addWidget(self.city_name)
        panel_layout.addWidget(self.icon_label)
        panel_layout.addWidget(self.city_input)
        panel_layout.addWidget(self.change_city_btn)
        panel_layout.addStretch()
        panel_layout.addWidget(self.update_weather_btn)
        panel_layout.addWidget(self.reset_btn)
        panel_layout.addWidget(self.color_btn)
        panel_layout.addWidget(self.load_model_btn)

        main_layout.addWidget(self.gl_widget, stretch=1)
        main_layout.addWidget(self.weather_panel)

        self.setCentralWidget(central_widget)

    def bind_signals(self):
        self.update_weather_btn.clicked.connect(self.update_weather)
        self.reset_btn.clicked.connect(self.gl_widget.reset_view)
        self.change_city_btn.clicked.connect(self.change_city)
        self.color_btn.clicked.connect(self.choose_color)
        self.load_model_btn.clicked.connect(self.load_model)

    def update_weather(self):
        temp, icon_url, city_name = self.weather_service.fetch_weather()
        self.temp_label.setText(f"Температура: {temp}°C")
        self.city_name.setText(f"Місто: {city_name}")
        self.icon_label.setText(f"Значок: {icon_url}")

    def change_city(self):
        new_city = self.city_input.text().strip()
        if new_city:
            self.weather_service.city = new_city
            self.update_weather()

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            r = color.red() / 255
            g = color.green() / 255
            b = color.blue() / 255
            self.gl_widget.model_color = (r, g, b)
            self.gl_widget.update()

    def load_model(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Виберіть .obj модель", "", "OBJ Files (*.obj)"
        )
        if file_path:
            self.gl_widget.load_new_model(file_path)
