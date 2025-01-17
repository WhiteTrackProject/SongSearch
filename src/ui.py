import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QTextEdit, QPushButton, QSlider, QRadioButton,
    QButtonGroup, QListWidget, QWidget, QFileDialog, QCheckBox, QListWidgetItem
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from database_manager import DatabaseManager  # Asegúrate de tener este archivo creado


class SongSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()  # Manejo de la base de datos
        self.setWindowTitle("SongSearch")
        self.setGeometry(100, 100, 800, 600)
        self.selected_folder = None
        self.player = QMediaPlayer()  # Reproductor multimedia
        self.init_ui()

    def init_ui(self):
        # Layout principal
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # ----- Primera fila: Cuadros de texto y botones -----
        text_button_layout = QHBoxLayout()

        # Cuadro izquierdo: Entrada de texto
        self.input_text = QTextEdit()
        text_button_layout.addWidget(self.input_text)

        # Botones en el centro
        button_layout = QVBoxLayout()
        self.search_button = QPushButton("Buscar")
        self.export_button = QPushButton("Exportar a Rekordbox")
        self.folder_button = QPushButton("Elegir Carpeta")
        self.update_button = QPushButton("Actualizar Base de Datos")
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.folder_button)
        button_layout.addWidget(self.update_button)
        text_button_layout.addLayout(button_layout)

        # Conexión del botón de actualización
        self.update_button.clicked.connect(self.update_database)

        # Cuadro derecho: Resultados
        self.results_list = QListWidget()
        text_button_layout.addWidget(self.results_list)

        main_layout.addLayout(text_button_layout)

        # ----- Segunda fila: Parámetros -----
        params_layout = QGridLayout()
        params_layout.addWidget(QLabel("Parámetros de Búsqueda:"), 0, 0, 1, 2)

        # Radio buttons para tipo de búsqueda
        self.artist_radio = QRadioButton("Artista")
        self.song_radio = QRadioButton("Canción")
        self.artist_radio.setChecked(True)
        self.radio_group = QButtonGroup()
        self.radio_group.addButton(self.artist_radio)
        self.radio_group.addButton(self.song_radio)
        params_layout.addWidget(self.artist_radio, 1, 0)
        params_layout.addWidget(self.song_radio, 1, 1)

        # Slider para ajustar intensidad
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(0, 100)
        self.quality_slider.setValue(50)
        self.quality_slider.valueChanged.connect(self.update_intensity_label)

        self.intensity_label = QLabel("Intensidad de Búsqueda: 50%")
        params_layout.addWidget(self.intensity_label, 2, 0)
        params_layout.addWidget(self.quality_slider, 2, 1)

        # Casillas de verificación para formatos de archivo
        params_layout.addWidget(QLabel("Formatos de Archivo:"), 3, 0, 1, 2)
        file_type_grid = QGridLayout()
        self.file_type_checkboxes = {
            ".mp3": QCheckBox(".MP3"),
            ".flac": QCheckBox(".FLAC"),
            ".wav": QCheckBox(".WAV"),
            ".aiff": QCheckBox(".AIFF"),
            ".ogg": QCheckBox(".OGG"),
            ".aac": QCheckBox(".AAC"),
        }
        row, col = 0, 0
        for checkbox in self.file_type_checkboxes.values():
            checkbox.setChecked(True)
            file_type_grid.addWidget(checkbox, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
        params_layout.addLayout(file_type_grid, 4, 0, 1, 2)

        main_layout.addLayout(params_layout)

        # ----- Tercera fila: Log de procesos -----
        log_layout = QVBoxLayout()
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setFixedHeight(50)

        self.expand_log_button = QPushButton("+")
        self.expand_log_button.setFixedSize(20, 20)
        self.expand_log_button.clicked.connect(self.toggle_log_size)

        log_with_button = QHBoxLayout()
        log_with_button.addWidget(self.log_box)
        log_with_button.addWidget(self.expand_log_button, alignment=Qt.AlignTop)

        log_layout.addLayout(log_with_button)
        main_layout.addLayout(log_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Conexión de botones y eventos
        self.folder_button.clicked.connect(self.select_folder)
        self.search_button.clicked.connect(self.perform_search)
        self.results_list.itemDoubleClicked.connect(self.handle_double_click)

    def update_database(self):
        """Actualiza la base de datos con las canciones de las carpetas seleccionadas."""
        try:
            if not self.selected_folder:
                folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta para Actualización")
                if folder:
                    self.selected_folder = folder
                    self.log_box.append(f"Carpeta seleccionada para actualización: {folder}")
                else:
                    self.log_box.append("No se seleccionó ninguna carpeta. No se puede actualizar la base de datos.")
                    return

            self.log_box.append("Actualizando la base de datos...")
            song_count = 0

            for root, _, files in os.walk(self.selected_folder):
                for file in files:
                    file_name, file_ext = os.path.splitext(file)
                    if file_ext.lower() in self.file_type_checkboxes:
                        path = os.path.join(root, file)
                        size = os.path.getsize(path)
                        modified_date = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")
                        self.db_manager.add_song(
                            name=file_name,
                            artist=None,
                            path=path,
                            duration=None,
                            file_format=file_ext,
                            size=size,
                            modified_date=modified_date,
                        )
                        song_count += 1

            self.log_box.append(f"Base de datos actualizada con {song_count} canciones nuevas.")
        except Exception as e:
            self.log_box.append(f"Error durante la actualización de la base de datos: {str(e)}")

    def perform_search(self):
        """Realiza la búsqueda de archivos según los parámetros."""
        try:
            input_songs = self.input_text.toPlainText().strip().split("\n")
            input_songs = [song.strip().lower() for song in input_songs if song.strip()]
            if not input_songs:
                self.log_box.append("Por favor, introduce canciones o artistas en el cuadro izquierdo.")
                return

            self.log_box.append("Buscando canciones...")
            found_in_db = []
            for query in input_songs:
                results = self.db_manager.search_song(query)
                if results:
                    for result in results:
                        self.add_result(result[1], "found", result[3])
                        found_in_db.append(query)

            to_search = [song for song in input_songs if song not in found_in_db]
            if to_search:
                self.log_box.append(f"Buscando en el sistema de archivos: {to_search}")
                self.search_in_filesystem(to_search)

            self.log_box.append("Búsqueda completada.")
        except Exception as e:
            self.log_box.append(f"Error durante la búsqueda: {str(e)}")

    def search_in_filesystem(self, to_search):
        """Busca canciones en el sistema de archivos y las añade a la base de datos."""
        try:
            found_songs = set()
            for root, _, files in os.walk(self.selected_folder):
                for file in files:
                    file_name, file_ext = os.path.splitext(file)
                    if file_ext.lower() in self.file_type_checkboxes and file_name.lower() in to_search:
                        path = os.path.join(root, file)
                        size = os.path.getsize(path)
                        modified_date = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")
                        self.db_manager.add_song(file_name, None, path, None, file_ext, size, modified_date)
                        self.add_result(file_name, "found", path)
                        found_songs.add(file_name)

            for song in to_search:
                if song not in found_songs:
                    self.add_result(song, "not_found")
        except Exception as e:
            self.log_box.append(f"Error al buscar en el sistema de archivos: {str(e)}")

    def handle_double_click(self, item):
        """Gestiona el doble clic en los resultados."""
        if item.foreground().color().name() == "#008000":
            self.play_song(item.toolTip())
        elif item.foreground().color().name() == "#ff0000":
            self.assign_song_location(item)

    def play_song(self, file_path):
        """Reproduce la canción seleccionada."""
        if not file_path or not os.path.exists(file_path):
            self.log_box.append("El archivo no existe o no está disponible.")
            return
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.player.play()
        self.log_box.append(f"Reproduciendo: {file_path}")

    def assign_song_location(self, item):
        """Abre un cuadro de diálogo para asignar manualmente la ubicación de una canción."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo")
        if file_path:
            item.setForeground(QColor("green"))
            item.setToolTip(file_path)
            self.log_box.append(f"Archivo asignado manualmente: {file_path}")

    def update_intensity_label(self):
        """Actualiza la etiqueta del porcentaje del slider."""
        value = self.quality_slider.value()
        self.intensity_label.setText(f"Intensidad de Búsqueda: {value}%")

    def toggle_log_size(self):
        """Cambia el tamaño del cuadro de sucesos."""
        if self.log_box.height() == 50:
            self.log_box.setFixedHeight(150)
            self.expand_log_button.setText("-")
        else:
            self.log_box.setFixedHeight(50)
            self.expand_log_button.setText("+")

    def add_result(self, name, status, path=None):
        """Añade un resultado a la lista con formato visual."""
        item = QListWidgetItem(name)
        if status == "found":
            item.setForeground(QColor("green"))
            item.setToolTip(f"Ubicación: {path}")
        else:
            item.setForeground(QColor("red"))
            item.setToolTip("No encontrado.")
        self.results_list.addItem(item)
