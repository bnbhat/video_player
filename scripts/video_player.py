from PyQt6.QtWidgets import QLabel, QStyle, QHBoxLayout
from PyQt6.QtCore import QTimer
from PyQt6.QtMultimedia import QMediaPlayer,  QAudioOutput
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QSlider, QVBoxLayout, QPushButton, QWidget
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QMouseEvent

from clickable_slider import ClickableSlider

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")

        self.mediaPlayer = QMediaPlayer(self)
        self.videoWidget = QVideoWidget(self)
        self.audioOutput = QAudioOutput(self)

        self.playButton = QPushButton(self)
        self.playButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.playButton.clicked.connect(self.play_pause)

        self.slider = ClickableSlider(Qt.Orientation.Horizontal, self)
        self.slider.sliderMoved.connect(self.setPosition)

        self.volumeSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.mediaPlayer.setAudioOutput(self.mediaPlayer.audioOutput())
        #self.mediaPlayer.
        #self.volumeSlider.sliderMoved.connect(self.mediaPlayer.setVolume)

        self.currentTimeLabel = QLabel("0:00", self)
        self.totalTimeLabel = QLabel("/0:00", self)

        self.fullScreenButton = QPushButton("Full Screen", self)
        self.fullScreenButton.clicked.connect(self.toggleFullScreen)

        self.openFileButton = QPushButton("Open File", self)
        self.openFileButton.clicked.connect(self.openFile)

        layout = QVBoxLayout()
        controlsLayout = QHBoxLayout()
        controlsLayout.addWidget(self.openFileButton)
        controlsLayout.addWidget(self.playButton)
        controlsLayout.addWidget(self.currentTimeLabel)
        controlsLayout.addWidget(self.slider)
        controlsLayout.addWidget(self.totalTimeLabel)
        controlsLayout.addWidget(self.volumeSlider)
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
        self.currentTimeLabel.setText(f"{currentTime // 60}:{currentTime % 60:02}")
        self.totalTimeLabel.setText(f"/{totalTime // 60}:{totalTime % 60:02}")

    def handleError(self):
        self.playButton.setEnabled(False)
        error = self.mediaPlayer.errorString()
        print(f"Error: {error}")

    def toggleFullScreen(self):
        if self.videoWidget.isFullScreen():
            self.videoWidget.setFullScreen(False)
        else:
            self.videoWidget.setFullScreen(True)

    def openFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Videos (*.mp4)")
        if filePath:
            self.loadVideo(filePath)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.videoWidget.geometry().contains(event.position().toPoint()):
                self.play_pause()

