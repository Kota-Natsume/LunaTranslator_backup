 
from traceback import print_exc

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtWidgets import QWidget,QLabel ,QProgressBar,QLineEdit,QPushButton 
import os,threading
from utils.config import globalconfig  ,_TR 
from utils.wrapper import threader
from version import version
import time
from utils.utils import makehtml

from utils.utils import getproxy
def resourcegrid( ) :  
        grid=[ 
            [('OCR-简体中文'),(makehtml('https://github.com/HIllya51/LunaTranslator/releases/download/v1.34.5/zh.zip',True),1,'link'),''],
            [('OCR-繁体中文'),(makehtml("https://github.com/HIllya51/LunaTranslator/releases/download/v1.34.5/cht.zip",True),1,'link')],
            [('OCR-韩语'),(makehtml("https://github.com/HIllya51/LunaTranslator/releases/download/v1.34.5/cht.zip",True),1,'link')],
            [('OCR-俄语'),(makehtml("https://github.com/HIllya51/LunaTranslator/releases/download/v1.1.2/ru.zip",True),1,'link')],
            [('辞书-MeCab'),(makehtml("https://github.com/HIllya51/LunaTranslator/releases/download/v1.0/Mecab.zip",True),1,'link')],
            [('辞书-小学馆'),(makehtml("https://github.com/HIllya51/LunaTranslator/releases/download/v1.0/xiaoxueguan.db",True),1,'link')],
            [('辞书-EDICT'),(makehtml("https://github.com/HIllya51/LunaTranslator/releases/download/v1.0/edict.db",True),1,'link')],
            [('辞书-EDICT2'),(makehtml("https://github.com/HIllya51/LunaTranslator/releases/download/v1.1.2/edict2",True),1,'link')],
            [('辞书-灵格斯词典'),(makehtml("https://github.com/HIllya51/LunaTranslator/releases/download/v1.0/Lingoes.zip",True),1,'link')],
            [('翻译-J北京7'),(makehtml("https://github.com/HIllya51/LunaTranslator/releases/download/v1.0/JBeijing7.zip",True),1,'link')],
            [('翻译-J北京7-用户词典'),(makehtml("https://github.com/HIllya51/LunaTranslator/releases/download/v2.2.0/JBeijing7UserDict.zip",True),1,'link')],
            [('翻译-金山快译'),(makehtml("https://github.com/HIllya51/LunaTranslator/releases/download/v1.0/FastAIT09_Setup.25269.4101.zip",True),1,'link')],
            [('翻译-快译通'),(makehtml("https://github.com/HIllya51/LunaTranslator/releases/download/v1.0/DR.eye.zip",True),1,'link')],
            [('转区-Locale-Emulator'),(makehtml("https://github.com/xupefei/Locale-Emulator/releases/download/v2.5.0.1/Locale.Emulator.2.5.0.1.zip",True),1,'link')],
            [('转区-Locale_Remulator'),(makehtml("https://github.com/InWILL/Locale_Remulator/releases"),1,'link')],
            [('语音-VoiceRoid2'),(makehtml("https://github.com/HIllya51/LunaTranslator/releases/download/v1.0/Yukari2.zip",True),1,'link')],
            [('语音-VOICEVOX'),(makehtml("https://github.com/VOICEVOX/voicevox/releases"),1,'link')],
        ]
        return grid
