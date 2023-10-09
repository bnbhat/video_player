from PyQt6.QtWidgets import QLabel, QStyle, QHBoxLayout
from PyQt6.QtCore import QTimer
from PyQt6.QtMultimedia import QMediaPlayer,  QAudioOutput
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QSlider, QVBoxLayout, QPushButton, QWidget, QMessageBox
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QMouseEvent

from clickable_slider import ClickableSlider

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Player")
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.resize(800, 600)

        self.mediaPlayer = QMediaPlayer(self)
        self.videoWidget = QVideoWidget(self)
        self.audioOutput = QAudioOutput(self)
        self.mediaPlayer.setAudioOutput(self.audioOutput)

        self.initButtons()
        self.initSliders()
        self.initLayout()
        self.applyStyles()


    def initButtons(self): 
        self.playButton = QPushButton(self)
        self.playButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.playButton.clicked.connect(self.play_pause)

        self.muteButton = QPushButton(self)
        self.muteButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))
        self.muteButton.clicked.connect(self.toggleMute)

        self.openFileButton = QPushButton(self)
        self.openFileButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
        self.openFileButton.clicked.connect(self.openFile)
        self.openFileButton.setToolTip("Open Video File")


    def initSliders(self):
        self.slider = ClickableSlider(Qt.Orientation.Horizontal, self)
        self.slider.sliderMoved.connect(self.setPosition)

        self.volumeSlider = ClickableSlider(Qt.Orientation.Horizontal, self)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.volumeSlider.setMaximumWidth(100)
        self.volumeSlider.valueChanged.connect(self.changeVolume)

        self.timeLabel = QLabel("0:00/0:00", self)

        self.fullScreenButton = QPushButton(self)
        self.fullScreenButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMaxButton))
        self.fullScreenButton.clicked.connect(self.toggleFullScreen)

    def initLayout(self):
        layout = QVBoxLayout()
        controlsLayout = QHBoxLayout()
        controlsLayout.addWidget(self.openFileButton)
        controlsLayout.addWidget(self.playButton)
        controlsLayout.addWidget(self.slider)
        controlsLayout.addWidget(self.timeLabel)
        controlsLayout.addWidget(self.volumeSlider)
        controlsLayout.addWidget(self.muteButton)
        controlsLayout.addWidget(self.fullScreenButton)        
        
        layout.addWidget(self.videoWidget)
        layout.addLayout(controlsLayout)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.errorOccurred.connect(self.handleError)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)

    def loadVideo(self, path):
        self.mediaPlayer.setSource(QUrl.fromLocalFile(path))

    def play_pause(self):
        if self.mediaPlayer.isPlaying():
            self.mediaPlayer.pause()
            self.playButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        else:
            self.mediaPlayer.play()
            self.playButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def positionChanged(self, position):
        self.slider.setValue(position)

    def durationChanged(self, duration):
        self.slider.setRange(0, duration)

    def updateTime(self):
        currentTime = self.mediaPlayer.position() // 1000
        totalTime = self.mediaPlayer.duration() // 1000
        self.timeLabel.setText(f"{currentTime // 60}:{currentTime % 60:02}/{totalTime // 60}:{totalTime % 60:02}")

    def handleError(self):
        self.playButton.setEnabled(False)
        error = self.mediaPlayer.errorString()
        print(f"Error: {error}")

    def toggleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.fullScreenButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMaxButton))
        else:
            self.showFullScreen()
            self.fullScreenButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarNormalButton))

    def openFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Videos (*.mp4)")
        if filePath:
            self.loadVideo(filePath)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.videoWidget.geometry().contains(event.position().toPoint()):
                self.play_pause()

    def changeVolume(self, value):
        """Set the volume to the specified value."""
        self.audioOutput.setVolume(value / 100.0)
        if value == 0 or self.audioOutput.isMuted():
            self.muteButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolumeMuted))
        else:
            self.muteButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))

    def toggleMute(self):
        """Toggle the mute status."""
        muted = self.audioOutput.isMuted()
        self.audioOutput.setMuted(not muted)
        if not muted:
            self.muteButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolumeMuted))
        else:
            self.muteButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))

    def keyPressEvent(self, event):
        """Override the keyPressEvent to handle the 'Esc' key."""
        if event.key() == Qt.Key.Key_Escape and self.isFullScreen():
            self.toggleFullScreen()  # Exit the full-screen mode when 'Esc' key is pressed.
        super().keyPressEvent(event)

    def applyStyles(self):
        # Set some basic styling using Qt Stylesheet
        style = """
            QMainWindow {
                background-color: #333;
            }

            QPushButton {
                background-color: #555;
                border: none;
                padding: 5px 10px;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #666;
            }

            QPushButton:pressed {
                background-color: #777;
            }

            QLabel {
                color: white;
            }
        """
        self.setStyleSheet(style)

    def closeEvent(self, event):
        """Handle the close event of the main window."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm Exit")
        msg_box.setText("Are you sure you want to close the application?")
        yes_button = msg_box.addButton("Yes", QMessageBox.ButtonRole.YesRole)
        no_button = msg_box.addButton("No", QMessageBox.ButtonRole.NoRole)

        msg_box.exec()

        if msg_box.clickedButton() == yes_button:
            event.accept()
        else:
            event.ignore()
