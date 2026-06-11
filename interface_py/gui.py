import matplotlib
matplotlib.use('Agg')  # CRUCIAL : Force un backend sans conflit avec PyQt6
import matplotlib.pyplot as plt
import io
from PyQt6.QtWidgets import QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QSlider, QLabel, QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from plotter import RealTimePlotter

class MainWindow(QMainWindow):
    def __init__(self, c_engine_callback):
        super().__init__()
        self.setWindowTitle("MathTwin - Symbolic Math Analyzer")
        self.resize(1100, 700)
        
        self.calculate_math = c_engine_callback

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Panel de gauche déroulant
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedWidth(400)
        
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        
        control_layout.addWidget(QLabel("Type your function naturally (e.g., 2x^2 + e^x):"))
        self.func_input = QLineEdit("2x^2 - 3x + sin(x)")
        self.func_input.setStyleSheet("font-size: 14px; padding: 6px; font-family: Consolas;")
        self.func_input.textChanged.connect(self.on_inputs_changed)
        control_layout.addWidget(self.func_input)

        self.btn_analyze = QPushButton("Analyser la fonction")
        self.btn_analyze.setStyleSheet("padding: 6px; font-weight: bold; font-size: 13px;")
        self.btn_analyze.clicked.connect(self.on_inputs_changed)
        control_layout.addWidget(self.btn_analyze)

        control_layout.addWidget(QLabel("Adjust X Max Range:"))
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(50)
        self.slider.setValue(10)
        self.slider.valueChanged.connect(self.on_inputs_changed)
        control_layout.addWidget(self.slider)

        control_layout.addSpacing(15)
        
        # Labels d'affichage mathématique
        control_layout.addWidget(QLabel("📝 MATHEMATICAL INTERPRETATION:"))
        self.lbl_preview = QLabel() 
        control_layout.addWidget(self.lbl_preview)

        control_layout.addWidget(QLabel("🌐 DOMAIN OF DEFINITION (DF):"))
        self.lbl_domain = QLabel() 
        control_layout.addWidget(self.lbl_domain)

        control_layout.addWidget(QLabel("📈 LIMITS AT INFINITY:"))
        self.lbl_limits = QLabel()
        control_layout.addWidget(self.lbl_limits)

        control_layout.addWidget(QLabel("📐 DERIVATIVE f'(x):"))
        self.lbl_derivative = QLabel() 
        control_layout.addWidget(self.lbl_derivative)

        control_layout.addWidget(QLabel("∫ PRIMITIVE F(x):"))
        self.lbl_primitive = QLabel() 
        control_layout.addWidget(self.lbl_primitive)

        control_layout.addWidget(QLabel("⚖️ PARITÉ & SYMÉTRIE:"))
        self.lbl_parity = QLabel()
        control_layout.addWidget(self.lbl_parity)

        control_layout.addWidget(QLabel("🕳️ PROLONGEMENT PAR CONTINUITÉ:"))
        self.lbl_extension = QLabel()
        control_layout.addWidget(self.lbl_extension)

        control_layout.addWidget(QLabel("🛑 ÉQUATIONS DES ASYMPTOTES:"))
        self.lbl_asymptote = QLabel()
        control_layout.addWidget(self.lbl_asymptote)

        control_layout.addStretch()
        scroll.setWidget(control_panel)
        main_layout.addWidget(scroll)

        # Panel de droite : Graphe
        self.plotter = RealTimePlotter()
        main_layout.addWidget(self.plotter.get_widget())

    def render_math_to_label(self, label, math_text, text_color="00ffcc"):
        """Génère proprement l'image LaTeX mémoire sans blocage."""
        try:
            fig = plt.figure(figsize=(4.5, 0.5), facecolor='#252526')
            fig.text(0.05, 0.3, math_text, color=text_color, fontsize=12)

            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.05, dpi=120, facecolor=fig.get_facecolor())
            plt.close(fig)
            buf.seek(0)

            qimg = QImage.fromData(buf.getvalue())
            pixmap = QPixmap.fromImage(qimg)
            label.setPixmap(pixmap)
        except Exception:
            label.setText("Erreur de rendu LaTeX.")

    def on_inputs_changed(self):
        expression_text = self.func_input.text()
        max_x = float(self.slider.value())
        
        # Récupération des calculs du moteur de math
        data = self.calculate_math(expression_text, max_x)
        if not data:
            return

        # Mise à jour des affichages textuels LaTeX (sans doublons de chaînes)
        self.render_math_to_label(self.lbl_preview, f"$f(x) = {data['math_preview']}$", '#39ff14')
        self.render_math_to_label(self.lbl_domain, f"${data['domain_text']}$", '#00ffcc')
        self.render_math_to_label(self.lbl_derivative, f"$f'(x) = {data['derivative_text']}$", '#ffcc00')
        self.render_math_to_label(self.lbl_primitive, f"$F(x) = {data['primitive_text']}$", '#ff007f')
        self.render_math_to_label(self.lbl_limits, f"${data['limits_text']}$", '#00ffcc')
        self.render_math_to_label(self.lbl_parity, f"${data['parity_txt']}$", '#ffffff')
        self.render_math_to_label(self.lbl_extension, f"${data['extension_txt']}$", '#ffaf40')
        self.render_math_to_label(self.lbl_asymptote, f"${data['asymptote_txt']}$", '#00ffcc')

        # Envoi direct des tableaux de données au Plotter
        self.plotter.update_graph(
            data["x_data"], data["y_data"],
            data["v_lines"], data["h_lines"], data["oblique_lines"]
        )