@threader
def getversion(self):
    import platform
    import requests 
    import shutil
    import zipfile
    from utils.downloader import mutithreaddownload
    # with open('files/about.txt','r',encoding='utf8') as ff:
    #     about=ff.read()
    # with open('files/version.txt','r',encoding='utf8') as ff:
    #     version=ff.read()  
    url='https://github.com/HIllya51/LunaTranslator/releases/'
    self.versiontextsignal.emit(('当前版本')+':'+  version+'  '+("最新版本")+':'+ ('获取中'))#,'',url,url)) 
    try:
        requests.packages.urllib3.disable_warnings()
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
             'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        res= requests.get('https://api.github.com/repos/HIllya51/LunaTranslator/releases/latest', headers=headers ,verify = False,proxies=getproxy()).json() 
        #print(res)
        _version=res['tag_name']
       # print(version)
        #url=res['assets'][0]['browser_download_url'] 
        
        if platform.architecture()[0]=='64bit': 
            bit=''
        elif platform.architecture()[0]=='32bit':
            bit='_x86'
        else:
            raise Exception
        url=f"https://github.com/HIllya51/LunaTranslator/releases/download/{_version}/LunaTranslator{bit}.zip"
    except:
        print_exc()
        _version=_TR("获取失败") 
    self.versiontextsignal.emit((f'{_TR("当前版本")}:{version}  {platform.architecture()[0]}  {_TR("最新版本")}:{ _version}') ) #,'' if version== _version else  newcontent,url,'LunaTranslator.zip'))
    if _version!=_TR("获取失败") and version!=_version:
        if globalconfig['autoupdate']: 
            self.progresssignal.emit('……',0)
        
            savep=f'./cache/update/LunaTranslator{bit}.zip' 
            def endcallback():
                if os.path.exists(f'./cache/update/LunaTranslator'):
                    shutil.rmtree(f'./cache/update/LunaTranslator')
                zipf=(zipfile.ZipFile(f'./cache/update/LunaTranslator{bit}.zip'))
                zipf.extractall('./cache/update')
                self.needupdate=True
                self.updatefile=savep
            mutithreaddownload(savep,url,self.progresssignal.emit,lambda: globalconfig.__getitem__('autoupdate'),endcallback) 
 
def updateprogress(self,text,val):
    self.downloadprogress.setValue(val)
    self.downloadprogress.setFormat(text)

def setTab_about_dicrect(self) : 
    
    self.versionlabel = QLabel()
    self.versionlabel.setOpenExternalLinks(True)
    self.versionlabel.setTextInteractionFlags(Qt.LinksAccessibleByMouse) 
    self.versiontextsignal.connect(lambda x:self.versionlabel.setText(x) )
    self.downloadprogress=QProgressBar()
         
    self.downloadprogress.setRange(0,10000)

    self.downloadprogress.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    self.progresssignal.connect(lambda text,val:updateprogress(self,text,val))
    getversion(self)
def setTab_about(self) : 
    self.tabadd_lazy(self.tab_widget, ('其他设置'), lambda :setTab_aboutlazy(self)) 
def setTab_aboutlazy(self) : 
         
        grid2=[                
                [('自动下载更新(需要连接github)',5),(self.getsimpleswitch(globalconfig ,'autoupdate',callback= lambda x:getversion(self)),1) ,('',10)],
                [(self.versionlabel,10)], 
                [(self.downloadprogress,10)],
                #[(self.versionlabel4,10)] 
        ]  
         
          
        shuominggrid=[
            ['项目网站',(makehtml("https://github.com/HIllya51/LunaTranslator"),3,'link')],
            ['问题反馈',(makehtml("https://github.com/HIllya51/LunaTranslator/issues"),3,'link')],
            
            ['问题反馈_QQ群',(makehtml('https://qm.qq.com/cgi-bin/qm/qr?k=FNOiTlBcER3g7GLlvk6svT5CxvC1jwLf&jump_from=webapi&authKey=2f3GqvuhqU/nsHWMluO/ZKEkhuhVlyZcRd+Sfhgl0ZLO8XAV8BT082q7mujHWlvr',show='770837672'),3,'link')],
            [('如果你感觉该软件对你有帮助，欢迎微信扫码赞助，谢谢~',4)], 
            
        ] 
        tab=self.makesubtab_lazy(['相关说明', '自动更新','资源下载' ],[
                lambda:self.makevbox([self.makegrid(shuominggrid),imgwidget("./files/zan.jpg")]), 
                lambda: self.makescroll(self.makegrid(grid2 )   ) ,
                
                lambda:self.makescroll( self.makegrid(resourcegrid() ) ), 
                ]) 
        return tab

class imgwidget(QWidget):
    def __init__(self,src) -> None:
         super().__init__()
         self.lb=QLabel(self)
         
         self.img=QPixmap.fromImage(QImage(src)) 
    def paintEvent(self, a0) -> None:
         self.lb.resize(self.size())
         self.lb.setPixmap(self.img.scaled(self.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation))
         return super().paintEvent(a0)