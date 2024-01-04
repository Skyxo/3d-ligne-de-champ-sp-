from math import *

add_library("peasycam")

espace = 900
width, height = espace, espace
eps0 = 8.85418782*10**(-12) # m-3 kg-1 s4 A2
k = 1/(4*pi*eps0)
e = 1.6*10**(-19)
nbvect = 10

class Particule:
    
    def __init__(self, x, y, z, q):
        self.x = x
        self.y = y
        self.z = z
        self.q = q
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getZ(self):
        return self.z
    
    def getQ(self):
        return self.q
    
    def drawParticule(self):
        q = self.getQ()
        
        if q>0:
            fill(0,0,255)
        if q<0:
            fill(255,0,0)

        pushMatrix()
        noStroke()
        translate(self.getX(), self.getY(), self.getZ())
        sphere(10*sqrt(abs(self.getQ()/e)))
        popMatrix()
    
    def getChampFrom(self, xp, yp, zp):
        MP = sqrt((xp-self.getX())**2 + (yp-self.getY())**2 + (zp-self.getZ())**2)

        if MP > 0:
            Ex = k*self.getQ()*(xp-self.getX())/(MP**3)
            Ey = k*self.getQ()*(yp-self.getY())/(MP**3)
            Ez = k*self.getQ()*(zp-self.getZ())/(MP**3)
        else:
            Ex, Ey, Ez = 0, 0, 0
            
        return Ex, Ey, Ez

class Fleche():
    
    def __init__(self, posx, posy, posz, cx, cy, cz):
        self.posx = posx
        self.posy = posy
        self.posz = posz
        self.champx = cx
        self.champy = cy
        self.champz = cz
        
    def getPosX(self):
        return self.posx
    
    def getPosY(self):
        return self.posy
    
    def getPosZ(self):
        return self.posz
    
    def getChampX(self):
        return self.champx
    
    def getChampY(self):
        return self.champy
    
    def getChampZ(self):
        return self.champz
    
    def getNormeChamp(self):
        return sqrt(self.getChampX()**2 + self.getChampY()**2 + self.getChampZ()**2)
    
    def setChamp(self, x, y, z):
        self.champx = x
        self.champy = y
        self.champz = z
    
    def drawArrow(self, maxindic):
        x, y, z = self.getPosX(), self.getPosY(), self.getPosZ()
        cx, cy, cz = self.getChampX(), self.getChampY(), self.getChampZ()
        normechamp = self.getNormeChamp()
        tindic = 0.15
        c = [0,0,0]
    
        if normechamp>0:
            tox = (espace/nbvect)*cx/normechamp
            toy = (espace/nbvect)*cy/normechamp
            toz = (espace/nbvect)*cz/normechamp
            
            if maxindic > 0:
                cindic = normechamp/maxindic
                if 0 < cindic**(0.5) < 0.1:
                    c[0] = 255*((2*cindic))
                    c[1] = 255
                elif 0.1 <= cindic**(0.5) <= 1:
                    c[0] = 255
                    c[1] = 255*(1-(2*cindic))
        else:
            tox, toy, toz = 0, 0, 0
        
        stroke(c[0], c[1], c[2]) #couleur des fleches
        line(x, y, z, x+(1-tindic)*tox, y+(1-tindic)*toy, z+(1-tindic)*toz)
        stroke(255, 255, 255) #couleur des bouts de fleches
        line(x+(1-tindic)*tox, y+(1-tindic)*toy, z+(1-tindic)*toz, x+tox, y+toy, z+toz)
        
#position des vecteurs
def posVect(n):
    
    pos = [[[0 for k in range(nbvect+1)] for j in range(nbvect+1)] for i in range(nbvect+1)]

    for i in range(nbvect+1):
        for j in range(nbvect+1):
            for k in range(nbvect+1):
                pos[i][j][k] = (i*espace/n, j*espace/n, k*espace/n)
        
    return pos

#création des vecteurs
def createArrows(n):
    posvect = posVect(n)
    
    for ligne in posvect:
        for colonne in ligne:
            for v in range(len(colonne)):
                colonne[v] = Fleche(colonne[v][0], colonne[v][1], colonne[v][2], colonne[v][0], colonne[v][1], colonne[v][2])
            
    return posvect
    
