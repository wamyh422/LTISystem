# -*- coding: utf-8 -*-

from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math
import wx,string
from numpy import mgrid,sin,cos
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

class LTISystem(wx.Frame):
    def __init__(self,parent,title):
        self.dirname = ''
        wx.Frame.__init__(self,parent,title=title)
        self.SQUARE=False
        self.contrl = wx.BoxSizer(wx.VERTICAL)
        self.contrl.SetMinSize(300,-1)
        self.SetMaxSize((325,250))

        self.CreateStatusBar()# 建立位於視窗的底部的狀態列
        #設定選單
        filemenu = wx.Menu()
        paramenu=wx.Menu()

        
        menuAbout = filemenu.Append(wx.ID_ABOUT,"&About","Information about this program") #(ID, 專案名稱, 狀態列資訊)
        filemenu.AppendSeparator()  #分割線
        menuExit = filemenu.Append(wx.ID_EXIT,"&Exit","Terminate the program") # (ID, 專案名稱, 狀態列資訊)

        self.p1=wx.MenuItem(paramenu,100,text='Square wave',kind=wx.ITEM_NORMAL)
        menup1 = paramenu.Append(100,"&Square wave","square wave approximation")


        #建立選單欄
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&Tools") 
        menuBar.Append(paramenu,"&parameters")
        self.SetMenuBar(menuBar) #在frame中新增選單欄

        #設定 events
        self.Bind(wx.EVT_MENU, self.OnAbout,menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit,menuExit)
        self.Bind(wx.EVT_MENU,self.OnPara1,menup1)

        #系統輸入
        self.st=wx.StaticText(self,-1,"系統設定")
        self.contrl.Add(self.st,0,wx.ALIGN_CENTER|wx.TOP,5)
        self.zero=wx.BoxSizer(wx.HORIZONTAL)
        self.zt = wx.StaticText(self,-1,"分子 : ")
        self.za=wx.TextCtrl(self,-1,size=(250,22))
        self.zero.Add(self.zt)
        self.zero.Add(self.za)
        self.contrl.Add(self.zero,0,wx.ALIGN_CENTER|wx.TOP,5)

        self.pole=wx.BoxSizer(wx.HORIZONTAL)
        self.pt=wx.StaticText(self,-1,"分母 : ")
        self.pa=wx.TextCtrl(self,-1,size=(250,22))
        self.pole.Add(self.pt)
        self.pole.Add(self.pa)
        self.contrl.Add(self.pole,0,wx.ALIGN_CENTER|wx.TOP,5)

        #輸入訊號
        self.it=wx.StaticText(self,-1,"輸入訊號")
        self.contrl.Add(self.it,0,wx.ALIGN_CENTER|wx.TOP,5)
        self.inp=wx.BoxSizer(wx.HORIZONTAL)
        self.st=wx.StaticText(self,-1,"w : ")
        self.sa=wx.TextCtrl(self,-1,size=(200,22))
        self.inp.Add(self.st)
        self.inp.Add(self.sa)
        self.contrl.Add(self.inp,0,wx.ALIGN_CENTER|wx.TOP,5)


        self.button=wx.Button(self, -1, "Test")
        self.contrl.Add(self.button, 1, wx.ALIGN_CENTER|wx.TOP,5)



        self.overview = wx.BoxSizer(wx.HORIZONTAL)
        self.overview.Add(self.contrl,0,wx.GROW)
        self.button.Bind(wx.EVT_BUTTON,self.OnInput)


        #啟用overview
        self.SetSizer(self.overview)
        self.SetAutoLayout(True)
        self.overview.Fit(self)
        self.Show(True)

        #self.Show(True)
    def OnPara1(self,x):
        temp=""
        if self.SQUARE==False:
            for i in range(0,20,1):
                temp+=str(i)+" "
            self.sa.SetEditable(False)
            self.SQUARE=True
        else:
            self.SQUARE=False
            self.sa.SetEditable(True)

        self.sa.SetValue(temp)

    def OnAbout(self,x):
        #建立一個帶"OK"按鈕的對話方塊
        dlg = wx.MessageDialog(self,'Linear-time invariant system\n注意事項\nZeros與Poles皆只能輸入數字，各階係數以空白鍵隔開\n訊號週期固定以sin(2*pi*n*t)格式輸入，請輸入數字，各數以空白鍵隔開',"About LTI System",wx.OK | wx.ALIGN_CENTER) #語法是(self, 內容, 標題, ID)
        dlg.ShowModal() #顯示對話方塊
        dlg.Destroy()   #當結束之後關閉對話方塊

    def OnExit(self,e):
        self.Close(True)  #關閉整個frame
    def OnInput(self,e):
        plt.clf()
        self.Refresh()

        flag=True
        str1 = self.za.GetValue()
        v1 = str1.split()
        x = np.array(v1)

        str2 = self.pa.GetValue()
        v2 = str2.split()
        h = np.array(v2)

        str3 = self.sa.GetValue()
        str3=str3.replace('/',' ')
        v3 = str3.split()
        s = np.array(v3)

        try:
            x=x.astype(float)
            h=h.astype(float)
            s=s.astype(float)
        except:
           dle = wx.MessageDialog(self,"輸入格式為：\分子 : N1 N2 N3 N4 ... \n分母 : N1 N2 N3 N4 ...\nw：N1 N2 N3 N4 ...\n請依照格式輸入!!","Error",wx.OK) #語法是(self, 內容, 標題, ID)
           dle.ShowModal() #顯示對話方塊
           dle.Destroy()   #當結束之後關閉對話方塊
           flag = False

        if flag == False:
            plt.clf()
        elif len(x)==0 or len(h)==0 or len(s)==0:
            dle = wx.MessageDialog(self,"輸入不能為空!!.","Error",wx.OK) #語法是(self, 內容, 標題, ID)
            dle.ShowModal() #顯示對話方塊
            dle.Destroy()   #當結束之後關閉對話方塊
        else:
            sys=signal.dlti(x,h,dt=0.001)
            imp=sys.impulse()
            time=np.arange(0,10,0.01)
            amplitude=np.array(time*0)
            if self.SQUARE==True:
                for i in s:
                    amplitude =np.sin((time*np.pi*(2*i+1)))/(np.pi*(2*i+1))+amplitude
            else:
                amplitude=np.array(time*0)
                for i in s:
                    amplitude = np.sin(time*np.pi/(i))+amplitude
        
            csys=signal.lti(x,h)
            r=range(0,10000,1)
            t,freq=signal.freqresp(csys)
            w,mag,phase = signal.bode(csys,w=r)

            value = np.reshape(imp[1][0],imp[1][0].shape[0])

            plt.subplot(321)
            plt.plot(time,amplitude)
            plt.title('input')

            plt.subplot(322)
            plt.plot(imp[0],value)
            plt.title('impluse response')

            y=signal.convolve(value,amplitude)
            yt=np.arange(0,10.99,0.01)
            plt.subplot(323)
            plt.plot(yt,y)
            plt.title('time response')

            plt.subplot(324)
            plt.plot(t/10,freq)
            plt.title('frequency response')

            plt.subplot(325)
            plt.plot(np.log(w),mag)
            plt.title('frequency mag.')

            plt.subplot(326)
            plt.plot(np.log(w),phase)
            plt.title('frequency phase')

            plt.subplots_adjust(hspace=0.3)

            plt.show()

app = wx.App(False)
frame = LTISystem(None,title="LTI System")
app.MainLoop()