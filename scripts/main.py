import sys
from PyQt6.QtWidgets import QApplication
from video_player import VideoPlayer


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    filePath = "/home/balachandra/Downloads/Tutorial.mp4"
    if filePath:
        player.loadVideo(filePath)
        player.show()
        sys.exit(app.exec())
