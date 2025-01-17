import os
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSlider, QRadioButton,
    QButtonGroup, QListWidget, QTextEdit, QWidget, QFileDialog, QCheckBox
)
from PyQt5.QtCore import Qt

class SongSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SongSearch")
        self.setGeometry(100, 100, 800, 600)
        self.selected_folder = None
        self.init_ui()

    def init_ui(self):
        # Layout principal
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # ----- Primera fila: Cuadros de texto y botones -----
        text_button_layout = QHBoxLayout()

        # Cuadro izquierdo: Entrada de texto
        self.input_text = QTextEdit()  # Cuadro izquierdo
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

        # Cuadro derecho: Resultados
        self.results_list = QListWidget()  # Cuadro derecho
        text_button_layout.addWidget(self.results_list)

        main_layout.addLayout(text_button_layout)

        # ----- Segunda fila: Parámetros -----
        params_layout = QGridLayout()
        params_layout.addWidget(QLabel("Parámetros de Búsqueda:"), 0, 0, 1, 2)

        # Radio buttons para elegir tipo de búsqueda
        self.artist_radio = QRadioButton("Artista")
        self.song_radio = QRadioButton("Canción")
        self.artist_radio.setChecked(True)  # Artista como predeterminado
        self.radio_group = QButtonGroup()
        self.radio_group.addButton(self.artist_radio)
        self.radio_group.addButton(self.song_radio)
        params_layout.addWidget(self.artist_radio, 1, 0)
        params_layout.addWidget(self.song_radio, 1, 1)

        # Slider para ajustar intensidad de búsqueda
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(0, 100)
        self.quality_slider.setValue(50)
        self.quality_slider.valueChanged.connect(self.update_intensity_label)  # Actualiza el porcentaje

        self.intensity_label = QLabel("Intensidad de Búsqueda: 50%")  # Etiqueta inicial
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
            ".aac": QCheckBox(".AAC")
        }
        row, col = 0, 0
        for i, checkbox in enumerate(self.file_type_checkboxes.values()):
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

        # Botón "+" para expandir/contraer el cuadro
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

        # ----- Conexión de botones -----
        self.folder_button.clicked.connect(self.select_folder)
        self.search_button.clicked.connect(self.perform_search)

    def select_folder(self):
        """Abre un cuadro de diálogo para seleccionar la carpeta."""
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if folder:
            self.selected_folder = folder
            self.log_box.append(f"Carpeta seleccionada: {folder}")

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

def perform_search(self):
    """Realiza la búsqueda de archivos según los parámetros."""
    try:
        if not self.selected_folder:
            self.log_box.append("Por favor, selecciona una carpeta antes de buscar.")
            return

        # Obtener los parámetros
        selected_formats = [ext for ext, checkbox in self.file_type_checkboxes.items() if checkbox.isChecked()]
        search_intensity = self.quality_slider.value()
        search_type = "Artista" if self.artist_radio.isChecked() else "Canción"

        # Leer las canciones proporcionadas en el cuadro izquierdo
        input_songs = self.input_text.toPlainText().strip().split("\n")
        input_songs = [song.strip().lower() for song in input_songs if song.strip()]  # Limpiar entradas

        if not input_songs:
            self.log_box.append("Por favor, introduce canciones o artistas en el cuadro izquierdo.")
            return

        # Mostrar los parámetros en el log
        self.log_box.append(f"Iniciando búsqueda con: formatos {selected_formats}, intensidad {search_intensity}%, tipo {search_type}")
        self.log_box.append(f"Canciones o artistas a buscar: {input_songs}")

        # Limpiar la lista de resultados
        self.results_list.clear()

        # Realizar la búsqueda
        found_songs = set()
        for root, _, files in os.walk(self.selected_folder):
            for file in files:
                file_ext = os.path.splitext(file)[-1].lower()
                if file_ext in selected_formats:
                    # Comparar con los nombres introducidos
                    file_name = os.path.splitext(file)[0].lower()
                    for song in input_songs:
                        if song in file_name:  # Coincidencia básica
                            found_songs.add(song)
                            self.add_result(file_name, "found", os.path.join(root, file))
                            break

        # Identificar los no encontrados
        for song in input_songs:
            if song not in found_songs:
                self.add_result(song, "not_found")

        self.log_box.append("Búsqueda completada.")
    except Exception as e:
        self.log_box.append(f"Error durante la búsqueda: {str(e)}")

    def add_result(self, name, status, path=None):
        """
        Añade un resultado a la lista con formato visual.
        :param name: Nombre del archivo o canción
        :param status: "found" para encontrado, "not_found" para no encontrado
        :param path: Ruta completa del archivo (si aplica)
        """
        item = QListWidgetItem(name)
        if status == "found":
            item.setForeground(QColor("green"))
            item.setToolTip(f"Ubicación: {path}")
        else:
            item.setForeground(QColor("red"))
            item.setToolTip("No encontrado.")
        self.results_list.addItem(item)


