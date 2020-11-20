# from math import ceil

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PIL import Image


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class EquipsArray(QWidget):
    def __init__(self, parent, equips_array):
        super().__init__()

        # add your buttons
        layout = QHBoxLayout(self)

        # adjust spacings to your needs
        # layout.setContentsMargins(0,0,0,0)
        # layout.setSpacing(0)

        prefix = "src/assets/E/equip_L_"
        # # equips = list(map(int, equips_array))
        for e in equips_array:
            e = str(e)
            if e == '':
                continue
            else:
                pass
            try:
                print("what the fuck")
                print('-------------------')
                print(e)
                # img_path = prefix + str(int(float(e[3:6]))) + ".png"
                # print(img_path)
                print('-------------------')
                img = QPixmap()
                is_loaded = img.load(get_data_path(img_path))
                

                fff = Image.open(get_data_path(img_path))
                fff.show()
        #         if is_loaded:
        #             # i = QStandardItem()
        #             # i.setData(QVariant(img), Qt.DecorationRole)
        #             l = QLabel(self)
        #             l.setPixmap(img)
        #             layout.addWidget(l)
        #         else:
        #             print("NOT LOADDDDDDDD")
            except ValueError as e:
                print(e)
        layout.addWidget(QPushButton('fuck you'))
        layout.addWidget(QPushButton('fuck you'))


        self.setLayout(layout)





if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    tab = QTableView()
    sti = QStandardItemModel()
    sti.appendRow([QStandardItem(str(i)) for i in range(4)])
    sti.appendRow([QStandardItem(str(i)) for i in range(4)])
    tab.setModel(sti)
    tab.setEditTriggers(QAbstractItemView.NoEditTriggers)



    # tab.setIndexWidget(sti.index(1, 2), QPushButton("button"))
    tab.setIndexWidget(sti.index(1, 2), EquipsArray(0, [1,1,1,1]))
    header = tab.horizontalHeader()
    for i in range(sti.columnCount()):
        # QHeaderView.Stretch
        header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
    tab.show()
    sys.exit(app.exec_())

# # from PyQt4.QtCore import *
# # from PyQt4.QtGui import *


# class QtWaitingSpinner(QWidget):
#     mColor = QColor(Qt.gray)
#     mRoundness = 100.0
#     mMinimumTrailOpacity = 31.4159265358979323846
#     mTrailFadePercentage = 50.0
#     mRevolutionsPerSecond = 1.57079632679489661923
#     mNumberOfLines = 20
#     mLineLength = 10
#     mLineWidth = 2
#     mInnerRadius = 20
#     mCurrentCounter = 0
#     mIsSpinning = False

#     def __init__(self, centerOnParent=True, disableParentWhenSpinning=True, *args, **kwargs):
#         QWidget.__init__(self, *args, **kwargs)
#         self.mCenterOnParent = centerOnParent
#         self.mDisableParentWhenSpinning = disableParentWhenSpinning
#         self.initialize()

#     def initialize(self):
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.rotate)
#         self.updateSize()
#         self.updateTimer()
#         self.hide()

#     @pyqtSlot()
#     def rotate(self):
#         self.mCurrentCounter += 1
#         if self.mCurrentCounter > self.numberOfLines():
#             self.mCurrentCounter = 0
#         self.update()

#     def updateSize(self):
#         size = (self.mInnerRadius + self.mLineLength) * 2
#         self.setFixedSize(size, size)

#     def updateTimer(self):
#         self.timer.setInterval(1000 / (self.mNumberOfLines * self.mRevolutionsPerSecond))

#     def updatePosition(self):
#         if self.parentWidget() and self.mCenterOnParent:
#             self.move(self.parentWidget().width() / 2 - self.width() / 2,
#                       self.parentWidget().height() / 2 - self.height() / 2)

#     def lineCountDistanceFromPrimary(self, current, primary, totalNrOfLines):
#         distance = primary - current
#         if distance < 0:
#             distance += totalNrOfLines
#         return distance

#     def currentLineColor(self, countDistance, totalNrOfLines, trailFadePerc, minOpacity, color):
#         if countDistance == 0:
#             return color

#         minAlphaF = minOpacity / 100.0

#         distanceThreshold = ceil((totalNrOfLines - 1) * trailFadePerc / 100.0)
#         if countDistance > distanceThreshold:
#             color.setAlphaF(minAlphaF)

