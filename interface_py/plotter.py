import pyqtgraph as pg
import numpy as np
from PyQt6.QtCore import Qt


class RealTimePlotter:
    def __init__(self):
        # Create a plot widget with a dark theme layout
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#1e1e1e')  # Dark
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)  # Subtle grid

        # Style the axes
        self.plot_widget.getAxis('left').setPen('w')
        self.plot_widget.getAxis('bottom').setPen('w')

        # Create a curve item with a bright neon color
        self.curve = self.plot_widget.plot(pen=pg.mkPen(color="#fff200", width=2))

    def update_graph(self, x_data, y_data, v_lines=[], h_lines=[], oblique_lines=[]):
        """Updates the line data on the screen instantly."""
        self.plot_widget.clear() # Clear previous asymptote lines
        
        # Plot the main curve
        self.plot_widget.plot(x_data, y_data, pen=pg.mkPen(color='#00ffcc', width=2))
        # Add vertical asymptotes as dashed red lines
        for x_val in v_lines:
            self.plot_widget.addLine(x=x_val, pen=pg.mkPen(color='#ff4040', width=1.5, style=Qt.PenStyle.DashLine))
        # Add horizontal asymptotes as dashed red lines
        for y_val in h_lines:
            self.plot_widget.addLine(y=y_val, pen=pg.mkPen(color='#ff4040', width=1, style=Qt.PenStyle.DashLine))

        for slope, intercept in oblique_lines:
            y_oblique = slope * x_data + intercept
            self.plot_widget.plot(x_data, y_oblique, pen=pg.mkPen(color='#ff4040', width=1, style=Qt.PenStyle.DashLine))    


    def get_widget(self):
        return self.plot_widget        

     