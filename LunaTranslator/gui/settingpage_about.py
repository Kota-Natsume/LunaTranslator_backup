 
from traceback import print_exc
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget,QLabel ,QProgressBar
import threading
import os
import shutil
import zipfile
from contextlib import closing
from utils.config import globalconfig ,postprocessconfig,savehook_new
import gui.switchbutton
def getversion(self):
    with open('files/about.txt','r',encoding='utf8') as ff:
        about=ff.read()
    url='https://github.com/HIllya51/LunaTranslator/releases/'
    self.versiontextsignal.emit(about  %(self.version, '获取中','',url,url))
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
        res=requests.get('https://api.github.com/repos/HIllya51/LunaTranslator/releases/latest', headers=headers,proxies=globalconfig['proxies'] ,verify = False).json()  if globalconfig['proxies'] else requests.get('https://api.github.com/repos/HIllya51/LunaTranslator/releases/latest', headers=headers,proxies={'http': None,'https': None} ,verify = False).json() 
        version=res['tag_name']
       # print(version)
        url=res['assets'][0]['browser_download_url']
        newcontent='更新内容：'+res['body']
    except:
        print_exc()
        version="获取失败"
        newcontent=''
    self.versiontextsignal.emit(about %(self.version, version,'' if self.version== version else  newcontent,url,'LunaTranslator.zip'))
    if version!="获取失败" and self.version!=version:
        if globalconfig['autoupdate']:
            self.downloadprogress.show()
            try:
                savep='./tmp/update.zip'
                 
                with closing(requests.get( url, stream=True,verify = False)) as response:#,proxies=globalconfig['proxies'] if globalconfig['proxies'] else {'http': None,'https': None})) as response:
                    file_size=0
                    chunk_size = 1024  # 单次请求最大值
                    content_size = res['assets'][0]['size']#int(response.headers['content-length'])  # 内容体总大小
                    if os.path.exists('tmp')==False:
                        os.mkdir('tmp')
                    
                     
                    if os.path.exists(savep) and os.path.getsize(savep)==content_size:
                        
                        self.progresssignal.emit(f'总大小{int(1000*(int(content_size/1024)/1024))/1000} MB 进度 100%',int(10000 ))
                    else:
                         
                        with open(savep, "wb") as file:
                            for data in response.iter_content(chunk_size=chunk_size):
                                if globalconfig['autoupdate']==False:
                                   
                                    return
                                file.write(data)
                                file_size+=len(data)
                                #print(f'正在下载webdriver 总大小{int(1000*(int(content_size/1024)/1024))/1000} MB 进度 {int(10000*(file_size/content_size))/100}%')
                                self.progresssignal.emit(f'总大小{int(1000*(int(content_size/1024)/1024))/1000} MB 进度 {int(10000*(file_size/content_size))/100:.2f}%',int(10000*file_size/content_size))
                    if os.path.exists('./tmp/LunaTranslator'):
                        shutil.rmtree('./tmp/LunaTranslator')
                    zipf=zipfile.ZipFile('./tmp/update.zip')
                    zipf.extractall('./tmp')
                    self.needupdate=True
                
            except:
                print_exc()
                self.progresssignal.emit('自动更新失败，请手动更新',0)
def updateprogress(self,text,val):
    self.downloadprogress.setValue(val)
    self.downloadprogress.setFormat(text)
     
def setTab_about(self) :
        with open('files/version.txt','r')as ff:
            self.version=ff.read() 
        self.tab_about = QWidget()
        self.tab_widget.addTab(self.tab_about, "资源下载&更新") 
        label = QLabel(self.tab_about)
        self.customSetGeometry(label, 20, 50, 200, 20)
        label.setText("自动下载更新(需要连接github)")
        self.updateswitch =gui.switchbutton.MySwitch(self.tab_about, sign= globalconfig['autoupdate'])
        self.customSetGeometry(self.updateswitch , 250, 50, 20,20)
        def changeupdate(x):
            globalconfig.__setitem__('autoupdate',x)
            if x:
                threading.Thread(target=lambda :getversion(self)).start()
        self.updateswitch.clicked.connect(lambda x:  changeupdate( x)) 

        self.downloadprogress=QProgressBar(self.tab_about)
        self.customSetGeometry(self.downloadprogress, 20, 80, 300, 20)
        
        self.downloadprogress.hide()
        self.downloadprogress.setRange(0,10000)

        self.downloadprogress.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.progresssignal.connect(lambda text,val:updateprogress(self,text,val))


        self.versionlabel = QLabel(self.tab_about)
        self.versionlabel.setOpenExternalLinks(True)
            
        self.versionlabel.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.customSetGeometry(self.versionlabel, 20, 150, 600, 500)

        
        self.versiontextsignal.connect(lambda x:self.versionlabel.setText(x) )
        self.versionlabel.setWordWrap(True)
        self.versionlabel.setAlignment(Qt.AlignTop)
        threading.Thread(target=lambda :getversion(self)).start()