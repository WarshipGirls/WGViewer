import feedparser
import sys
from PyQt5 import QtWidgets, QtCore

class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setGeometry(200, 200, 800, 600)
        self.textLabel = QtWidgets.QLabel('')               # label showing some text
        self.uButton = QtWidgets.QPushButton('upper Button')    
        self.lButton =  QtWidgets.QPushButton('lower Button')
        self.label = QtWidgets.QLabel('')                   # label showing the news
        self.label.setAlignment(QtCore.Qt.AlignRight)           # text starts on the right
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.textLabel)
        self.layout.addWidget(self.uButton)
        self.layout.addWidget(self.lButton)
        self.layout.addWidget(self.label)
        self.layout.setStretch(0, 3)
        self.layout.setStretch(1, 3)
        self.layout.setStretch(2, 3)
        self.layout.setStretch(3, 1)         
        self.setLayout(self.layout)

        self.timeLine = QtCore.QTimeLine()  
        self.timeLine.setCurveShape(QtCore.QTimeLine.LinearCurve)                   # linear Timeline
        self.timeLine.frameChanged.connect(self.setText)
        self.timeLine.finished.connect(self.nextNews)           
        self.signalMapper = QtCore.QSignalMapper(self)
        self.signalMapper.mapped[str].connect(self.setTlText)
        self.uButton.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(self.uButton, self.uButton.text())
        self.lButton.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(self.lButton, self.lButton.text())

        self.feed()

    def feed(self):
        fm = self.label.fontMetrics()
        self.nl = int(self.label.width()/fm.averageCharWidth())     # shown stringlength
        news = []
        sports = feedparser.parse('http://rssfeeds.usatoday.com/UsatodaycomSports-TopStories')
        for e in sports['entries']:
            news.append(e.get('title', ''))
        appendix = ' '*self.nl                      # add some spaces at the end
        news.append(appendix)
        delimiter = '      +++      '                   # shown between the messages
        self.news = delimiter.join(news)
        newsLength = len(self.news)                 # number of letters in news = frameRange 
        lps = 4                                 # letters per second 
        dur = newsLength*1000/lps               # duration until the whole string is shown in milliseconds                                          
        self.timeLine.setDuration(dur)
        self.timeLine.setFrameRange(0, newsLength) 
        self.timeLine.start()

    def setText(self, number_of_frame):   
        if number_of_frame < self.nl:
            start = 0
        else:
            start = number_of_frame - self.nl
        text = '{}'.format(self.news[start:number_of_frame])        
        self.label.setText(text)

    def nextNews(self):
        self.feed()                             # start again

    def setTlText(self, text):
        string = '{} pressed'.format(text)
        self.textLabel.setText(string)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())