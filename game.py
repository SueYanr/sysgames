import os,queue,random,sys,threading,time
from pynput.keyboard import Listener

import webbrowser

#变量定义
loop=True
a=[]
lenax=0
lenay=0
PlayerX=0
PlayerY=0
openfile=1
waitvalue=False
stoplist=['保存','退出','返回']
exitnum=0
games={'PlayerX':0,'PlayerY':0,'ShotX':256,'ShotY':256,'bullets':{'null':{'x':'null','y':'null'}}}
#初始化
q=queue.Queue()
startmenulist=['新游戏','加载游戏','退出']
startmenutitle='开始游戏'
startmenutips='↑↓键选择，Enter键确定'
filename=[]
filepath=[]
t1=0
t2=0
keyboards=''

#函数定义
def press(key):
    try:

        keys=key.char
        if keys=='a'or keys=='d':
            q.put(keys)
    except AttributeError:
        keys=key.name
        if keys=='esc'or keys=='space'or keys=='enter'or keys=='up'or keys =='down':
            q.put(keys)


def cleanprint():
    os.system('cls')




def start():
    for i in range(38):
        cleanprint()
        print('*'* i,end='')
        print('\nby若流之上')
        print('https://space.bilibili.com/1538929699')
        print('*'*i)
        time.sleep(0.2)

    webbrowser.open('https://space.bilibili.com/1538929699')
    time.sleep(2)

listener=Listener(on_press=press)
listener.start()

#类定义
class menu:
    def __init__(self,title,list,tips,enter=True):
        self.list=list
        self.list2=tuple(list)
        self.len=len(self.list)-1
        self.mode=0
        self.enter=enter
        self.title=title
        self.tips=tips
        self.str=self.list[self.mode]
        self.str+='<'
        self.list[self.mode]=self.str
    def printf(self):
        cleanprint()
        print(self.title)
        if self.enter:
            for i in self.list:
                print(i)
        else:
            for i in self.list:
                print(i,end='')
        print('\n'+self.tips)
    def tick(self,loopexit=True):
        global loop
        while True:
            self.ticks=q.get()
            if self.ticks== 'down':
                self.str=''
                self.str=self.list2[self.mode]
                self.list[self.mode]=self.str
                if self.mode< self.len:
                    self.mode+=1
                else:
                    self.mode=0
                self.str = ''
                self.str = self.list2[self.mode]
                self.str+='<'
                self.list[self.mode] = self.str

                break
            if self.ticks== 'up':
                self.str = ''
                self.str = self.list2[self.mode]
                self.list[self.mode] = self.str
                if self.mode> 0:
                    self.mode-=1
                else:
                    self.mode=self.len
                self.str = ''
                self.str = self.list2[self.mode]
                self.str += '<'
                self.list[self.mode] = self.str
                break
            if self.ticks == 'enter':
                self.str = ''
                self.str = self.list2[self.mode]
                self.list[self.mode] = self.str
                if loopexit:
                    loop=False
                break



class map:
    def __init__(self,mapx,mapy,randomNumber,maps=[]):#创建地图
        global a,lenay,lenax
        if maps==[]:
            for x in range(mapx):
                x_ = []
                for y in range(mapy):
                    if x>17:
                        x_.append(2)
                    else:
                        x_.append(0)
                a.append(x_)
            lenax=mapx-1
            lenay=mapy-1#!
            for i in range(randomNumber):
                xr = random.randint(0, lenax)
                yr = random.randint(0, lenay)#!
                if a[xr][yr]==0:
                    a[xr][yr] = 2
                else:
                    randomNumber+=1
        else:
            a=maps
    def printf(self,tips):
        cleanprint()

        for x1,a_ in enumerate(a):
            for y1,b_ in enumerate(a[x1]):
                if games['PlayerX']==x1 and games['PlayerY']==y1:
                    print(1,end='')
                elif games['ShotX']==x1 and games['ShotY']==y1:
                    print(8,end='')

                else:
                    linshibianliang = 0
                    for key,value in games['bullets'].items():
                        if value['x']==x1 and value['y']==y1:
                            print('.')
                            linshibianliang=1
                            break
                    if linshibianliang==0:
                        print(b_, end='')


            print('')
        print(tips)

