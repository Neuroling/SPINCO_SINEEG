import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.io import wavfile
from matplotlib.mlab import psd


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main window layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Set up the file browser panel
        file_browser_layout = QVBoxLayout()
        main_layout.addLayout(file_browser_layout)

        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.plot_file)
        file_browser_layout.addWidget(self.file_list)

        browse_button = QPushButton('Browse')
        browse_button.clicked.connect(self.browse_files)
        file_browser_layout.addWidget(browse_button)

        # Set up the plot panel
        plot_layout = QVBoxLayout()
        main_layout.addLayout(plot_layout)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        plot_layout.addWidget(self.canvas)

    def browse_files(self):
        # Open a file dialog to select .wav files
        file_dialog = QFileDialog()
        file_dialog.setNameFilter('WAV files (*.wav)')
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            # Add the selected files to the file list
            for file_name in file_dialog.selectedFiles():
                self.file_list.addItem(file_name)

    def plot_file(self, item):
        # Read the selected file and plot the spectra
        file_name = item.text()
        rate, data = wavfile.read(file_name)
        self.figure.clear()
        self.figure.suptitle(os.path.basename(file_name))
        ax = self.figure.add_subplot(111)
        ax.specgram(data, Fs=rate)
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
    
     


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main window layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Set up the file browser panel
        file_browser_layout = QVBoxLayout()
        main_layout.addLayout(file_browser_layout)

        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.plot_file)
        file_browser_layout.addWidget(self.file_list)

        browse_button = QPushButton('Browse')
        browse_button.clicked.connect(self.browse_files)
        file_browser_layout.addWidget(browse_button)

        # Set up the plot panel
        plot_layout = QVBoxLayout()
        main_layout.addLayout(plot_layout)

        # Set up the toggle buttons for waveform and envelope
        toggle_layout = QHBoxLayout()
        waveform_toggle = QCheckBox('Waveform')
        waveform_toggle.stateChanged.connect(self.plot_file)
        toggle_layout.addWidget(waveform_toggle)
        envelope_toggle = QCheckBox('Envelope')
        envelope_toggle.stateChanged.connect(self.plot_file)
        toggle_layout.addWidget(envelope_toggle)
        plot_layout.addLayout(toggle_layout)

        # Add the canvas for the waveform plot
        self.waveform_canvas = FigureCanvas(Figure())
        plot_layout.addWidget(self.waveform_canvas)
        self.waveform_canvas.hide()

        # Add the canvas for the envelope plot
        self.envelope_canvas = FigureCanvas(Figure())
        plot_layout.addWidget(self.envelope_canvas)
        self.envelope_canvas.hide()

        # Add the canvas for the spectrum plot
        self.spectrum_canvas = FigureCanvas(Figure())
        plot_layout.addWidget(self.spectrum_canvas)

    def browse_files(self):
        # Open a file dialog to select .wav files
        file_dialog = QFileDialog()
        file_dialog.setNameFilter('WAV files (*.wav)')
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            # Add the selected files to the file list
            for file_name in file_dialog.selectedFiles():
                self.file_list.addItem(file_name)

    def plot_file(self, item):
        # Read the selected file and plot the waveform, envelope, and spectrum
        file_name = item.text()
        rate, data = wavfile.read(file_name)

        # Plot the spectrum
        self.spectrum_canvas.figure.clear()
        self.spectrum_canvas.figure.suptitle(os.path.basename(file_name))
        ax = self.spectrum_canvas.figure.add_subplot(111)
        ax.specgram(data, Fs=rate)
        self.spectrum_canvas.draw()

        # Plot the waveform if the waveform toggle is checked
        if self.sender() is None or self.sender().text() == 'Waveform' and self.sender().isChecked():
            self.waveform_canvas.figure.clear()
            ax = self.waveform_canvas.figure.add_subplot(111)
            ax.plot(data)
            self.waveform_canvas.draw()
            self.waveform_canvas.show()
        else:
            self.waveform_canvas.hide()

        # Plot the envelope if the envelope toggle is checked
        if self.sender() is None or self.sender().text() == 'Envelope' and self.sender().isChecked():
            self.envelope_canvas.figure.clear()
            env = np.abs(data)
            ax = self.envelope_canvas.figure.add_subplot(
