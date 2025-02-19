
from PyQt5.QtWidgets import QWidget, QMainWindow ,QApplication,QPushButton,QTabBar,QStylePainter,QStyleOptionTab,QStyle,QMessageBox
from PyQt5.QtGui import QFont,QCloseEvent
from PyQt5.QtCore import Qt,pyqtSignal ,QSize ,QRect ,QPoint 
from utils.config import _TR

import qtawesome 

def getQMessageBox(parent=None,title="",text="",useok=True,usecancel=False,okcallback=None,cancelcallback=None):
    msgBox=QMessageBox(parent)
    msgBox.setWindowTitle(_TR(title))
    msgBox.setText(_TR(text)) 
    btn=0
    if useok:btn|=QMessageBox.Ok
    if usecancel:btn|=QMessageBox.Cancel

    msgBox.setStandardButtons(btn)
    msgBox.setDefaultButton(QMessageBox.Ok)
    ret=msgBox.exec()
    
    if ret==QMessageBox.Ok and okcallback:
        okcallback()
    elif ret==QMessageBox.Cancel and cancelcallback:
        cancelcallback()
class closeashidewindow(QMainWindow): 
    showsignal=pyqtSignal() 
    realshowhide=pyqtSignal(bool)
    def __init__(self, args,dic=None,key=None) -> None:
        super().__init__(args )
        self.showsignal.connect(self.showfunction)  
        self.realshowhide.connect(self.realshowhidefunction)
        d=QApplication.desktop()
        self.dic,self.key=dic,key
        if self.dic:
            dic[key][0]=min(max(dic[key][0],0),d.width()-dic[key][2])
            dic[key][1]=min(max(dic[key][1],0),d.height()-dic[key][3])
            self.setGeometry(*dic[key])
    def realshowhidefunction(self,show):
        if show:
            self.showNormal()
        else:
            self.hide()
    def showfunction(self): 
        if self.isMinimized():
            self.showNormal() 
        elif self.isHidden(): 
            self.show()  
        else:
            self.hide()  
    def resizeEvent(self, a0 ) -> None:
        if self.dic:
            if self.isMaximized()==False: 
                self.dic[self.key]=list(self.geometry().getRect())
    def moveEvent(self, a0 ) -> None:
        if self.dic:
            if self.isMaximized()==False: 
                self.dic[self.key]=list(self.geometry().getRect())
    def closeEvent(self, event:QCloseEvent) :  
        self.hide() 
        event.ignore() 
        if self.dic:
            if self.isMaximized()==False: 
                self.dic[self.key]=list(self.geometry().getRect())

class MySwitch(QPushButton): 
    def __init__(self,rate, parent = None,sign=True ,enable=True):
        super().__init__(parent) 
        
        self.setStyleSheet('''background-color: rgba(255, 255, 255, 0);
          color: black;
          border: 0px;
          font: 100 10pt;''')
        self.rate= rate
        self.clicked.connect(self.setChecked)
        self.setIconSize(QSize(int(25*self.rate),
                                 int(25*self.rate)))  
        self.setEnabled(enable)
        self.setCheckable(True)
        self.setChecked(sign)  
    def setChecked(self,  a0)  :
        super().setChecked(a0) 
        self.setIcon(qtawesome.icon("fa.check" ,color="#FF69B4") if a0 else qtawesome.icon("fa.times" ,color='#dadbdc'))

