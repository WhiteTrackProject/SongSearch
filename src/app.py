# src/app.py
from PyQt5.QtWidgets import QApplication
from ui import SongSearchApp
import sys

def main():
    """Punto de entrada principal para la aplicación SongSearch."""
    # Crear la instancia de la aplicación Qt
    app = QApplication(sys.argv)
    
    # Crear e inicializar la ventana principal
    window = SongSearchApp()
    window.show()
    
    # Ejecutar el bucle principal de la aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
