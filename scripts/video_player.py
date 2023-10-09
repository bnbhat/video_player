"""Video Player Class"""
from PyQt6.QtWidgets import (
    QLabel, QMainWindow, QFileDialog, QVBoxLayout, QPushButton,
    QWidget, QMessageBox, QHBoxLayout, QStyle
)
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtGui import QMouseEvent, QColor
from clickable_slider import ClickableSlider
from utils import change_icon_color


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setupMediaPlayer()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)

    def setupUI(self):
        self.setWindowTitle("Video Player")
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.resize(800, 600)

        self.videoWidget = QVideoWidget(self)
        self.playButton = QPushButton(self)
        self.playButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.playButton.clicked.connect(self.play_pause)

        self.muteButton = QPushButton(self)
        self.muteButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))
        self.muteButton.clicked.connect(self.toggleMute)

        self.openFileButton = QPushButton(self)
        self.openFileButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
        self.openFileButton.clicked.connect(self.openFile)

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
        self.fullScreenButton.setStyleSheet("background-color: #626567")
        self.fullScreenButton.clicked.connect(self.toggleFullScreen)

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

    def setupMediaPlayer(self):
        self.firstTimeLoad = True

        self.mediaPlayer = QMediaPlayer(self)
        self.audioOutput = QAudioOutput(self)
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.errorOccurred.connect(self.handleError)
        self.mediaPlayer.mediaStatusChanged.connect(self.handleMediaStatusChanged)

    def loadVideo(self, path):
        self.mediaPlayer.setSource(QUrl.fromLocalFile(path))

    def stop(self):
        self.mediaPlayer.stop()
        self.playButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

    def play_pause(self):
        if not self.mediaPlayer.source().isValid():  # Check if a valid video source is set
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("No Video")
            msg_box.setText("No video has been selected. Please select a video first.")
            msg_box.setIcon(QMessageBox.Icon.Warning)
            upload_button = msg_box.addButton("Upload", QMessageBox.ButtonRole.YesRole)
            cancel_button = msg_box.addButton("Cancel", QMessageBox.ButtonRole.NoRole)
            msg_box.exec()
            if msg_box.clickedButton() == upload_button:
                self.openFile()
            return

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
        self.stop()
        self.firstTimeLoad = True
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Videos (*.mp4)")
        if filePath:
            self.loadVideo(filePath)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.videoWidget.geometry().contains(event.position().toPoint()):
                self.play_pause()

    def changeVolume(self, value):
        self.audioOutput.setVolume(value / 100.0)
        if value == 0 or self.audioOutput.isMuted():
            self.muteButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolumeMuted))
        else:
            self.muteButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))

    def toggleMute(self):
        self.audioOutput.setMuted(not self.audioOutput.isMuted())
        if self.audioOutput.isMuted():
            self.muteButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolumeMuted))
        else:
            self.muteButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape and self.isFullScreen():
            self.toggleFullScreen()
        elif event.key() == Qt.Key.Key_Space:
            self.play_pause()
        elif event.key() == Qt.Key.Key_F:
            self.toggleFullScreen()
        elif event.key() == Qt.Key.Key_Q:
            self.toggleFullScreen()
        super().keyPressEvent(event)

    def handleMediaStatusChanged(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.playButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
            self.mediaPlayer.setPosition(0)
        elif status == QMediaPlayer.MediaStatus.LoadedMedia:
            if self.firstTimeLoad:
                self.mediaPlayer.pause()
                self.firstTimeLoad = False

    def applyStyles(self):
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
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm Exit")
        msg_box.setText("Are you sure you want to close?  ")
        yes_button = msg_box.addButton("Yes", QMessageBox.ButtonRole.YesRole)
        no_button = msg_box.addButton("No", QMessageBox.ButtonRole.NoRole)
        msg_box.exec()

        if msg_box.clickedButton() == yes_button:
            event.accept()
        else:
            event.ignore()