#         else:
#             alphaDiff = self.mColor.alphaF() - minAlphaF
#             gradient = alphaDiff / distanceThreshold + 1.0
#             resultAlpha = color.alphaF() - gradient * countDistance
#             resultAlpha = min(1.0, max(0.0, resultAlpha))
#             color.setAlphaF(resultAlpha)
#         return color

#     def paintEvent(self, event):
#         self.updatePosition()
#         painter = QPainter(self)
#         painter.fillRect(self.rect(), Qt.transparent)
#         painter.setRenderHint(QPainter.Antialiasing, True)
#         if self.mCurrentCounter > self.mNumberOfLines:
#             self.mCurrentCounter = 0
#         painter.setPen(Qt.NoPen)

#         for i in range(self.mNumberOfLines):
#             painter.save()
#             painter.translate(self.mInnerRadius + self.mLineLength,
#                               self.mInnerRadius + self.mLineLength)
#             rotateAngle = 360.0 * i / self.mNumberOfLines
#             painter.rotate(rotateAngle)
#             painter.translate(self.mInnerRadius, 0)
#             distance = self.lineCountDistanceFromPrimary(i, self.mCurrentCounter,
#                                                          self.mNumberOfLines)
#             color = self.currentLineColor(distance, self.mNumberOfLines,
#                                           self.mTrailFadePercentage, self.mMinimumTrailOpacity, self.mColor)
#             painter.setBrush(color)
#             painter.drawRoundedRect(QRect(0, -self.mLineWidth // 2, self.mLineLength, self.mLineLength),
#                                     self.mRoundness, Qt.RelativeSize)
#             painter.restore()

#     def start(self):
#         self.updatePosition()
#         self.mIsSpinning = True
#         self.show()

#         if self.parentWidget() and self.mDisableParentWhenSpinning:
#             self.parentWidget().setEnabled(False)

#         if not self.timer.isActive():
#             self.timer.start()
#             self.mCurrentCounter = 0

#     def stop(self):
#         self.mIsSpinning = False
#         self.hide()

#         if self.parentWidget() and self.mDisableParentWhenSpinning:
#             self.parentWidget().setEnabled(True)

#         if self.timer.isActive():
#             self.timer.stop()
#             self.mCurrentCounter = 0

#     def setNumberOfLines(self, lines):
#         self.mNumberOfLines = lines
#         self.updateTimer()

#     def setLineLength(self, length):
#         self.mLineLength = length
#         self.updateSize()

#     def setLineWidth(self, width):
#         self.mLineWidth = width
#         self.updateSize()

#     def setInnerRadius(self, radius):
#         self.mInnerRadius = radius
#         self.updateSize()

#     def color(self):
#         return self.mColor

#     def roundness(self):
#         return self.mRoundness

#     def minimumTrailOpacity(self):
#         return self.mMinimumTrailOpacity

#     def trailFadePercentage(self):
#         return self.mTrailFadePercentage

#     def revolutionsPersSecond(self):
#         return self.mRevolutionsPerSecond

#     def numberOfLines(self):
#         return self.mNumberOfLines

#     def lineLength(self):
#         return self.mLineLength

#     def lineWidth(self):
#         return self.mLineWidth

#     def innerRadius(self):
#         return self.mInnerRadius

#     def isSpinning(self):
#         return self.mIsSpinning

#     def setRoundness(self, roundness):
#         self.mRoundness = min(0.0, max(100, roundness))

#     def setColor(self, color):
#         self.mColor = color

#     def setRevolutionsPerSecond(self, revolutionsPerSecond):
#         self.mRevolutionsPerSecond = revolutionsPerSecond
#         self.updateTimer()

#     def setTrailFadePercentage(self, trail):
#         self.mTrailFadePercentage = trail

#     def setMinimumTrailOpacity(self, minimumTrailOpacity):
#         self.mMinimumTrailOpacity = minimumTrailOpacity


# if __name__ == '__main__':
#     import sys

#     app = QApplication(sys.argv)
#     dial = QDialog()
#     w = QtWaitingSpinner(dial)
#     dial.show()
#     w.start()
#     QTimer.singleShot(1000, w.stop)
#     sys.exit(app.exec_())