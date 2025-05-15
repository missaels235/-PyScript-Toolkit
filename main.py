# -*- coding: utf-8 -*-
import sys
import os
import webbrowser
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QProcess, QLocale, QTextCodec, QMetaObject, Qt, QSize,
                          QUrl, QRect, pyqtSlot)
from PyQt5.QtGui import (QDesktopServices, QIcon, QFont, QPalette,
                         QColor, QBrush, QPixmap)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog, QMessageBox,
                             QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit,
                             QMenuBar, QMenu, QAction, QStatusBar,
                             QListWidget, QStackedWidget, QListWidgetItem, QFrame,
                             QStyle)

# ---------------------------------------------------
# CLASE DE LA INTERFAZ (Definición de Widgets)
# ---------------------------------------------------
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(980, 700)
        self.app_version = "2.0" # Versión por cambio de tema mayor
        MainWindow.setWindowTitle(f"PyScript Toolkit v{self.app_version} - Logo Harmony")

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.mainLayout = QHBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # --- Paleta de Colores "Logo Harmony" ---
        # (Ajusta estos colores si es necesario para que coincidan EXACTAMENTE con tu logo)
        DARK_TEAL_BG = "#0D3B3F"        # Verde azulado oscuro profundo (fondo principal)
        SIDEBAR_TEAL_BG = "#0A2F33"     # Teal un poco más oscuro para sidebar
        CONTENT_PANE_BG = DARK_TEAL_BG  # Mismo que el principal para unificar
        LOGO_YELLOW = "#FFD700"       # Amarillo/Dorado del logo (Oro estándar)
        # O usa el anterior: LOGO_YELLOW = "#FFC107" # Ámbar
        LOGO_YELLOW_HOVER = "#FFDF33"   # Amarillo más brillante para hover
        LOGO_YELLOW_PRESSED = "#E0B800"  # Amarillo más oscuro para pressed
        TEXT_ON_YELLOW = "#201800"     # Texto oscuro (casi negro) para botones amarillos
        MAIN_TEXT_COLOR = "#E0F2F1"     # Blanco hueso / Cian muy pálido
        SECONDARY_TEXT_COLOR = "#A0D8D4" # Cian pálido para texto secundario/status
        INPUT_BG = "#082428"           # Fondo de inputs, más oscuro que el principal
        INPUT_BORDER = "#1E535A"       # Borde para inputs, teal medio
        BORDER_SUBTLE = "#072023"       # Borde muy sutil para separadores
        SECONDARY_BUTTON_BG = "#1E535A"   # Teal medio para botones "Examinar"
        SECONDARY_BUTTON_HOVER = "#2A7580"
        SECONDARY_BUTTON_TEXT = MAIN_TEXT_COLOR

        MainWindow.setStyleSheet(f"""
            QMainWindow {{ background-color: {DARK_TEAL_BG}; }}
            QWidget {{
                color: {MAIN_TEXT_COLOR};
                font-family: 'Segoe UI', 'Roboto', system-ui, sans-serif;
                font-size: 10pt;
            }}
            QToolTip {{
                background-color: {INPUT_BG}; color: {MAIN_TEXT_COLOR};
                border: 1px solid {INPUT_BORDER}; padding: 5px; border-radius: 3px;
            }}

            /* --- Barra Lateral --- */
            #sidebarWidget {{
                background-color: {SIDEBAR_TEAL_BG};
                border-right: 1px solid {BORDER_SUBTLE};
            }}
            #logoLabel {{
                margin-bottom: 20px; padding-top: 10px; /* Ajustar padding si es necesario */
            }}
            QListWidget#navigationList {{
                background-color: transparent; border: none;
                font-size: 11pt; outline: 0; min-height: 150px;
            }}
            QListWidget#navigationList::item {{
                padding: 14px 18px; border-radius: 5px; margin: 4px 8px;
                color: {SECONDARY_TEXT_COLOR}; /* Texto de items no seleccionados */
            }}
            QListWidget#navigationList::item:hover {{
                background-color: rgba(255, 255, 255, 0.07); /* Hover sutil */
                color: {MAIN_TEXT_COLOR};
            }}
            QListWidget#navigationList::item:selected {{
                background-color: {LOGO_YELLOW};
                color: {TEXT_ON_YELLOW};
                font-weight: 600;
            }}
            QListWidget#navigationList QScrollBar:vertical {{
                border: none; background: {SIDEBAR_TEAL_BG}; width: 8px; margin: 0;
            }}
            QListWidget#navigationList QScrollBar::handle:vertical {{
                background: {INPUT_BORDER}; border-radius: 4px; min-height: 20px;
            }}

            /* --- Área de Contenido Principal --- */
            #contentStack {{ background-color: {CONTENT_PANE_BG}; }}
            #compilerPageWidget, #obfuscatorPageWidget {{
                 background-color: transparent; /* Heredan del Stack o main window */
                 /* Si quieres un panel de contenido ligeramente diferenciado: */
                 /* background-color: rgba(10, 43, 47, 0.5); */ /* Teal muy oscuro semi-transparente */
                 /* border-radius: 8px; */
            }}
            QLabel.pageTitle {{
                font-size: 16pt; font-weight: 600; color: {MAIN_TEXT_COLOR};
                padding: 10px 0 15px 0; border-bottom: 1px solid {INPUT_BORDER};
                margin-bottom: 15px;
            }}

            /* --- Otros Widgets --- */
            QTextEdit, QLineEdit {{
                background-color: {INPUT_BG}; border: 1px solid {INPUT_BORDER};
                padding: 9px 12px; border-radius: 5px; color: {MAIN_TEXT_COLOR};
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border: 1px solid {LOGO_YELLOW}; /* Foco dorado */
                background-color: {SIDEBAR_TEAL_BG};
            }}
            QTextEdit {{ font-family: 'Consolas', 'Fira Code', 'Courier New', monospace; }}
            QTextEdit QScrollBar:vertical {{
                border: none; background: {INPUT_BG}; width: 8px; margin: 0;
            }}
            QTextEdit QScrollBar::handle:vertical {{
                background: {INPUT_BORDER}; border-radius: 4px; min-height: 20px;
            }}

            /* Botones Secundarios (Examinar) */
            QPushButton {{
                background-color: {SECONDARY_BUTTON_BG};
                color: {SECONDARY_BUTTON_TEXT};
                border: 1px solid {INPUT_BORDER};
                padding: 9px 18px; border-radius: 5px;
                min-height: 30px; font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {SECONDARY_BUTTON_HOVER};
                border-color: {LOGO_YELLOW_HOVER}; /* Borde dorado al pasar */
            }}
            QPushButton:pressed {{ background-color: {INPUT_BORDER}; }}
            QPushButton:disabled {{
                background-color: rgba(30, 83, 90, 0.5);
                color: rgba(160, 216, 212, 0.5);
                border-color: rgba(30, 83, 90, 0.3);
            }}

            /* Botones Primarios (Compilar/Ofuscar - Dorados) */
            QPushButton#btn_compile, QPushButton#btn_obfuscate {{
                background-color: {LOGO_YELLOW};
                color: {TEXT_ON_YELLOW};
                font-size: 11pt; font-weight: bold; border: none;
                padding: 10px 28px; min-height: 36px; border-radius: 5px;
            }}
            QPushButton#btn_compile:hover, QPushButton#btn_obfuscate:hover {{
                background-color: {LOGO_YELLOW_HOVER};
            }}
            QPushButton#btn_compile:pressed, QPushButton#btn_obfuscate:pressed {{
                background-color: {LOGO_YELLOW_PRESSED};
            }}
            QPushButton#btn_compile:disabled, QPushButton#btn_obfuscate:disabled {{
                background-color: rgba(255, 215, 0, 0.3);
                color: rgba(32, 24, 0, 0.4);
            }}

            QLabel {{ background-color: transparent; }}
            QLabel#label_info_dev a {{ color: {LOGO_YELLOW_HOVER}; text-decoration: none; }}
            QLabel#label_info_dev a:hover {{ text-decoration: underline; }}

            /* Menú y Status Bar */
            QMenuBar {{ background-color: {SIDEBAR_TEAL_BG}; color: {SECONDARY_TEXT_COLOR}; border-bottom: 1px solid {BORDER_SUBTLE}; }}
            QMenuBar::item {{ padding: 5px 12px; }}
            QMenuBar::item:selected {{ background-color: {INPUT_BG}; color: {MAIN_TEXT_COLOR}; }}
            QMenu {{ background-color: {INPUT_BG}; color: {MAIN_TEXT_COLOR}; border: 1px solid {BORDER_SUBTLE}; padding: 5px; }}
            QMenu::item {{ padding: 6px 18px; }}
            QMenu::item:selected {{ background-color: {SIDEBAR_TEAL_BG}; color: {MAIN_TEXT_COLOR}; border-radius: 3px; }}
            QStatusBar {{ color: {SECONDARY_TEXT_COLOR}; background-color: {SIDEBAR_TEAL_BG}; border-top: 1px solid {BORDER_SUBTLE}; }}
        """)

        self.sidebarWidget = QWidget(self.centralwidget)
        self.sidebarWidget.setObjectName("sidebarWidget")
        self.sidebarWidget.setMinimumWidth(230) # Ancho ajustado para logo más pequeño
        self.sidebarWidget.setMaximumWidth(270)
        self.sidebarLayout = QVBoxLayout(self.sidebarWidget)
        self.sidebarLayout.setContentsMargins(10, 15, 10, 15)
        self.sidebarLayout.setSpacing(15)
        self.sidebarLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.logoLabel = QLabel(self.sidebarWidget)
        self.logoLabel.setObjectName("logoLabel")
        logo_path = "logo.png"
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            # --- HACER EL LOGO MÁS PEQUEÑO ---
            # Ajusta el '160' al ancho deseado para tu logo
            pixmap = pixmap.scaledToWidth(160, Qt.TransformationMode.SmoothTransformation)
            self.logoLabel.setPixmap(pixmap)
            self.logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.logoLabel.setText("[ Logo no encontrado ]")
            self.logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.logoLabel.setStyleSheet(f"color: #FF8A80; font-style: italic;") # Rojo claro error
            print(f"Advertencia: No se encontró {logo_path}. Coloque su logo.png en la carpeta.")
        self.sidebarLayout.addWidget(self.logoLabel)

        self.navigationList = QListWidget(self.sidebarWidget)
        self.navigationList.setObjectName("navigationList")
        style = QApplication.style()
        compile_icon_std = style.standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        obfuscate_icon_std = style.standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton)
        item_compiler = QListWidgetItem(compile_icon_std, "Compilador", self.navigationList)
        item_obfuscator = QListWidgetItem(obfuscate_icon_std, "Ofuscador", self.navigationList)
        self.navigationList.setIconSize(QSize(20, 20))
        self.navigationList.setCurrentRow(0)
        self.sidebarLayout.addWidget(self.navigationList)
        self.sidebarLayout.addStretch(1)

        self.mainLayout.addWidget(self.sidebarWidget)

        self.contentStack = QStackedWidget(self.centralwidget)
        self.contentStack.setObjectName("contentStack")
        self.mainLayout.addWidget(self.contentStack, 1)

        # --- Definición de las páginas (Compilador, Ofuscador) ---
        # (El código de los widgets internos de las páginas no cambia, solo su contenedor)

        # Página 1: Compilador
        self.compilerPageWidget = QWidget()
        self.compilerPageWidget.setObjectName("compilerPageWidget")
        self.compilerPageLayout = QVBoxLayout(self.compilerPageWidget)
        self.compilerPageLayout.setContentsMargins(30, 20, 30, 30)
        self.compilerPageLayout.setSpacing(18)
        self.compilerTitleLabel = QLabel("Compilador de Scripts Python", self.compilerPageWidget)
        self.compilerTitleLabel.setProperty("class", "pageTitle")
        self.compilerPageLayout.addWidget(self.compilerTitleLabel)
        self.compilerInputLayout = QFormLayout()
        self.compilerInputLayout.setSpacing(15)
        self.compilerInputLayout.setLabelAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.compilerInputLayout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        self.label_py_file = QLabel("Archivo Python:", self.compilerPageWidget)
        self.pyPathLayout = QHBoxLayout()
        self.lineEdit_py_path = QLineEdit(self.compilerPageWidget)
        self.lineEdit_py_path.setPlaceholderText("Ruta al archivo .py")
        self.btn_browse_py = QPushButton("Examinar...", self.compilerPageWidget)
        self.pyPathLayout.addWidget(self.lineEdit_py_path, 1)
        self.pyPathLayout.addWidget(self.btn_browse_py)
        self.compilerInputLayout.addRow(self.label_py_file, self.pyPathLayout)
        self.label_icon_file = QLabel("Archivo Ícono (opc.):", self.compilerPageWidget)
        self.iconPathLayout = QHBoxLayout()
        self.lineEdit_icon_path = QLineEdit(self.compilerPageWidget)
        self.lineEdit_icon_path.setPlaceholderText("Ruta al archivo .ico")
        self.btn_browse_icon = QPushButton("Examinar...", self.compilerPageWidget)
        self.iconPathLayout.addWidget(self.lineEdit_icon_path, 1)
        self.iconPathLayout.addWidget(self.btn_browse_icon)
        self.compilerInputLayout.addRow(self.label_icon_file, self.iconPathLayout)
        self.compilerPageLayout.addLayout(self.compilerInputLayout)
        self.btn_compile = QPushButton("Compilar a EXE", self.compilerPageWidget)
        self.btn_compile.setObjectName("btn_compile") # Para estilo dorado
        self.compilerPageLayout.addWidget(self.btn_compile, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.compilerPageLayout.addSpacing(10)
        self.label_compile_status = QLabel("Salida del Proceso:", self.compilerPageWidget)
        self.textEdit_compile_output = QTextEdit(self.compilerPageWidget)
        self.textEdit_compile_output.setReadOnly(True)
        self.textEdit_compile_output.setPlaceholderText("Los mensajes y errores de PyInstaller aparecerán aquí...")
        self.textEdit_compile_output.setMinimumHeight(150)
        self.compilerPageLayout.addWidget(self.label_compile_status)
        self.compilerPageLayout.addWidget(self.textEdit_compile_output, 1)
        self.contentStack.addWidget(self.compilerPageWidget)

        # Página 2: Ofuscador
        self.obfuscatorPageWidget = QWidget()
        self.obfuscatorPageWidget.setObjectName("obfuscatorPageWidget")
        self.obfuscatorPageLayout = QVBoxLayout(self.obfuscatorPageWidget)
        self.obfuscatorPageLayout.setContentsMargins(30, 20, 30, 30)
        self.obfuscatorPageLayout.setSpacing(18)
        self.obfuscatorTitleLabel = QLabel("Ofuscador de Código Python", self.obfuscatorPageWidget)
        self.obfuscatorTitleLabel.setProperty("class", "pageTitle")
        self.obfuscatorPageLayout.addWidget(self.obfuscatorTitleLabel)
        self.obfuscatorInputLayout = QFormLayout()
        self.obfuscatorInputLayout.setSpacing(15)
        self.obfuscatorInputLayout.setLabelAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.obfuscatorInputLayout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        self.label_obf_py_file = QLabel("Archivo Python:", self.obfuscatorPageWidget)
        self.obfPyPathLayout = QHBoxLayout()
        self.lineEdit_obf_py_path = QLineEdit(self.obfuscatorPageWidget)
        self.lineEdit_obf_py_path.setPlaceholderText("Ruta al archivo .py a ofuscar")
        self.btn_browse_obf_py = QPushButton("Examinar...", self.obfuscatorPageWidget)
        self.obfPyPathLayout.addWidget(self.lineEdit_obf_py_path, 1)
        self.obfPyPathLayout.addWidget(self.btn_browse_obf_py)
        self.obfuscatorInputLayout.addRow(self.label_obf_py_file, self.obfPyPathLayout)
        self.obfuscatorPageLayout.addLayout(self.obfuscatorInputLayout)
        self.btn_obfuscate = QPushButton("Ofuscar Script", self.obfuscatorPageWidget)
        self.btn_obfuscate.setObjectName("btn_obfuscate") # Para estilo dorado
        self.obfuscatorPageLayout.addWidget(self.btn_obfuscate, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.obfuscatorPageLayout.addSpacing(10)
        self.label_obfuscate_status = QLabel("Salida del Proceso:", self.obfuscatorPageWidget)
        self.textEdit_obfuscate_output = QTextEdit(self.obfuscatorPageWidget)
        self.textEdit_obfuscate_output.setReadOnly(True)
        self.textEdit_obfuscate_output.setPlaceholderText("Los mensajes y errores de PyArmor aparecerán aquí...")
        self.textEdit_obfuscate_output.setMinimumHeight(150)
        self.obfuscatorPageLayout.addWidget(self.label_obfuscate_status)
        self.obfuscatorPageLayout.addWidget(self.textEdit_obfuscate_output, 1)
        self.contentStack.addWidget(self.obfuscatorPageWidget)

        # --- Menú Bar ---
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 980, 30))
        self.menubar.setObjectName("menubar")
        self.menuAyuda = QMenu("Ayuda", self.menubar)
        self.actionAcercaDe = QAction("Acerca de PyScript Toolkit", MainWindow)
        self.menuAyuda.addAction(self.actionAcercaDe)
        self.menubar.addAction(self.menuAyuda.menuAction())
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QMetaObject.connectSlotsByName(MainWindow)