class GamePlayer:
    def __init__(self):
        while True:
            global PlayerX,PlayerY,games,lenay,lenax,a
            PlayerX = random.randint(0, lenax)
            PlayerY = random.randint(0, lenay)
            if a[PlayerX][PlayerY]==0 and a[PlayerX+1][PlayerY]==2:

                games['PlayerX']=PlayerX
                games['PlayerY']=PlayerY
                break

    def go(self,gox,goy):  #gox移动x值goy移动y值
        global lenax,lenay,a,games
        print(lenax,lenay)
        if (games['ShotX']!=games['PlayerX']+gox or games['ShotY']!=games['PlayerY']+goy) and games['PlayerX'] + gox < lenax+1 and games['PlayerX'] + gox > -1 and  games['PlayerY']+ goy < lenay+1 and games['PlayerY'] + goy > -1:
            if a[games['PlayerX']+gox][games['PlayerY']+goy]== 0 :
                games['PlayerX'] += gox
                games['PlayerY'] += goy
    def down(self):
        global t2,games,a,prints
        if a[games['PlayerX']+1][games['PlayerY']]==0 and (games['PlayerX']+1!=games['ShotX'] or games['PlayerY']!=games['ShotY']):
            time.sleep(0.15)
            games['PlayerX'] += 1
            t2=time.time()
            prints=1





''''''
class bullet:
    def __init__(self,targetx,targety,gunx,guny,name):
        global games
        self.xv = (targetx - gunx) / (abs(targety - gunx) + abs(targety - guny))
        self.yv = (targety - guny) / (abs(targety - gunx) + abs(targety - guny))
        self.nx = gunx
        self.ny = guny
        if self.xv > 0.3:
            self.nx += 1
        elif self.xv < -0.3:
            self.nx -= 1
        if self.yv > 0.3:
            self.ny += 1
        elif self.yv < -0.3:
            self.ny -= 1
        games['bullets'][name]={'x':self.nx,'vx':self.xv ,'y': self.ny, 'vy': self.yv}

''''''
class shots():

    def __init__(self):
        global games, a, lenay, lenax
        while True:

            shotsx = random.randint(0, lenax)
            shotsy = random.randint(0, lenay)
            if a[shotsx][shotsy] == 0 and a[shotsx + 1][shotsy] == 2 and shotsx>lenax*0.6:
                games['ShotX']=shotsx
                games['ShotY']=shotsy
                print(games)
                break








if os.path.exists('save')==False:
    os.mkdir('save')






start()



#主程序
startmenu=menu(startmenutitle,startmenulist,startmenutips)
startmenu.printf()
while True:
    startmenu.printf()
    startmenu.tick()
    startmenu.printf()
    if loop==False:
        if startmenu.mode==0 or startmenu.mode==1:
            if startmenu.mode==0:
                Gamemap=map(20,40,20)
            if startmenu.mode==1:
                for root,dirs,files in os.walk('save'):
                    if files!=[]and root=='save':
                        for i in files:
                            filename.append(i)
                            filepath.append(os.path.join(root,i))
                filename.append('退出')
                filelen=(len(filename)-1)
                fileload=menu('文件选择',filename,'↑↓选择，Enter确认')
                loop=True
                while True:
                    fileload.printf()
                    fileload.tick()
                    if loop==False :
                        if fileload.mode==filelen:
                            openfile=0
                            break
                        else:
                            pass#打开文件


            if openfile==1:
                gamestop = menu('暂停游戏', stoplist, '↑↓选择，Enter确认')
                gameplayer=GamePlayer()
                Gamemap.printf(tips='')
                prints=0
                Shots=shots()

                while True:
                    t1=time.time()#当前时间
                    t3=0
                    exitnum = 0
                    if q.empty():
                        pass

                    else:
                        keyboards=q.get()
                        if keyboards=='space' and( a[games['PlayerX']+1][games['PlayerY']]==2 or (games['PlayerX']+1==games['ShotX'] and games['PlayerY']==games['ShotY'])):
                            gameplayer.go(-3,0)
                            prints=1
                        if keyboards=='s':
                            gameplayer.go(1,0)
                            prints = 1
                        if keyboards=='a' :
                            gameplayer.go(0,-1)
                            prints = 1
                        if keyboards=='d':
                            gameplayer.go(0,1)
                            prints = 1
                        if keyboards=='esc':
                            gamestop.printf()
                            while True:
                                gamestop.tick()
                                gamestop.printf()
                                if loop==False:
                                    if gamestop.mode==0:
                                        with open('save','w+')as fl:
                                            fl.write(str(a))#!
                                        break
                                    if gamestop.mode==2:
                                        exitnum=1
                                        break
                                    if gamestop.mode==1:

                                        sys.exit()
                            if exitnum==1:
                                break
                    if t1 - t2 > 0.5:
                        gameplayer.down()


                    if prints==1:
                        Gamemap.printf(tips='')
                        prints=0





        if startmenu.mode==2:
            sys.exit()
















