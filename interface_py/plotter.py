import pyqtgraph as pg
import numpy as np
from PyQt6.QtCore import Qt

class RealTimePlotter:
    def __init__(self):
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#1e1e1e')  # Fond sombre
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3) 

        # Style des axes
        self.plot_widget.getAxis('left').setPen('w')
        self.plot_widget.getAxis('bottom').setPen('w')

        # On ne crée plus de courbe factice jaune ici, 
        # on laisse update_graph gérer le tracé dynamique.

    def update_graph(self, x_data, y_data, v_lines=[], h_lines=[], oblique_lines=[]):
        """Met à jour les données de la courbe et des asymptotes instantanément."""
        # Nettoie tout le graphe précédent (courbe + lignes d'asymptotes)
        self.plot_widget.clear() 
        
        # 1. Tracé de la courbe principale
        # CRUCIAL : connect="finite" permet de "casser" la ligne sur les valeurs NaN
        self.plot_widget.plot(
            x_data, y_data, 
            pen=pg.mkPen(color='#00ffcc', width=2), # Cyan néon
            connect="finite" 
        )
        
        # 2. Ajout des asymptotes verticales
        for x_val in v_lines:
            self.plot_widget.addLine(x=x_val, pen=pg.mkPen(color='#ff4040', width=1.5, style=Qt.PenStyle.DashLine))
            
        # 3. Ajout des asymptotes horizontales
        for y_val in h_lines:
            self.plot_widget.addLine(y=y_val, pen=pg.mkPen(color='#ff4040', width=1.5, style=Qt.PenStyle.DashLine))

        # 4. Ajout des asymptotes obliques
        for slope, intercept in oblique_lines:
            y_oblique = slope * x_data + intercept
            self.plot_widget.plot(x_data, y_oblique, pen=pg.mkPen(color='#ff4040', width=1.5, style=Qt.PenStyle.DashLine))    

    def get_widget(self):
        return self.plot_widget