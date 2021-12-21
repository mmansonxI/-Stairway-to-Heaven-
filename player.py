import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaContent,QMediaPlayer
from PyQt5.QtCore import QUrl, QUrlQuery
from PyQt5 import QtCore

class MP3Player(QWidget):
    def __init__(self):
        super().__init__()

        self.state = "Play"
        self.playlist = []
        self.position = 0

        self.init_ui()


    def init_ui(self):
        vb = QVBoxLayout()
        self.setLayout(vb)
        vb.setAlignment(QtCore.Qt.AlignCenter)


        self.label = QLabel("MP3 Player")
        self.label.setFont(QFont("Calibri",20 ))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        vb.addWidget(self.label)

        hb = QHBoxLayout()
        vb.addLayout(hb)

        font = QFont("Calibri", 14)
        self.backwardbtn = QPushButton()
        self.backwardbtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        hb.addWidget(self.backwardbtn)

        self.playbtn = QPushButton('Play',self)
        self.playbtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playbtn.setFont(font)
        hb.addWidget(self.playbtn)

        self.forwardbtn = QPushButton()
        self.forwardbtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.forwardbtn.setFont(font)
        hb.addWidget(self.forwardbtn)


        hb2 = QHBoxLayout()
        vb.addLayout(hb2)

        self.openfilebtn = QPushButton()
        self.openfilebtn.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        self.openfilebtn.setFont(font)
        hb2.addWidget(self.openfilebtn)

        self.slider = QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)
        hb2.addWidget(self.slider)

        self.songlist = QListWidget()
        vb.addWidget(self.songlist)

        self.toolbar = QToolBar()
        vb.addWidget(self.toolbar)

        self.openfileaction = QAction()
        self.openfileaction.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        self.openfileaction.setFont(font)
        self.toolbar.addAction(self.openfileaction)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()

        self.player = QMediaPlayer()

        self.openfilebtn.clicked.connect(self.open_mp3_file)
        self.playbtn.clicked.connect(self.play_mp3)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        self.player.stateChanged.connect(self.state_changed)
        self.backwardbtn.clicked.connect(self.move_backward)
        self.forwardbtn.clicked.connect(self.move_forward)


    def open_mp3_file(self):
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        names = file_name.getOpenFileNames(self,"Open files", os.getenv("HOME"))
        self.song = names[0]
        self.songlist.addItems(self.song)


    def play_mp3(self):
        if self.state == "Play":
            self.playbtn.setText("Pause")
            self.state = "Pause"
            path = self.songlist.currentItem().text()
            url = QUrl.fromLocalFile(path)
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.player.setPosition(self.position)
            self.playlist.append(path)
            if len(self.playlist) > 2:
                self.playlist.pop(0)
            if self.songlist.currentItem().text() != self.playlist[0]:
                self.position = 0
                self.player.setPosition(self.position)
            self.player.play()
        else:
            self.playbtn.setText("Play")
            self.state = "Play"
            self.player.pause()
            paused = self.player.position()
            self.position = paused

    def set_position(self, position):
        self.player.setPosition(position)


    def position_changed(self,position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def state_changed(self, state):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.playbtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playbtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def move_forward(self):
        self.player.setPosition(int(self.player.position()) + 2000)

    def move_backward(self):
        self.player.setPosition(int(self.player.position()) - 2000)

def main():
    app = QApplication(sys.argv)
    gui = MP3Player()
    gui.setGeometry(600,200,600,700)
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()