#actualisation des vecteurs
def refreshArrows(particules):
    global arrows, maxindic
    
    champs = []
    
    for ligne in arrows:
        for colonne in ligne:
            for arrow in colonne:
                champx = 0
                champy = 0
                champz = 0
                            
                for p in particules:
                    Ex, Ey, Ez = p.getChampFrom(arrow.getPosX(), arrow.getPosY(), arrow.getPosZ())
                    champx+=Ex
                    champy+=Ey
                    champz+=Ez
                
                arrow.setChamp(champx, champy, champz)
                champs.append(arrow.getNormeChamp())
    
    maxindic = max(champs)
    
arrows = createArrows(nbvect) # fleches
x, y, z = espace/2, espace/2, espace/2 #position initiale nouvelle particule
hud=1

#Particules test
p1 = Particule(100,100,100,3*e)
p2 = Particule(0,0,0,-3*e)

v=7 # vitesse de déplacement de la particule

qmouse=0
particules = []
maxindic = 0
        
def setup():
    global cam
    size(width, height, P3D)
    perspective(PI/3.0, float(width)/float(height), 0.001, 100000000)
    
    cam = PeasyCam(this, 1000)
    
def draw():
    global arrows, x, y, z, qmouse
    background(0)
    #background(150,255,255)
    stroke(255)
    translate(-espace/2, -espace/2, -espace/2)
    
    if keyPressed:
        if key == 'd':
            x+=v
        if key=='q':
            x-=v
        if key=='s':
            y+=v
        if key=='z':
            y-=v
        if key==' ':
            z+=v
        if keyCode==CONTROL:
            z-=v
        if keyCode == UP and qmouse!=0:
            qmouse += qmouse/abs(qmouse)
            print("charge : {}eV".format(qmouse))
        if keyCode == DOWN and abs(qmouse) > 1:
            qmouse -= qmouse/abs(qmouse)
            print("charge : {}eV".format(qmouse))
    
    if hud:
        cam.beginHUD()
        textSize(20)
        fill(255)
        text("P : Positif\nN : Negatif\nO : Montre charge\nUP/DOWN : Taille charge\nLEFT/RIGHT : nbVecteurs\nL : Depose une charge\nZ/Q/S/D/SPACE/CTRL : Deplacement", 10, 20)
        cam.endHUD()
    
    if qmouse:
        sp = Particule(x, y, z, qmouse*e)
        particules.append(sp)
    
    refreshArrows(particules)
    
    for ligne in arrows:
        for colonne in ligne:
            for arrow in colonne:
                arrow.drawArrow(maxindic)
            
    for p in particules:
        p.drawParticule()   
    
    if qmouse:   
        particules.remove(particules[-1])
            
def mouseClicked():
    global particules
    #particules.append(Particule(x, y, z, qmouse*e))
    #print("Particule de charge {}eV placee en x={}, y={}, z={}".format(qmouse, x, y, z))
    
def keyPressed():
    global particules, qmouse, nbvect, arrows, espace, x, y, z, hud
    
    if key=="h":
        hud = 0 if hud else 1
    if key=="c":
        particules=[]
        x, y, z = espace/2, espace/2, espace/2
    if key=="+":
        espace+=100
        arrows = createArrows(nbvect)
    if key=="-" and c>100:
        espace-=100
        arrows = createArrows(nbvect)
    if key=='l':
        particules.append(Particule(x, y, z, qmouse*e))
        print("Particule de charge {}eV placee en x={}, y={}, z={}".format(qmouse, x, y, z))
    if key == 'p':
        qmouse = abs(qmouse) if qmouse else 1
        print("charge : {}eV".format(qmouse))
    if key == 'n':
        qmouse = -abs(qmouse) if qmouse else -1
        print("charge : {}eV".format(qmouse))
    if key == 'o':
        x, y, z = c/2, c/2, c/2
        qmouse = 0 if qmouse else 1
    if keyCode == RIGHT:
        nbvect += 1
        arrows = createArrows(nbvect)
    if keyCode == LEFT and nbvect>1:
        nbvect -= 1
        arrows = createArrows(nbvect)
    