class resizableframeless(QWidget):
    def __init__(self, parent , flags ) -> None:
        super().__init__(parent, flags)
        self.setMouseTracking(True)  
        
        self._padding = 10
        # 设置鼠标跟踪判断扳机默认值
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._lcorner_drag = False
        self._right_drag = False
        self._left_drag = False
        
    
    def isinrect(self,pos,rect):
        x,y=pos.x(),pos.y()
        x1,x2,y1,y2=rect
        return x>=x1 and x<=x2 and y<=y2 and y>=y1
    def resizeEvent(self, e):
        
        if self._move_drag ==False: 
            self._right_rect = [self.width() - self._padding, self.width() + 1 ,0, self.height() - self._padding]
            self._left_rect = [-1, self._padding,0, self.height() - self._padding]
            self._bottom_rect = [self._padding, self.width() - self._padding,self.height() - self._padding, self.height() + 1]
            self._corner_rect = [self.width() - self._padding, self.width() + 1,self.height() - self._padding, self.height() + 1]
            self._lcorner_rect = [-1, self._padding,self.height() - self._padding, self.height() + 1]
    
    def mousePressEvent(self, event):
        # 重写鼠标点击的事件 
         
        if (event.button() == Qt.LeftButton) and (self.isinrect(event.pos(), self._corner_rect)):
            # 鼠标左键点击右下角边界区域
            self._corner_drag = True 
        elif (event.button() == Qt.LeftButton) and (self.isinrect(event.pos(),self._right_rect)):
            # 鼠标左键点击右侧边界区域
            self._right_drag = True 
        elif (event.button() == Qt.LeftButton) and (self.isinrect(event.pos(),self._left_rect)):
            # 鼠标左键点击右侧边界区域
            self._left_drag = True 
            self.startxp=(event.globalPos() - self.pos() ) 
            self.startx=event.globalPos().x()
            self.startw=self.width()
        elif (event.button() == Qt.LeftButton) and (self.isinrect(event.pos(),self._bottom_rect)):
            # 鼠标左键点击下侧边界区域
            self._bottom_drag = True 
        elif (event.button() == Qt.LeftButton) and (self.isinrect(event.pos(),self._lcorner_rect)):
            # 鼠标左键点击下侧边界区域
            self._lcorner_drag = True 
            self.startxp=(event.globalPos() - self.pos() ) 
            self.startx=event.globalPos().x()
            self.startw=self.width()
        # and (event.y() < self._TitleLabel.height()):
        elif (event.button() == Qt.LeftButton):
            # 鼠标左键点击标题栏区域
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos() 

    def mouseMoveEvent(self, QMouseEvent):
        # 判断鼠标位置切换鼠标手势 
        
        pos=QMouseEvent.pos()
         
        if self._move_drag ==False:
            if self.isinrect( pos,self._corner_rect):
                self.setCursor(Qt.SizeFDiagCursor)
            elif self.isinrect( pos,self._lcorner_rect):
                self.setCursor(Qt.SizeBDiagCursor)
            elif self.isinrect(pos ,self._bottom_rect):
                self.setCursor(Qt.SizeVerCursor)
            elif self.isinrect(pos ,self._right_rect):
                self.setCursor(Qt.SizeHorCursor)
            elif self.isinrect(pos ,self._left_rect):
                self.setCursor(Qt.SizeHorCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
        if Qt.LeftButton and self._right_drag:
            
            # 右侧调整窗口宽度
            self.resize(pos.x(), self.height())
        elif Qt.LeftButton and self._left_drag:
            # 右侧调整窗口宽度  
            self.setGeometry((QMouseEvent.globalPos() - self.startxp).x(),self.y(),self.startw-(QMouseEvent.globalPos().x() - self.startx),self.height())
            #self.resize(pos.x(), self.height())
        elif Qt.LeftButton and self._bottom_drag:
            # 下侧调整窗口高度
            self.resize(self.width(), QMouseEvent.pos().y()) 
        elif Qt.LeftButton and self._lcorner_drag:
            # 下侧调整窗口高度
            self.setGeometry((QMouseEvent.globalPos() - self.startxp).x(),self.y(),self.startw-(QMouseEvent.globalPos().x() - self.startx),QMouseEvent.pos().y())
        elif Qt.LeftButton and self._corner_drag:
            # 右下角同时调整高度和宽度
            self.resize(pos.x(),pos.y()) 
        elif Qt.LeftButton and self._move_drag:
            # 标题栏拖放窗口位置
            self.move(QMouseEvent.globalPos() - self.move_DragPosition) 

    def mouseReleaseEvent(self, QMouseEvent):
        # 鼠标释放后，各扳机复位
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._lcorner_drag = False
        self._right_drag = False
        self._left_drag = False
class rotatetab(QTabBar): 
    def tabSizeHint(self, index): 
        s = QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s
    def paintEvent(self, e) : 
        painter = QStylePainter(self)
        opt = QStyleOptionTab() 
        for i in range(self.count()) :
            self.initStyleOption(opt, i)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save() 
            s = opt.rect.size()
            s.transpose()
            r = QRect(QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r 
            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt)
            painter.restore()  
         