# ---------------------------------------------------
# CLASE PRINCIPAL DE LA APLICACIÓN (Lógica)
# ---------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.process = None
        try:
            codec = QTextCodec.codecForLocale()
            self.encoding = codec.name().data().decode()
            if self.encoding.lower() == 'system': self.encoding = 'utf-8'
        except Exception: self.encoding = 'utf-8'

        self.ui.navigationList.currentRowChanged.connect(self.change_page)
        self.ui.actionAcercaDe.triggered.connect(self.show_about_dialog)

        if self.ui.navigationList.count() > 0:
            self.ui.contentStack.setCurrentIndex(0)
            self.ui.navigationList.setCurrentRow(0)

        self.ui.btn_browse_py.clicked.connect(self.browse_compile_input)
        self.ui.btn_browse_icon.clicked.connect(self.browse_icon)
        self.ui.btn_browse_obf_py.clicked.connect(self.browse_obfuscate_input)
        self.ui.btn_compile.clicked.connect(self.start_compile)
        self.ui.btn_obfuscate.clicked.connect(self.start_obfuscate)

    @pyqtSlot(int)
    def change_page(self, row):
        if 0 <= row < self.ui.contentStack.count():
             self.ui.contentStack.setCurrentIndex(row)

    @pyqtSlot()
    def show_about_dialog(self):
        # Usar colores del tema para el diálogo "Acerca de"
        LOGO_YELLOW = "#FFD700" # O el que hayas definido
        TEXT_ON_YELLOW = "#201800"
        DARK_TEAL_BG = "#0D3B3F"
        MAIN_TEXT_COLOR = "#E0F2F1"

        title = f"Acerca de PyScript Toolkit v{self.ui.app_version}"
        text = f"""
        <h3 style='color:{LOGO_YELLOW};'>PyScript Toolkit v{self.ui.app_version}</h3>
        <p style='color:{MAIN_TEXT_COLOR};'>Herramienta profesional para compilar y ofuscar scripts de Python.</p>
        <p style='color:{MAIN_TEXT_COLOR};'>Desarrollador: <a style='color: {LOGO_YELLOW_HOVER};' href='https://github.com/missaels235'>Missael S</a></p>
        <br>
        <p style='color:{SECONDARY_TEXT_COLOR};'><i>Construido con Python y PyQt5.</i></p>
        """
        about_dialog = QMessageBox(self)
        about_dialog.setWindowTitle(title)
        about_dialog.setTextFormat(Qt.TextFormat.RichText)
        about_dialog.setText(text)
        about_dialog.setIconPixmap(QPixmap("logo.png").scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)) # Icono del diálogo

        # Estilo para el diálogo QMessageBox
        about_dialog.setStyleSheet(f"""
            QMessageBox {{
                background-color: {INPUT_BG}; /* Un fondo oscuro pero no el principal */
            }}
            QMessageBox QLabel {{ /* Para el texto dentro del QMessageBox */
                color: {MAIN_TEXT_COLOR};
                background-color: transparent;
            }}
            QMessageBox QPushButton {{ /* Botón OK del diálogo */
                background-color: {LOGO_YELLOW};
                color: {TEXT_ON_YELLOW};
                padding: 8px 25px;
                border-radius: 4px;
                border: none;
                min-width: 80px;
                font-weight: bold;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {LOGO_YELLOW_HOVER};
            }}
        """)
        ok_button = about_dialog.addButton("OK", QMessageBox.ButtonRole.AcceptRole)
        about_dialog.exec_()

    # --- Resto de métodos (sin cambios lógicos) ---
    def browse_file(self, caption, filter, line_edit_widget):
        initial_dir = os.path.dirname(line_edit_widget.text()) if os.path.isfile(line_edit_widget.text()) else "."
        filePath, _ = QFileDialog.getOpenFileName(self, caption, initial_dir, filter)
        if filePath: line_edit_widget.setText(filePath)
    def browse_compile_input(self): self.browse_file("Seleccionar Script Python", "Python Files (*.py *.pyw);;All Files (*)", self.ui.lineEdit_py_path)
    def browse_icon(self): self.browse_file("Seleccionar Archivo de Ícono", "Icon Files (*.ico);;All Files (*)", self.ui.lineEdit_icon_path)
    def browse_obfuscate_input(self): self.browse_file("Seleccionar Script Python", "Python Files (*.py *.pyw);;All Files (*)", self.ui.lineEdit_obf_py_path)
    def update_status(self, message, is_error=False, target_output=None):
        status_widget = target_output if target_output else self.ui.statusbar
        if isinstance(status_widget, QStatusBar): status_widget.showMessage(message, 5000)
        elif target_output is not None: prefix = "ERROR: " if is_error else ""; target_output.append(f"--- {prefix}{message} ---")
    def handle_process_output(self, target_output):
        if not self.process or not target_output: return
        try: data = self.process.readAllStandardOutput().data().decode(self.encoding, errors='replace')
        except Exception as e: target_output.append(f"Error decodificando salida: {e}"); return
        if data: target_output.append(data.strip())
    def handle_process_error_output(self, target_output):
        if not self.process or not target_output: return
        try: data = self.process.readAllStandardError().data().decode(self.encoding, errors='replace')
        except Exception as e: target_output.append(f"Error decodificando stderr: {e}"); return
        if data: target_output.append(f"stderr: {data.strip()}")
    def on_process_finished(self, exitCode, exitStatus, button, target_output):
        output_widget = target_output if target_output else None
        if output_widget: self.handle_process_output(output_widget); self.handle_process_error_output(output_widget)
        success = (exitStatus == QProcess.ExitStatus.NormalExit and exitCode == 0)
        final_message = f"Proceso finalizado ({'Éxito' if success else 'Errores'})"
        self.update_status(final_message, is_error=not success, target_output=output_widget)
        if button: button.setEnabled(True)
        self.process = None
    def on_process_error(self, error, button, target_output):
        error_map = { QProcess.ProcessError.FailedToStart: "No se pudo iniciar (Comando no encontrado?).", QProcess.ProcessError.Crashed: "Cerrado inesperadamente.", QProcess.ProcessError.Timedout: "Tiempo agotado.", QProcess.ProcessError.ReadError: "Error lectura.", QProcess.ProcessError.WriteError: "Error escritura.", QProcess.ProcessError.UnknownError: "Error desconocido." }
        error_message = error_map.get(error, f"Error QProcess ({error}).")
        self.update_status(error_message, is_error=True, target_output=target_output if target_output else None)
        QMessageBox.critical(self, "Error de Proceso", error_message)
        if button: button.setEnabled(True)
        self.process = None
    def start_external_process(self, command, args, button, output_widget):
        if self.process is not None and self.process.state() != QProcess.ProcessState.NotRunning: QMessageBox.warning(self, "Proceso en Ejecución", "Ya hay otro proceso en ejecución."); return
        if not output_widget: print("Error: output_widget no definido"); return
        output_widget.clear(); output_widget.append(f"Ejecutando: {command} {' '.join(args)}\n" + "="*20)
        self.update_status(f"Iniciando {command}...", target_output=output_widget); self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(lambda: self.handle_process_output(output_widget)); self.process.readyReadStandardError.connect(lambda: self.handle_process_error_output(output_widget))
        self.process.finished.connect(lambda exitCode, exitStatus: self.on_process_finished(exitCode, exitStatus, button, output_widget))
        if hasattr(self.process, 'errorOccurred'): self.process.errorOccurred.connect(lambda error: self.on_process_error(error, button, output_widget))
        if button: button.setEnabled(False)
        self.process.start(command, args)
    def start_compile(self):
        file_path = self.ui.lineEdit_py_path.text().strip(); icon_path = self.ui.lineEdit_icon_path.text().strip()
        if not file_path or not os.path.isfile(file_path): QMessageBox.warning(self, "Archivo Inválido", f"Archivo Python no válido:\n{file_path}"); return
        args = ['--onefile', '--windowed', '--noconfirm', '--clean']
        if icon_path:
            if not os.path.isfile(icon_path): QMessageBox.warning(self, "Archivo Ícono Inválido", f"Archivo Ícono no válido:\n{icon_path}"); return
            args.extend(['--icon', icon_path])
        args.append(file_path); self.start_external_process("pyinstaller", args, self.ui.btn_compile, self.ui.textEdit_compile_output)
    def start_obfuscate(self):
        path = self.ui.lineEdit_obf_py_path.text().strip()
        if not path or not os.path.isfile(path): QMessageBox.warning(self, "Archivo Inválido", f"Archivo Python no válido:\n{path}"); return
        args = ['obfuscate', path]; self.start_external_process("pyarmor", args, self.ui.btn_obfuscate, self.ui.textEdit_obfuscate_output)

# ---------------------------------------------------
# PUNTO DE ENTRADA PRINCIPAL
# ---------------------------------------------------
if __name__ == "__main__":
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())