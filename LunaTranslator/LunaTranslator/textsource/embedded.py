  
from utils.config import globalconfig ,_TR   
from textsource.textsourcebase import basetext   
import functools,queue,time,win32utils
 
class embedded(basetext  ): 
     
    def __init__(self,textgetmethod,hookselectdialog,pids,hwnd,pname,parent) : 
         
        self.textgetmethod, self.pids,self.hwnd,self.pname =textgetmethod,pids,hwnd,pname
        self.parent=parent 
        
        hookselectdialog.changeprocessclearsignal.emit()
        self.hookselectdialog=hookselectdialog
        self.newline=queue.Queue()
        self.agentreceiveddata='' 
        b=win32utils.GetBinaryType(pname)
        if b!=0:
            self.embeddedfailed(_TR("暂不支持64程序"))
        else:
            self.parent.startembedsignal.emit(pids[0],self) 
        
        super(embedded,self).__init__(textgetmethod,*self.checkmd5prefix(pname))
    def timeout(self): 
        self.embeddedfailed(_TR("连接超时"))
     
    def unrecognizedengine(self): 
        self.embeddedfailed(_TR("无法识别的引擎"))
    def getenginename(self,name): 
        self.textgetmethod("<msg>"+_TR("识别到引擎")+name) 
    def translate(self,text ,embedcallback):
        self.agentreceiveddata=text
        self.hookselectdialog.getnewsentencesignal.emit(text)
        if globalconfig['autorun']:
            self.newline.put((self.agentreceiveddata,False, embedcallback))
        else:
            embedcallback('zhs',text) 
    def gettextthread(self ): 
            paste_str=self.newline.get()
            return paste_str
    def embeddedfailed(self,result): 
        self.textgetmethod("<msg>"+result+'  '+ _TR("内嵌失败，请使用普通HOOK"))     
    def runonce(self): 
        self.textgetmethod(self.agentreceiveddata,False)
    def end(self): 
        self.parent.ga.quit()
        super().end()